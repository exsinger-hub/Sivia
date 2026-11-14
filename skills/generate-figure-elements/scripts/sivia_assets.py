#!/usr/bin/env python3
"""Sivia element pipeline: plan -> sheet prompt -> (image model) -> key-color cutout -> split -> QA -> placement.

Turns an approved overview's illustrative objects into independent, transparent, correctly sized
assets that can be inserted into draw.io or PowerPoint next to native shapes, text and arrows.

Requires Pillow and numpy (scipy is used when present, never required). Every subcommand prints JSON.
Exit codes: 0 ok, 1 QA failure, 2 invalid input.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from collections import deque
from pathlib import Path

try:
    import numpy as np
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
except ImportError as exc:  # pragma: no cover - environment dependent
    sys.stderr.write(f"sivia_assets.py needs Pillow and numpy: python -m pip install Pillow numpy ({exc})\n")
    raise SystemExit(2)

try:  # optional accelerator
    from scipy import ndimage as _ndi
except Exception:  # pragma: no cover - environment dependent
    _ndi = None

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_TEMPLATE = SKILL_DIR / "references" / "templates" / "element-sheet.txt"
IMAGEGEN = SCRIPT_DIR / "imagegen.mjs"

ID_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{0,47}$")
ROUTES = {"generate", "extract", "native", "data"}
ANCHORS = {"center", "bottom", "top"}
GRIDS = {1: (1, 1), 2: (2, 1), 3: (3, 1), 4: (2, 2), 5: (3, 2), 6: (3, 2), 7: (4, 2), 8: (4, 2), 9: (3, 3)}
KEY_CANDIDATES = ["#00FF00", "#FF00FF", "#00FFFF", "#FFFF00", "#FF8000", "#0000FF"]
DEFAULT_RASTER_REASON = (
    "Independent illustrative artwork produced with an image model and a key-color cutout; it has no editable "
    "native equivalent and carries no empirical data."
)
DEFAULT_DECOMPOSITION = (
    "Single element cut from a clean asset sheet; labels, arrows, frames and other reconstructable objects "
    "are rebuilt natively outside this picture."
)


class AssetError(Exception):
    """Invalid input or unusable data (exit code 2)."""


# --------------------------------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------------------------------
def hex_to_rgb(value):
    match = re.fullmatch(r"#?([0-9a-fA-F]{6})", str(value).strip())
    if not match:
        raise AssetError(f"not a #RRGGBB color: {value!r}")
    number = int(match.group(1), 16)
    return ((number >> 16) & 255, (number >> 8) & 255, number & 255)


def rgb_to_hex(rgb):
    return "#%02X%02X%02X" % tuple(int(round(max(0, min(255, float(v))))) for v in rgb)


def read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise AssetError(f"file not found: {path}")
    except json.JSONDecodeError as error:
        raise AssetError(f"{path} is not valid JSON: {error}")


def write_json(path, payload):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_size(text, label="size"):
    match = re.fullmatch(r"(\d+)\s*[xX×]\s*(\d+)", str(text).strip())
    if not match:
        raise AssetError(f"{label} must look like 1536x1024")
    width, height = int(match.group(1)), int(match.group(2))
    if width <= 0 or height <= 0:
        raise AssetError(f"{label} must be positive")
    return width, height


class Workdir:
    """One figure's element files. Every path can still be overridden on the command line."""

    def __init__(self, root):
        self.root = Path(root or ".").resolve()
        self.plan = self.root / "elements.json"
        self.style = self.root / "style-lock.json"
        self.prompts = self.root / "prompts"
        self.sheets = self.root / "sheets"
        self.assets = self.root / "assets"
        self.qa = self.root / "qa"
        self.manifest = self.root / "manifest.json"


# --------------------------------------------------------------------------------------------------
# Plan (elements.json)
# --------------------------------------------------------------------------------------------------
def load_plan(path):
    plan = read_json(path)
    if not isinstance(plan, dict) or not isinstance(plan.get("elements"), list) or not plan["elements"]:
        raise AssetError("elements.json needs a non-empty 'elements' list")
    seen = set()
    for element in plan["elements"]:
        if not isinstance(element, dict):
            raise AssetError("every element must be an object")
        element_id = element.get("id")
        if not isinstance(element_id, str) or not ID_RE.fullmatch(element_id):
            raise AssetError(f"element id {element_id!r} must match {ID_RE.pattern} (lowercase slug)")
        if element_id in seen:
            raise AssetError(f"duplicate element id: {element_id}")
        seen.add(element_id)
        route = element.setdefault("route", "generate")
        if route not in ROUTES:
            raise AssetError(f"{element_id}: route must be one of {sorted(ROUTES)}")
        if route == "generate" and not str(element.get("description", "")).strip():
            raise AssetError(f"{element_id}: a generated element needs a description")
        slot = element.get("slot")
        if slot is not None:
            box = slot.get("bbox_px") if isinstance(slot, dict) else None
            if not (isinstance(box, list) and len(box) == 4 and all(isinstance(v, (int, float)) for v in box)
                    and box[2] > box[0] and box[3] > box[1]):
                raise AssetError(f"{element_id}: slot.bbox_px must be [x0, y0, x1, y1] with x1>x0 and y1>y0")
            if slot.get("anchor", "center") not in ANCHORS:
                raise AssetError(f"{element_id}: slot.anchor must be one of {sorted(ANCHORS)}")
    figure = plan.setdefault("figure", {})
    figure.setdefault("target_dpi", 300)
    size = figure.get("ref_size_px")
    if size is not None and not (isinstance(size, list) and len(size) == 2 and all(v > 0 for v in size)):
        raise AssetError("figure.ref_size_px must be [width, height]")
    return plan


def placed_width_mm(plan, element):
    """Physical width the element will occupy, from an explicit width or its slot, if known."""
    if element.get("width_mm"):
        return float(element["width_mm"])
    figure = plan.get("figure", {})
    slot = element.get("slot")
    if slot and figure.get("ref_size_px") and figure.get("width_mm"):
        x0, _, x1, _ = slot["bbox_px"]
        return (x1 - x0) / float(figure["ref_size_px"][0]) * float(figure["width_mm"])
    return None


