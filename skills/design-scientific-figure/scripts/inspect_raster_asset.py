#!/usr/bin/env python3
"""Read-only retained-pixel/placement estimate. Requires Pillow; never resamples."""

import argparse
import json
import math
from pathlib import Path
import sys

from PIL import Image


def placement_report(size_px, width_mm, height_mm=None, crop_px=None, target_dpi=300):
    """Use stored raster coordinates; ignore embedded DPI metadata."""
    for name, value in (("width_mm", width_mm), ("target_dpi", target_dpi)):
        if not math.isfinite(value) or value <= 0:
            raise ValueError(f"{name} must be finite and positive")
    if height_mm is not None and (not math.isfinite(height_mm) or height_mm <= 0):
        raise ValueError("height_mm must be finite and positive")
    width_px, height_px = size_px
    if width_px <= 0 or height_px <= 0:
        raise ValueError("image dimensions must be positive")
    crop = tuple(crop_px) if crop_px is not None else (0, 0, width_px, height_px)
    if len(crop) != 4 or any(not isinstance(value, int) for value in crop):
        raise ValueError("crop_px requires four integer pixel edges")
    left, top, right, bottom = crop
    if not (0 <= left < right <= width_px and 0 <= top < bottom <= height_px):
        raise ValueError("crop must have positive area and stay inside the image")
    retained_width, retained_height = right - left, bottom - top
    if height_mm is None:
        height_mm = width_mm * retained_height / retained_width
    required = [math.ceil(mm * target_dpi / 25.4) for mm in (width_mm, height_mm)]
    effective = [retained_width * 25.4 / width_mm, retained_height * 25.4 / height_mm]
    return {
        "source_size_px": [width_px, height_px],
        "crop_px": list(crop),
        "retained_size_px": [retained_width, retained_height],
        "placement_mm": [width_mm, height_mm],
        "effective_dpi_xy": effective,
        "target_dpi": target_dpi,
        "required_size_px": required,
        "sampling_sufficient": retained_width >= required[0] and retained_height >= required[1],
        "display_aspect_ratio_relative_to_pixels": (width_mm / height_mm) / (retained_width / retained_height),
        "assessment_scope": "Sampling only, not visual quality or scientific authenticity; no file changed.",
    }


def alpha_report(source, crop_px):
    """Check actual alpha inside the retained crop; coordinates stay source-relative."""
    alpha = source.convert("RGBA").getchannel("A").crop(crop_px)
    minimum, maximum = alpha.getextrema()
    bounds = alpha.getbbox()
    left, top, _, _ = crop_px
    if bounds is not None:
        bounds = [bounds[0] + left, bounds[1] + top, bounds[2] + left, bounds[3] + top]
    return {
        "alpha_extrema": [minimum, maximum],
        "visible_bbox_px": bounds,
        "pixel_requirement_pass": minimum == 0 and maximum > 0,
        "assessment_scope": "Requires both fully transparent and visible pixels in the crop; not a cutout-edge or background-quality verdict.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", required=True, type=Path)
    parser.add_argument("--width-mm", required=True, type=float)
    parser.add_argument("--height-mm", type=float, help="Default: preserve the retained pixel aspect ratio")
    parser.add_argument("--crop-px", type=int, nargs=4, metavar=("LEFT", "TOP", "RIGHT", "BOTTOM"))
    parser.add_argument("--target-dpi", type=float, default=300, help="Working sampling target, not a journal rule")
    parser.add_argument("--require-transparent", action="store_true", help="Read alpha and exit 1 if the retained crop lacks transparent or visible pixels")
    args = parser.parse_args()
    try:
        with Image.open(args.image) as source:
            report = placement_report(source.size, args.width_mm, args.height_mm, args.crop_px, args.target_dpi)
            if args.require_transparent:
                report["alpha_check"] = alpha_report(source, report["crop_px"])
        report["image"] = str(args.image.resolve())
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.require_transparent and not report["alpha_check"]["pixel_requirement_pass"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