def required_pixels(width_mm, dpi):
    return math.ceil(width_mm * dpi / 25.4)


# --------------------------------------------------------------------------------------------------
# Palette and key color
# --------------------------------------------------------------------------------------------------
def extract_palette(image, colors=8, ignore_light=True):
    small = image.convert("RGB")
    small.thumbnail((256, 256))
    quantized = small.quantize(colors=max(2, colors), method=Image.Quantize.MEDIANCUT)
    palette = quantized.getpalette() or []
    counts = quantized.getcolors() or []
    total = sum(count for count, _ in counts) or 1
    result = []
    for count, index in sorted(counts, reverse=True):
        rgb = tuple(palette[index * 3: index * 3 + 3])
        if len(rgb) < 3:
            continue
        r, g, b = (v / 255.0 for v in rgb)
        light = max(r, g, b) > 0.93 and (max(r, g, b) - min(r, g, b)) < 0.08
        if ignore_light and light:
            continue
        result.append({"hex": rgb_to_hex(rgb), "share": round(count / total, 4)})
    return result


def recommend_key(palette_hex, candidates=None):
    """Pick the candidate key color farthest from every palette color (RGB distance, 0..441)."""
    candidates = candidates or KEY_CANDIDATES
    colors = [hex_to_rgb(value) for value in palette_hex] or [(128, 128, 128)]
    scored = []
    for candidate in candidates:
        key = np.array(hex_to_rgb(candidate), dtype=np.float32)
        nearest = min(float(np.linalg.norm(key - np.array(color, dtype=np.float32))) for color in colors)
        scored.append((nearest, candidate))
    scored.sort(reverse=True)
    return {"key": scored[0][1], "min_distance": round(scored[0][0], 1), "ranking": [{"key": c, "min_distance": round(d, 1)} for d, c in scored]}


# --------------------------------------------------------------------------------------------------
# Connected components (scipy when available, small pure-Python fallback otherwise)
# --------------------------------------------------------------------------------------------------
def label_components(mask):
    mask = np.asarray(mask, dtype=bool)
    if _ndi is not None:
        labels, count = _ndi.label(mask, structure=np.ones((3, 3), dtype=int))
        return labels, int(count)
    height, width = mask.shape
    labels = np.zeros(mask.shape, dtype=np.int32)
    count = 0
    flat_mask = mask.ravel()
    flat_labels = labels.ravel()
    for start in np.flatnonzero(flat_mask):
        if flat_labels[start]:
            continue
        count += 1
        flat_labels[start] = count
        queue = deque([start])
        while queue:
            node = queue.popleft()
            row, col = divmod(node, width)
            for d_row in (-1, 0, 1):
                n_row = row + d_row
                if n_row < 0 or n_row >= height:
                    continue
                for d_col in (-1, 0, 1):
                    n_col = col + d_col
                    if 0 <= n_col < width:
                        neighbour = n_row * width + n_col
                        if flat_mask[neighbour] and not flat_labels[neighbour]:
                            flat_labels[neighbour] = count
                            queue.append(neighbour)
    return labels, count


def component_areas(mask):
    labels, count = label_components(mask)
    if count == 0:
        return labels, []
    return labels, np.bincount(labels.ravel(), minlength=count + 1)[1:].tolist()


def _box_sum(values, radius):
    size = 2 * radius + 1
    padded = np.pad(values, ((radius, radius), (radius, radius)), mode="constant")
    integral = np.zeros((padded.shape[0] + 1, padded.shape[1] + 1), dtype=np.float64)
    integral[1:, 1:] = padded.cumsum(0).cumsum(1)
    return integral[size:, size:] - integral[:-size, size:] - integral[size:, :-size] + integral[:-size, :-size]


def _dilate(mask, radius):
    """Square dilation via an integral image: constant cost whatever the radius."""
    if radius <= 0:
        return np.asarray(mask, dtype=bool)
    return _box_sum(np.asarray(mask, dtype=np.float64), radius) > 0.5


# --------------------------------------------------------------------------------------------------
# Key-color cutout (known-background matting)
# --------------------------------------------------------------------------------------------------
def propagate_foreground(arr, core, need, min_support=3.0):
    """Colour of nearby definite-foreground pixels for every `need` pixel (normalised convolution)."""
    out = np.zeros_like(arr, dtype=np.float32)
    remaining = need.copy()
    core_f = core.astype(np.float64)
    for radius in (2, 4, 8, 16, 32):
        if not remaining.any():
            break
        weight = _box_sum(core_f, radius)
        usable = remaining & (weight >= min_support)
        if usable.any():
            for channel in range(3):
                total = _box_sum(arr[..., channel].astype(np.float64) * core_f, radius)
                out[..., channel][usable] = (total[usable] / weight[usable]).astype(np.float32)
            remaining &= ~usable
    filled = need & ~remaining
    return out, filled


def measure_background(rgb, frame=0.02):
    height, width = rgb.shape[:2]
    thickness = max(2, int(min(height, width) * frame))
    border = np.concatenate([
        rgb[:thickness].reshape(-1, 3), rgb[-thickness:].reshape(-1, 3),
        rgb[:, :thickness].reshape(-1, 3), rgb[:, -thickness:].reshape(-1, 3),
    ]).astype(np.float32)
    return np.median(border, axis=0), border.std(axis=0)


def chroma_cutout(rgb, key, lo=28.0, hi=90.0, erode=0, min_island=None):
    """Return (RGBA uint8, stats). Pixels near `key` become transparent; edge colours are re-estimated from
    the neighbouring foreground and alpha is solved against the known key, so no key-colour fringe remains."""
    if not 0 <= lo < hi:
        raise AssetError("--lo must be >= 0 and smaller than --hi")
    arr = rgb.astype(np.float32)
    key_vec = np.array(key, dtype=np.float32)
    diff = arr - key_vec
    distance = np.sqrt((diff ** 2).sum(-1))
    core = distance >= hi
    background = distance <= lo
    transition = ~(core | background)
    # Only background pixels near the subject need a clean colour (they border the edge when an asset is cropped).
    near = _dilate(core, 16)
    estimate, filled = propagate_foreground(arr, core, transition | (background & near))

    alpha = np.zeros(distance.shape, dtype=np.float32)
    alpha[core] = 1.0
    if transition.any():
        fg_minus_key = estimate - key_vec
        denominator = (fg_minus_key ** 2).sum(-1)
        numerator = (diff * fg_minus_key).sum(-1)
        solved = np.clip(np.where(denominator > 1e-3, numerator / np.maximum(denominator, 1e-3), 0.0), 0.0, 1.0)
        ramp = np.clip((distance - lo) / (hi - lo), 0.0, 1.0)
        alpha[transition] = np.where(filled, solved, ramp)[transition]

    colour = arr.copy()
    recolour = (transition | (background & near)) & filled
    colour[recolour] = estimate[recolour]

    alpha8 = np.round(alpha * 255.0).astype(np.uint8)
    if erode > 0:
        alpha8 = np.asarray(Image.fromarray(alpha8, mode="L").filter(ImageFilter.MinFilter(2 * erode + 1)))

    # Real generators leave a few stray pixels near the image edge whose colour drifts into the transition band.
    # A component that never reaches solid alpha is noise, not artwork; subject edges stay because they touch solid pixels.
    removed = 0
    present_labels, present_count = label_components(alpha8 > 0)
    if present_count:
        strong = np.unique(present_labels[alpha8 > 127])
        weak = (present_labels > 0) & ~np.isin(present_labels, strong[strong > 0])
        if weak.any():
            removed += int(len(np.unique(present_labels[weak])))
            alpha8[weak] = 0

    threshold = int(min_island) if min_island is not None else max(50, int(alpha8.size * 0.0004))
    solid = alpha8 > 127
    labels, areas = component_areas(solid)
    small = [index + 1 for index, area in enumerate(areas) if area < threshold]
    if small:
        drop = np.isin(labels, small)
        alpha8[_dilate(drop, 3)] = 0
        removed += len(small)

    rgba = np.dstack([np.clip(colour, 0, 255).astype(np.uint8), alpha8])
    stats = {
        "transparent_fraction": round(float((alpha8 == 0).mean()), 4),
        "opaque_fraction": round(float((alpha8 == 255).mean()), 4),
        "partial_fraction": round(float(((alpha8 > 0) & (alpha8 < 255)).mean()), 4),
        "removed_specks": removed,
        "speck_threshold_px": threshold,
    }
    return rgba, stats


# --------------------------------------------------------------------------------------------------
# prompt
# --------------------------------------------------------------------------------------------------
def style_block(plan, style_lock):
    style = {**(style_lock or {}), **(plan.get("style") or {})}
    palette = style.get("palette") or [item["hex"] if isinstance(item, dict) else item for item in (style_lock or {}).get("palette", [])]
    lines = [
        f"- Rendering: {style.get('summary') or 'clean flat vector-style scientific illustration, restrained palette, no photorealism'}.",
    ]
    if palette:
        lines.append(f"- Palette: use only these hues and their light/dark tints: {', '.join(palette)}.")
    lines.append(f"- Line work: {style.get('line') or 'one uniform dark outline weight on every illustration'}.")
    lines.append(f"- Shading: {style.get('shading') or 'flat fills with at most one soft shadow tone; light from the upper left'}.")
    lines.append("- Consistency: every illustration shares the same outline weight, corner softness, level of detail, lighting and visual weight, so they look drawn by one hand.")
    for extra in style.get("avoid", []):
        lines.append(f"- Avoid: {extra}.")
    return "\n".join(lines)


def element_lines(elements, cols):
    lines = []
    for index, element in enumerate(elements):
        row, col = divmod(index, cols)
        label = element.get("label") or element["id"]
        parts = [f"{index + 1}. [row {row + 1}, column {col + 1}] {label}: {str(element['description']).strip().rstrip('.')}."]
        if element.get("view"):
            parts.append(f"View: {element['view']}.")
        if element.get("must_show"):
            parts.append("Must show: " + "; ".join(element["must_show"]) + ".")
        if element.get("must_not_contain"):
            parts.append("Must not contain: " + "; ".join(element["must_not_contain"]) + ".")
        lines.append(" ".join(parts))
    return "\n".join(lines)


def group_sheets(plan, per_sheet):
    """Explicit `sheet` names are honoured, 'solo' gives one sheet per element, the rest are chunked in order."""
    generated = [e for e in plan["elements"] if e.get("route") == "generate"]
    explicit, loose, solos = {}, [], []
    for element in generated:
        name = element.get("sheet")
        if name == "solo":
            solos.append(element)
        elif name:
            explicit.setdefault(re.sub(r"[^a-z0-9_-]+", "-", str(name).lower()), []).append(element)
        else:
            loose.append(element)
    groups = []
    for name, members in explicit.items():
        for start in range(0, len(members), 9):
            groups.append((f"sheet-{name}" + (f"-{start // 9 + 1}" if len(members) > 9 else ""), members[start:start + 9]))
    for start in range(0, len(loose), per_sheet):
        groups.append((f"sheet-{start // per_sheet + 1:02d}", loose[start:start + per_sheet]))
    for element in solos:
        groups.append((f"solo-{element['id']}", [element]))
    return groups


def default_canvas(cols, rows):
    if cols > rows:
        return 1536, 1024
    if rows > cols:
        return 1024, 1536
    return 1024, 1024


def command_prompt(args):
    wd = Workdir(args.workdir)
    plan = load_plan(args.plan or wd.plan)
    style_path = Path(args.style) if args.style else wd.style
    style_lock = read_json(style_path) if style_path.exists() else {}
    template_path = Path(args.template) if args.template else DEFAULT_TEMPLATE
    try:
        template = template_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise AssetError(f"prompt template not found: {template_path}")
    if not 1 <= args.per_sheet <= 9:
        raise AssetError("--per-sheet must be between 1 and 9")

    palette_hex = [item["hex"] if isinstance(item, dict) else item for item in (plan.get("style", {}).get("palette") or style_lock.get("palette") or [])]
    if args.key == "auto":
        key = (style_lock.get("recommended_key") or recommend_key(palette_hex)["key"]) if (palette_hex or style_lock.get("recommended_key")) else "#00FF00"
    else:
        key = rgb_to_hex(hex_to_rgb(args.key))
    key_rgb = hex_to_rgb(key)
    if palette_hex:
        nearest = min(float(np.linalg.norm(np.array(key_rgb) - np.array(hex_to_rgb(c)))) for c in palette_hex)
        if nearest < 150:
            sys.stderr.write(f"warning: key {key} is only {nearest:.0f} away from the palette; consider --key with a different hue\n")

    groups = group_sheets(plan, args.per_sheet)
    if not groups:
        raise AssetError("no element has route 'generate'; nothing to put on a sheet")
    wd.prompts.mkdir(parents=True, exist_ok=True)
    dpi = float(plan["figure"].get("target_dpi", 300))
    sheets = []
    for sheet_id, members in groups:
        cols, rows = GRIDS[len(members)]
        width, height = parse_size(args.canvas, "--canvas") if args.canvas else default_canvas(cols, rows)
        cell_w, cell_h = width // cols, height // rows
        empty = [f"row {i // cols + 1}, column {i % cols + 1}" for i in range(len(members), cols * rows)]
        text = template
        replacements = {
            "count": str(len(members)), "width": str(width), "height": str(height), "key_hex": key,
            "key_rgb": f"{key_rgb[0]}, {key_rgb[1]}, {key_rgb[2]}", "cols": str(cols), "rows": str(rows),
            "cell_w": str(cell_w), "cell_h": str(cell_h),
            "empty_cells_rule": ("Leave these cells completely empty (pure background): " + "; ".join(empty) + ".") if empty else "",
            "element_list": element_lines(members, cols), "style_block": style_block(plan, style_lock),
            "extra_rules": plan.get("sheet_rules", ""),
        }
        for name, value in replacements.items():
            text = text.replace("{{" + name + "}}", value)
        leftover = sorted(set(re.findall(r"{{(\w+)}}", text)))
        if leftover:
            raise AssetError(f"template has unfilled placeholders: {leftover}")
        text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"
        prompt_file = wd.prompts / f"{sheet_id}.txt"
        prompt_file.write_text(text, encoding="utf-8")

        warnings = []
        subject_px = int(min(cell_w, cell_h) * 0.7)
        for element in members:
            width_mm = placed_width_mm(plan, element)
            if width_mm:
                need = required_pixels(width_mm, dpi)
                if subject_px < need:
                    warnings.append(f"{element['id']}: needs about {need}px across at {width_mm:.1f} mm / {dpi:g} dpi but the sheet gives ~{subject_px}px; use sheet 'solo', fewer per sheet or a larger --canvas")
        layout = {
            "sheet_id": sheet_id, "canvas_px": [width, height], "grid": [cols, rows], "cell_px": [cell_w, cell_h],
            "key": key, "order": [e["id"] for e in members], "prompt_file": str(prompt_file.relative_to(wd.root)),
            "prompt_chars_nonspace": len(re.sub(r"\s+", "", text)), "plan_sha256": hashlib.sha256(json.dumps(plan, sort_keys=True).encode()).hexdigest(),
        }
        write_json(wd.prompts / f"{sheet_id}.layout.json", layout)
        refs = [str(Path(r)) for r in (plan.get("style", {}).get("references") or [])]
        command = f'node "{IMAGEGEN}" generate --prompt-file "{prompt_file}" --size {width}x{height} --quality high --out "{wd.sheets / (sheet_id + ".png")}"'
        if refs:
            command = command.replace(" generate ", " edit ", 1) + "".join(f' --image "{r}"' for r in refs)
        sheets.append({**layout, "warnings": warnings, "imagegen_command": command, "reference_images": refs})
    return {"workdir": str(wd.root), "key": key, "sheets": sheets}


# --------------------------------------------------------------------------------------------------
# cutout / split
# --------------------------------------------------------------------------------------------------
def command_cutout(args):
    wd = Workdir(args.workdir)
    layout = None
    if args.sheet_id:
        layout = read_json(wd.prompts / f"{args.sheet_id}.layout.json")
    source = Path(args.image) if args.image else (wd.sheets / f"{args.sheet_id}.png" if args.sheet_id else None)
    if source is None:
        raise AssetError("give --sheet-id (with --workdir) or --image")
    output = Path(args.out) if args.out else source.with_name(source.stem + ".rgba.png")
    if output.resolve() == source.resolve():
        raise AssetError("--out must differ from the source image")
    with Image.open(source) as handle:
        rgb = np.asarray(handle.convert("RGB"))
    measured, spread = measure_background(rgb)
    # The painted background is rarely the exact colour that was requested (#00FF00 often arrives as #08F601). Edge pixels blend with
    # what was actually painted, so the measured border colour is the reference unless a colour is forced with --key #RRGGBB.
    forced = args.key if args.key and args.key.lower() != "auto" else None
    requested = forced or (layout or {}).get("key")
    key = tuple(float(v) for v in hex_to_rgb(forced)) if forced else tuple(float(v) for v in measured)
    deviation = float(np.linalg.norm(measured - np.array(hex_to_rgb(requested), dtype=np.float32))) if requested else 0.0
    warnings = []
    if requested and deviation > 40:
        warnings.append(f"the generated background ({rgb_to_hex(measured)}) is {deviation:.0f} away from the requested key {requested}; the model did not paint a flat key color. Check the sheet image before trusting the cut-out.")
    if float(spread.max()) > 12:
        warnings.append(f"the background varies (std {float(spread.max()):.1f}); a gradient or texture may leave patches. Raise --lo or regenerate with a stricter background instruction.")
    rgba, stats = chroma_cutout(rgb, key, lo=args.lo, hi=args.hi, erode=args.erode, min_island=args.min_island)
    output.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(rgba, mode="RGBA").save(output)
    return {
        "input": str(source), "output": str(output), "size_px": [rgb.shape[1], rgb.shape[0]],
        "key_requested": requested, "key_used": rgb_to_hex(key), "key_source": "forced" if forced else "measured border", "measured_background": rgb_to_hex(measured),
        "background_spread": [round(float(v), 2) for v in spread], "warnings": warnings, **stats,
    }


def load_manifest(wd, plan):
    if wd.manifest.exists():
        manifest = read_json(wd.manifest)
    else:
        manifest = {"version": 1, "elements": [], "sheets": {}}
    manifest["figure"] = plan.get("figure", {})
    return manifest


def upsert(manifest, entry):
    for index, existing in enumerate(manifest["elements"]):
        if existing["id"] == entry["id"]:
            manifest["elements"][index] = {**existing, **entry}
            return
    manifest["elements"].append(entry)


def alpha_bbox(alpha, threshold=16):
    mask = (np.asarray(alpha) > threshold)
    if not mask.any():
        return None
    rows = np.flatnonzero(mask.any(axis=1))
    cols = np.flatnonzero(mask.any(axis=0))
    return int(cols[0]), int(rows[0]), int(cols[-1]) + 1, int(rows[-1]) + 1


def command_split(args):
    wd = Workdir(args.workdir)
    plan = load_plan(args.plan or wd.plan)
    layout = read_json(args.layout) if args.layout else read_json(wd.prompts / f"{args.sheet_id}.layout.json")
    sheet_id = layout["sheet_id"]
    sheet_path = Path(args.sheet) if args.sheet else wd.sheets / f"{sheet_id}.rgba.png"
    if not sheet_path.exists():
        raise AssetError(f"cut-out sheet not found: {sheet_path} (run cutout first)")
    boxes = {}
    for item in args.box or []:
        match = re.fullmatch(r"([a-z0-9_-]+)=(\d+),(\d+),(\d+),(\d+)", item)
        if not match:
            raise AssetError(f"--box expects id=x0,y0,x1,y1, got {item!r}")
        boxes[match.group(1)] = tuple(int(match.group(i)) for i in range(2, 6))
    with Image.open(sheet_path) as handle:
        sheet = handle.convert("RGBA")
    width, height = sheet.size
    cols, rows = layout["grid"]
    wd.assets.mkdir(parents=True, exist_ok=True)
    manifest = load_manifest(wd, plan)
    lookup = {e["id"]: e for e in plan["elements"]}
    results = []
    for index, element_id in enumerate(layout["order"]):
        if element_id not in lookup:
            raise AssetError(f"layout lists {element_id}, which is not in elements.json")
        row, col = divmod(index, cols)
        cell = boxes.get(element_id) or (round(col * width / cols), round(row * height / rows), round((col + 1) * width / cols), round((row + 1) * height / rows))
        crop = sheet.crop(cell)
        bbox = alpha_bbox(crop.getchannel("A"))
        problems, notes = [], []
        if bbox is None:
            results.append({"id": element_id, "status": "fail", "problems": ["empty cell: nothing visible after the cutout"]})
            continue
        touches = bbox[0] <= 1 or bbox[1] <= 1 or bbox[2] >= crop.width - 1 or bbox[3] >= crop.height - 1
        if touches and element_id not in boxes:
            problems.append("the element touches its cell border: it is clipped or bleeds into a neighbour; regenerate with more margin or pass --box")
        _, areas = component_areas(np.asarray(crop.getchannel("A")) > 127)
        big = [a for a in areas if a >= 0.02 * max(areas)] if areas else []
        if len(big) > 1:
            notes.append(f"{len(big)} separate shapes in this cell; fine for a multi-part object, a problem if a neighbour spilled in")
        pad = args.pad_px
        tight = crop.crop(bbox)
        asset = Image.new("RGBA", (tight.width + 2 * pad, tight.height + 2 * pad), (0, 0, 0, 0))
        asset.paste(tight, (pad, pad))
        target = wd.assets / f"{element_id}.png"
        asset.save(target, optimize=True)
        entry = {
            "id": element_id, "route": lookup[element_id].get("route", "generate"), "file": str(target.relative_to(wd.root)),
            "size_px": list(asset.size), "visible_bbox_px": [pad, pad, pad + tight.width, pad + tight.height],
            "sheet": sheet_id, "sheet_cell_px": list(cell), "key": layout.get("key"), "sha256": sha256_file(target),
        }
        upsert(manifest, entry)
        results.append({"id": element_id, "status": "fail" if problems else "ok", "file": str(target), "size_px": list(asset.size),
                        "visible_px": [tight.width, tight.height], "problems": problems, "notes": notes})
    manifest["sheets"][sheet_id] = {"layout": f"prompts/{sheet_id}.layout.json", "prompt": layout.get("prompt_file"), "cutout": str(Path(sheet_path).name)}
    # Keep the manifest in plan order so placement z-order is predictable.
    order = {e["id"]: i for i, e in enumerate(plan["elements"])}
    manifest["elements"].sort(key=lambda e: order.get(e["id"], 10 ** 6))
    write_json(wd.manifest, manifest)
    return {"sheet": sheet_id, "manifest": str(wd.manifest), "elements": results}


# --------------------------------------------------------------------------------------------------
# qa
# --------------------------------------------------------------------------------------------------
def checkerboard(size, cell=12):
    tile = Image.new("RGB", size, (255, 255, 255))
    draw = ImageDraw.Draw(tile)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle([x, y, x + cell - 1, y + cell - 1], fill=(204, 204, 204))
    return tile


def on_background(asset, background, size):
    tile = checkerboard(size) if background == "checker" else Image.new("RGB", size, background)
    fitted = asset.copy()
    fitted.thumbnail((size[0] - 16, size[1] - 16), Image.Resampling.LANCZOS)
    tile.paste(fitted, ((size[0] - fitted.width) // 2, (size[1] - fitted.height) // 2), fitted)
    return tile


def inspect_asset(path, key_hex, width_mm, target_dpi):
    with Image.open(path) as handle:
        asset = handle.convert("RGBA")
    arr = np.asarray(asset)
    alpha = arr[..., 3]
    report = {"size_px": list(asset.size), "alpha_extrema": [int(alpha.min()), int(alpha.max())]}
    problems, warnings = [], []
    if alpha.min() != 0 or alpha.max() == 0:
        problems.append("no real transparency: the alpha channel lacks fully transparent or visible pixels")
    bbox = alpha_bbox(alpha)
    if bbox is None:
        problems.append("nothing visible")
        report.update(problems=problems, warnings=warnings)
        return asset, report
    report["visible_bbox_px"] = list(bbox)
    visible_w, visible_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    report["visible_size_px"] = [visible_w, visible_h]
    report["visible_fraction"] = round(float((alpha > 16).mean()), 4)
    if bbox[0] <= 0 or bbox[1] <= 0 or bbox[2] >= asset.width or bbox[3] >= asset.height:
        problems.append("visible pixels touch the image edge, so the subject may be clipped")
    _, areas = component_areas(alpha > 127)
    if areas:
        specks = [a for a in areas if a < 0.002 * max(areas)]
        report["components"] = len(areas)
        if specks:
            warnings.append(f"{len(specks)} tiny detached specks remain; remove with cutout --min-island or by hand")
    edge = (alpha > 8) & (alpha < 248)
    if edge.any() and key_hex:
        key = np.array(hex_to_rgb(key_hex), dtype=np.float32)
        distance = np.linalg.norm(arr[..., :3].astype(np.float32) - key, axis=-1)
        spill = float((distance[edge] < 90).mean())
        report["edge_key_spill"] = round(spill, 3)
        if spill > 0.15:
            problems.append(f"{spill:.0%} of edge pixels still carry the key color; re-run cutout with --erode 1 or a larger --hi")
        elif spill > 0.05:
            warnings.append(f"{spill:.0%} of edge pixels are close to the key color; inspect the edge on a dark background")
    if width_mm:
        effective = visible_w * 25.4 / width_mm
        report["placed_width_mm"] = round(width_mm, 2)
        report["effective_dpi"] = round(effective, 1)
        report["required_px_at_target"] = required_pixels(width_mm, target_dpi)
        if effective < 0.5 * target_dpi:
            problems.append(f"only {effective:.0f} dpi at {width_mm:.1f} mm; regenerate this element alone at a larger size or place it smaller")
        elif effective < target_dpi:
            warnings.append(f"{effective:.0f} dpi at {width_mm:.1f} mm is below the {target_dpi:g} dpi target")
    report.update(problems=problems, warnings=warnings)
    return asset, report


def command_qa(args):
    wd = Workdir(args.workdir)
    plan = load_plan(args.plan or wd.plan)
    manifest = load_manifest(wd, plan)
    dpi = float(plan["figure"].get("target_dpi", 300))
    backgrounds = ["checker", (255, 255, 255), (31, 41, 55)] + [hex_to_rgb(c) for c in (args.bg or [])]
    if plan["figure"].get("background") and plan["figure"]["background"].upper() not in {"#FFFFFF"}:
        backgrounds.append(hex_to_rgb(plan["figure"]["background"]))
    wd.qa.mkdir(parents=True, exist_ok=True)
    reports, tiles, finals = [], [], []
    tile = 220
    for element in plan["elements"]:
        if element.get("route") not in {"generate", "extract"}:
            continue
        path = wd.assets / f"{element['id']}.png"
        if not path.exists():
            reports.append({"id": element["id"], "status": "fail", "problems": [f"missing asset {path.name}"], "warnings": []})
            continue
        entry = next((e for e in manifest["elements"] if e["id"] == element["id"]), {})
        width_mm = placed_width_mm(plan, element)
        asset, report = inspect_asset(path, entry.get("key"), width_mm, dpi)
        report["id"] = element["id"]
        report["status"] = "fail" if report["problems"] else ("warn" if report["warnings"] else "pass")
        reports.append(report)
        row = Image.new("RGB", (tile * len(backgrounds), tile + 22), (245, 245, 245))
        for i, background in enumerate(backgrounds):
            row.paste(on_background(asset, background, (tile, tile)), (i * tile, 22))
        ImageDraw.Draw(row).text((6, 5), f"{element['id']}  [{report['status']}]", fill=(0, 0, 0), font=ImageFont.load_default())
        tiles.append(row)
        if width_mm:
            size = max(8, round(width_mm * args.preview_dpi / 25.4))
            resized = asset.resize((size, max(1, round(size * asset.height / asset.width))), Image.Resampling.LANCZOS)
            finals.append((element["id"], resized))
        upsert(manifest, {"id": element["id"], "qa": {"status": report["status"], **{k: v for k, v in report.items() if k not in {"id", "status"}}},
                          "raster_reason": element.get("raster_reason", DEFAULT_RASTER_REASON),
                          "decomposition_note": element.get("decomposition_note", DEFAULT_DECOMPOSITION),
                          "role": "schematic illustration (not empirical data)" if element.get("route") == "generate" else element.get("role", "illustration")})
    outputs = {}
    if tiles:
        sheet = Image.new("RGB", (max(t.width for t in tiles), sum(t.height for t in tiles)), (245, 245, 245))
        y = 0
        for t in tiles:
            sheet.paste(t, (0, y))
            y += t.height
        outputs["contact_sheet"] = str(wd.qa / "contact-sheet.png")
        sheet.save(outputs["contact_sheet"])
    if finals:
        gap = 16
        width = sum(img.width for _, img in finals) + gap * (len(finals) + 1)
        height = max(img.height for _, img in finals) + 2 * gap
        strip = Image.new("RGB", (width, height), hex_to_rgb(plan["figure"].get("background", "#FFFFFF")))
        x = gap
        for _, img in finals:
            strip.paste(img, (x, gap), img)
            x += img.width + gap
        outputs["final_size_strip"] = str(wd.qa / "final-size.png")
        outputs["final_size_dpi"] = args.preview_dpi
        strip.save(outputs["final_size_strip"])
    write_json(wd.manifest, manifest)
    write_json(wd.qa / "qa-report.json", {"elements": reports})
    summary = {s: sum(1 for r in reports if r["status"] == s) for s in ("pass", "warn", "fail")}
    return {"summary": summary, "outputs": outputs, "elements": reports,
            "review_required": "Open the contact sheet and check silhouette, edges on dark and light backgrounds, missing parts and baked-in text. Metrics cannot see those."}, (1 if summary["fail"] else 0)


# --------------------------------------------------------------------------------------------------
# place
# --------------------------------------------------------------------------------------------------
def fit_box(slot, aspect, mode, anchor="center"):
    x0, y0, x1, y1 = slot
    width, height = x1 - x0, y1 - y0
    if mode == "fill":
        return x0, y0, width, height
    scale = min(width / aspect[0], height / aspect[1])
    placed_w, placed_h = aspect[0] * scale, aspect[1] * scale
    # A standing figure keeps its feet on the slot floor, a hanging one its top edge, whatever its aspect ratio.
    top = y0 + (height - placed_h) if anchor == "bottom" else y0 if anchor == "top" else y0 + (height - placed_h) / 2
    return x0 + (width - placed_w) / 2, top, placed_w, placed_h


def command_place(args):
    wd = Workdir(args.workdir)
    plan = load_plan(args.plan or wd.plan)
    manifest = read_json(wd.manifest)
    figure = plan["figure"]
    ref = figure.get("ref_size_px")
    if not ref:
        raise AssetError("figure.ref_size_px is needed to scale slots from the approved reference")
    if args.backend == "drawio":
        canvas = parse_size(args.canvas, "--canvas") if args.canvas else tuple(ref)
    else:
        canvas = parse_size(args.canvas, "--canvas") if args.canvas else (960, 540)
    scale_x, scale_y = canvas[0] / ref[0], canvas[1] / ref[1]
    lookup = {e["id"]: e for e in plan["elements"]}
    calls, unplaced = [], []
    for entry in manifest["elements"]:
        element = lookup.get(entry["id"])
        if element is None or not element.get("slot"):
            unplaced.append({"id": entry["id"], "reason": "no slot.bbox_px in elements.json"})
            continue
        if entry.get("qa", {}).get("status") == "fail" and not args.allow_failed:
            unplaced.append({"id": entry["id"], "reason": "QA failed; fix the asset or pass --allow-failed"})
            continue
        asset_path = (wd.root / entry["file"]).resolve()
        visible = entry.get("visible_bbox_px") or [0, 0, *entry["size_px"]]
        aspect = (visible[2] - visible[0], visible[3] - visible[1])
        # Place the tight visible region inside the slot, then grow the box to include the transparent padding.
        x0, y0, x1, y1 = element["slot"]["bbox_px"]
        left, top, vis_w, vis_h = fit_box((x0 * scale_x, y0 * scale_y, x1 * scale_x, y1 * scale_y), aspect, args.fit, element["slot"].get("anchor", "center"))
        pad_scale_x, pad_scale_y = vis_w / aspect[0], vis_h / aspect[1]
        full_w, full_h = entry["size_px"][0] * pad_scale_x, entry["size_px"][1] * pad_scale_y
        full_left, full_top = left - visible[0] * pad_scale_x, top - visible[1] * pad_scale_y
        raster_reason = entry.get("raster_reason") or element.get("raster_reason") or DEFAULT_RASTER_REASON
        note = entry.get("decomposition_note") or element.get("decomposition_note") or DEFAULT_DECOMPOSITION
        alt = element.get("alt_text") or element.get("label") or element["id"]
        warnings = []
        if figure.get("width_mm"):
            placed_mm = vis_w / canvas[0] * figure["width_mm"]
            effective = (visible[2] - visible[0]) * 25.4 / placed_mm
            if effective < float(figure.get("target_dpi", 300)):
                warnings.append(f"{effective:.0f} dpi at the placed {placed_mm:.1f} mm")
        if args.backend == "drawio":
            call = {"tool": "drawio_live_add_image", "arguments": {
                "id": f"img-{element['id']}", "image_path": str(asset_path), "label": "",
                "x": round(full_left, 2), "y": round(full_top, 2), "width": round(full_w, 2), "height": round(full_h, 2),
                "raster_reason": raster_reason, "source_is_tightly_cropped": True, "atomic_raster_unit": True,
                "contains_reconstructable_content": False, "decomposition_note": note, "preserve_aspect": True}}
        else:
            call = {"tool": "powerpoint_add_image", "arguments": {
                "slide_index": args.slide_index, "image_path": str(asset_path), "name": f"img-{element['id']}",
                "left": round(full_left, 2), "top": round(full_top, 2), "width": round(full_w, 2), "height": round(full_h, 2),
                "lock_aspect_ratio": True, "alt_text": alt, "raster_reason": raster_reason, "source_is_tightly_cropped": True,
                "atomic_raster_unit": True, "contains_reconstructable_content": False, "decomposition_note": note}}
        calls.append({"element": element["id"], **call, "warnings": warnings})
    warnings = []
    ref_aspect, canvas_aspect = ref[0] / ref[1], canvas[0] / canvas[1]
    if abs(canvas_aspect / ref_aspect - 1) > 0.02:
        warnings.append(
            f"the canvas aspect {canvas_aspect:.3f} differs from the approved reference {ref_aspect:.3f}; slot positions are stretched. "
            f"Use --canvas {canvas[0]}x{round(canvas[0] / ref_aspect, 1)} (and size the slide/canvas to match) to keep the approved layout."
        )
    result = {"backend": args.backend, "canvas": list(canvas), "units": "px" if args.backend == "drawio" else "pt", "warnings": warnings, "calls": calls, "unplaced": unplaced}
    out = Path(args.out) if args.out else wd.root / f"placement.{args.backend}.json"
    write_json(out, result)
    result["file"] = str(out)
    return result


# --------------------------------------------------------------------------------------------------
# palette / init / doctor
# --------------------------------------------------------------------------------------------------
def command_palette(args):
    wd = Workdir(args.workdir)
    with Image.open(args.image) as handle:
        palette = extract_palette(handle, colors=args.colors, ignore_light=not args.keep_light)
    key = recommend_key([item["hex"] for item in palette])
    payload = {"source_image": str(Path(args.image)), "palette": palette, "recommended_key": key["key"], "key_ranking": key["ranking"]}
    write_json(Path(args.out) if args.out else wd.style, payload)
    return payload


EXAMPLE_PLAN = {
    "version": 1,
    "figure": {"id": "fig-overview", "ref_image": "approved/overview.png", "ref_size_px": [3000, 1688], "width_mm": 180, "target_dpi": 300, "background": "#FFFFFF"},
    "style": {
        "summary": "clean flat vector-style scientific illustration with soft pastel fills",
        "line": "one uniform 2px dark navy outline (#1F2937) at 1024px width",
        "shading": "flat fills, one soft shadow tone, light from the upper left",
        "palette": ["#1F2937", "#4C78A8", "#F58518", "#E5E7EB"],
        "avoid": ["photorealism", "gradients on the background", "text of any kind"],
    },
    "elements": [
        {"id": "counselor", "label": "Counselor agent", "route": "generate", "description": "a friendly rounded robot counselor seated in an armchair, holding a clipboard",
         "view": "three-quarter view facing right", "must_not_contain": ["text", "arrows"], "slot": {"bbox_px": [120, 300, 520, 760]}, "alt_text": "Counselor agent"},
        {"id": "seeker", "label": "Help-seeker", "route": "generate", "description": "a person with a thought bubble that is empty, slumped shoulders, calm expression",
         "view": "three-quarter view facing left", "slot": {"bbox_px": [900, 300, 1300, 760]}},
    ],
}


def command_init(args):
    wd = Workdir(args.workdir)
    wd.root.mkdir(parents=True, exist_ok=True)
    if wd.plan.exists() and not args.force:
        raise AssetError(f"{wd.plan} already exists; pass --force to overwrite")
    write_json(wd.plan, EXAMPLE_PLAN)
    for directory in (wd.prompts, wd.sheets, wd.assets, wd.qa):
        directory.mkdir(exist_ok=True)
    return {"workdir": str(wd.root), "created": str(wd.plan), "next": "Edit elements.json, then run: palette (optional), prompt, imagegen, cutout, split, qa, place."}


def command_doctor(_args):
    import PIL
    return {"python": sys.version.split()[0], "pillow": PIL.__version__, "numpy": np.__version__,
            "scipy": getattr(sys.modules.get("scipy"), "__version__", None) if _ndi is not None else None,
            "component_labeling": "scipy" if _ndi is not None else "pure-python fallback",
            "imagegen_script": str(IMAGEGEN), "imagegen_script_exists": IMAGEGEN.exists(), "template": str(DEFAULT_TEMPLATE), "template_exists": DEFAULT_TEMPLATE.exists()}


# --------------------------------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------------------------------
def build_parser():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    def add(name, help_text, func):
        p = sub.add_parser(name, help=help_text)
        p.add_argument("--workdir", default=".", help="Figure element folder (default: current directory)")
        p.set_defaults(func=func)
        return p

    p = add("init", "Create a workdir with an example elements.json", command_init)
    p.add_argument("--force", action="store_true")

    p = add("palette", "Extract a palette from the approved overview and recommend a key color", command_palette)
    p.add_argument("--image", required=True)
    p.add_argument("--colors", type=int, default=8)
    p.add_argument("--keep-light", action="store_true", help="Keep near-white/grey colors in the palette")
    p.add_argument("--out")

    p = add("prompt", "Write one flat-key-color element-sheet prompt per sheet", command_prompt)
    p.add_argument("--plan")
    p.add_argument("--style", help="style-lock.json (default: <workdir>/style-lock.json if present)")
    p.add_argument("--template")
    p.add_argument("--key", default="auto", help="#RRGGBB or auto (farthest from the palette)")
    p.add_argument("--per-sheet", type=int, default=6)
    p.add_argument("--canvas", help="Sheet size such as 1536x1024 (default depends on the grid)")

    p = add("cutout", "Remove the flat key background and write a transparent RGBA sheet", command_cutout)
    p.add_argument("--sheet-id")
    p.add_argument("--image")
    p.add_argument("--out")
    p.add_argument("--key", help="Force a #RRGGBB reference color. Default: measure the sheet border (recommended)")
    p.add_argument("--lo", type=float, default=28.0, help="RGB distance below which a pixel is background")
    p.add_argument("--hi", type=float, default=90.0, help="RGB distance above which a pixel is solid foreground")
    p.add_argument("--erode", type=int, default=0, help="Shrink the alpha by N px to trim a halo")
    p.add_argument("--min-island", type=int, help="Remove detached specks smaller than this many pixels")

    p = add("split", "Cut each grid cell into a tight transparent asset and update manifest.json", command_split)
    p.add_argument("--plan")
    p.add_argument("--sheet-id")
    p.add_argument("--layout")
    p.add_argument("--sheet", help="Cut-out sheet (default: sheets/<id>.rgba.png)")
    p.add_argument("--pad-px", type=int, default=12)
    p.add_argument("--box", action="append", help="Override one cell: id=x0,y0,x1,y1 in sheet pixels")

    p = add("qa", "Check alpha, clipping, key spill and effective dpi; write a contact sheet", command_qa)
    p.add_argument("--plan")
    p.add_argument("--bg", action="append", help="Extra #RRGGBB background to test on (repeatable)")
    p.add_argument("--preview-dpi", type=float, default=150.0)

    p = add("place", "Turn the manifest into drawio_live_add_image / powerpoint_add_image arguments", command_place)
    p.add_argument("--plan")
    p.add_argument("--backend", choices=["drawio", "pptx"], required=True)
    p.add_argument("--canvas", help="Target size: draw.io canvas units or slide points (pptx default 960x540)")
    p.add_argument("--slide-index", type=int, default=1)
    p.add_argument("--fit", choices=["contain", "fill"], default="contain")
    p.add_argument("--allow-failed", action="store_true")
    p.add_argument("--out")

    p = sub.add_parser("doctor", help="Report dependencies")
    p.set_defaults(func=command_doctor)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        outcome = args.func(args)
        code = 0
        if isinstance(outcome, tuple):
            outcome, code = outcome
        print(json.dumps(outcome, ensure_ascii=False, indent=2))
        return code
    except AssetError as error:
        sys.stderr.write(f"sivia_assets: {error}\n")
        return 2
    except OSError as error:
        sys.stderr.write(f"sivia_assets: {error}\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())
