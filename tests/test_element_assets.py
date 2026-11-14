import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "generate-figure-elements" / "scripts" / "sivia_assets.py"
spec = importlib.util.spec_from_file_location("sivia_assets", SCRIPT)
assets = importlib.util.module_from_spec(spec)
spec.loader.exec_module(assets)

KEY = (0, 255, 0)
NAVY = (31, 41, 80)
ORANGE = (245, 133, 24)


def run(*argv):
    """Run the CLI in-process and return (exit code, parsed JSON)."""
    out = io.StringIO()
    err = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = assets.main([str(a) for a in argv])
    text = out.getvalue().strip()
    return code, (json.loads(text) if text else None), err.getvalue()


def painted_sheet(size, grid, shapes, noise=2.0, seed=7, bg=KEY):
    """Key-colored sheet with anti-aliased navy/orange blobs, one per cell (supersampled edges)."""
    scale = 4
    big = Image.new("RGB", (size[0] * scale, size[1] * scale), bg)
    draw = ImageDraw.Draw(big)
    cols, rows = grid
    cw, ch = size[0] / cols, size[1] / rows
    for index, kind in enumerate(shapes):
        row, col = divmod(index, cols)
        cx, cy = (col + 0.5) * cw * scale, (row + 0.5) * ch * scale
        half = min(cw, ch) * scale * 0.3
        box = [cx - half, cy - half, cx + half, cy + half]
        if kind == "ellipse":
            draw.ellipse(box, fill=ORANGE, outline=NAVY, width=3 * scale)
        elif kind == "rect":
            draw.rectangle(box, fill=NAVY)
        elif kind == "bleed":  # crosses the cell border
            draw.ellipse([cx - cw * scale * 0.7, cy - half, cx + cw * scale * 0.7, cy + half], fill=ORANGE, outline=NAVY, width=3 * scale)
    image = big.resize(size, Image.Resampling.LANCZOS)
    arr = np.asarray(image).astype(np.float32)
    rng = np.random.default_rng(seed)
    arr += rng.normal(0, noise, arr.shape)
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")


class ChromaCutoutTests(unittest.TestCase):
    def setUp(self):
        self.image = painted_sheet((600, 400), (1, 1), ["ellipse"])
        self.rgb = np.asarray(self.image)

    def test_background_becomes_transparent_and_subject_stays_opaque(self):
        rgba, stats = assets.chroma_cutout(self.rgb, KEY)
        alpha = rgba[..., 3]
        self.assertEqual(int(alpha[5, 5]), 0)
        self.assertEqual(int(alpha[200, 300]), 255)
        self.assertGreater(stats["partial_fraction"], 0.0005, "anti-aliased edge keeps soft alpha")
        self.assertLess(stats["partial_fraction"], 0.05)

    def test_edges_carry_no_key_color(self):
        rgba, _ = assets.chroma_cutout(self.rgb, KEY)
        alpha = rgba[..., 3]
        edge = (alpha > 8) & (alpha < 248)
        self.assertTrue(edge.any())
        distance = np.linalg.norm(rgba[..., :3].astype(np.float32) - np.array(KEY, np.float32), axis=-1)
        self.assertLess(float((distance[edge] < 90).mean()), 0.02)
        # A naive threshold would leave a green halo; compare against the source edge to prove the point.
        naive_edge = np.linalg.norm(self.rgb.astype(np.float32) - np.array(KEY, np.float32), axis=-1)
        self.assertGreater(float(((naive_edge > 28) & (naive_edge < 90)).sum()), 0)

    def test_noise_in_the_background_does_not_leave_specks(self):
        noisy = painted_sheet((600, 400), (1, 1), ["ellipse"], noise=6.0, seed=3)
        rgba, stats = assets.chroma_cutout(np.asarray(noisy), KEY)
        _, areas = assets.component_areas(rgba[..., 3] > 127)
        self.assertEqual(len(areas), 1)

    def test_small_detached_specks_are_removed(self):
        rgb = self.rgb.copy()
        rgb[20:24, 20:24] = NAVY  # a 16 px speck
        rgba, stats = assets.chroma_cutout(rgb, KEY, min_island=40)
        self.assertEqual(int(rgba[22, 22, 3]), 0)
        self.assertGreaterEqual(stats["removed_specks"], 1)

    def test_invalid_thresholds_are_rejected(self):
        with self.assertRaises(assets.AssetError):
            assets.chroma_cutout(self.rgb, KEY, lo=100, hi=50)


class PaletteTests(unittest.TestCase):
    def test_key_avoids_the_palette(self):
        self.assertNotEqual(assets.recommend_key(["#00B050", "#2E8B57"])["key"], "#00FF00")
        ranked = assets.recommend_key(["#1F2937", "#4C78A8", "#F58518"])
        self.assertIn(ranked["key"], assets.KEY_CANDIDATES)
        self.assertEqual(ranked["min_distance"], max(item["min_distance"] for item in ranked["ranking"]))
        self.assertGreaterEqual(ranked["min_distance"], 150, "the key must sit far from every palette color")

    def test_palette_ignores_the_white_page(self):
        image = Image.new("RGB", (200, 200), (255, 255, 255))
        ImageDraw.Draw(image).rectangle([50, 50, 150, 150], fill=(76, 120, 168))
        palette = assets.extract_palette(image, colors=4)
        self.assertTrue(palette)
        self.assertNotIn("#FFFFFF", [item["hex"] for item in palette])


class PlanTests(unittest.TestCase):
    def write(self, plan):
        folder = tempfile.mkdtemp()
        path = Path(folder) / "elements.json"
        path.write_text(json.dumps(plan))
        return path

    def test_rejects_duplicate_ids_and_bad_routes(self):
        base = {"elements": [{"id": "a", "description": "x"}, {"id": "a", "description": "y"}]}
        with self.assertRaises(assets.AssetError):
            assets.load_plan(self.write(base))
        with self.assertRaises(assets.AssetError):
            assets.load_plan(self.write({"elements": [{"id": "a", "route": "magic", "description": "x"}]}))
        with self.assertRaises(assets.AssetError):
            assets.load_plan(self.write({"elements": [{"id": "A b", "description": "x"}]}))
        with self.assertRaises(assets.AssetError):
            assets.load_plan(self.write({"elements": [{"id": "a"}]}))

    def test_slot_anchor_is_validated(self):
        with self.assertRaises(assets.AssetError):
            assets.load_plan(self.write({"elements": [{"id": "a", "description": "x", "slot": {"bbox_px": [0, 0, 10, 10], "anchor": "middle"}}]}))

    def test_anchor_keeps_a_standing_figure_on_the_slot_floor(self):
        slot = (100, 100, 300, 500)  # 200 x 400
        aspect = (100, 100)           # a square subject is limited by the width: 200 x 200
        self.assertEqual(assets.fit_box(slot, aspect, "contain")[1], 200)                    # centred
        self.assertEqual(assets.fit_box(slot, aspect, "contain", "bottom")[1], 300)          # feet on y=500
        self.assertEqual(assets.fit_box(slot, aspect, "contain", "top")[1], 100)
        self.assertEqual(assets.fit_box(slot, aspect, "contain", "bottom")[1] + 200, 500)

    def test_slot_must_be_a_real_box(self):
        with self.assertRaises(assets.AssetError):
            assets.load_plan(self.write({"elements": [{"id": "a", "description": "x", "slot": {"bbox_px": [10, 10, 5, 50]}}]}))

    def test_placed_width_comes_from_the_slot_and_figure_width(self):
        plan = {"figure": {"ref_size_px": [3000, 1500], "width_mm": 180}, "elements": []}
        element = {"slot": {"bbox_px": [0, 0, 500, 500]}}
        self.assertAlmostEqual(assets.placed_width_mm(plan, element), 30.0)
        self.assertEqual(assets.required_pixels(30, 300), 355)


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.wd = Path(self.tmp.name)
        plan = {
            "figure": {"id": "demo", "ref_size_px": [3000, 1500], "width_mm": 180, "target_dpi": 300, "background": "#FFFFFF"},
            "style": {"summary": "flat vector illustration", "palette": ["#1F2937", "#F58518"], "line": "uniform navy outline"},
            "elements": [
                {"id": "counselor", "label": "Counselor", "description": "round robot", "view": "front", "slot": {"bbox_px": [100, 200, 600, 700]}},
                {"id": "seeker", "label": "Seeker", "description": "seated person", "must_not_contain": ["text"], "slot": {"bbox_px": [900, 200, 1400, 700]}},
                {"id": "memory", "label": "Memory", "description": "stack of cards", "slot": {"bbox_px": [1700, 200, 2200, 700]}},
                {"id": "native-box", "route": "native"},
            ],
        }
        (self.wd / "elements.json").write_text(json.dumps(plan))

    def make_sheet(self, shapes):
        layout = json.loads((self.wd / "prompts" / "sheet-01.layout.json").read_text())
        image = painted_sheet(tuple(layout["canvas_px"]), tuple(layout["grid"]), shapes)
        (self.wd / "sheets").mkdir(exist_ok=True)
        image.save(self.wd / "sheets" / "sheet-01.png")

    def test_prompt_is_complete_and_layout_matches(self):
        code, out, _ = run("prompt", "--workdir", self.wd, "--canvas", "1536x1024", "--key", "#00FF00")
        self.assertEqual(code, 0)
        sheet = out["sheets"][0]
        self.assertEqual(sheet["grid"], [3, 1])
        self.assertEqual(sheet["order"], ["counselor", "seeker", "memory"])
        text = (self.wd / sheet["prompt_file"]).read_text(encoding="utf-8")
        self.assertNotIn("{{", text)
        for needle in ["#00FF00", "1536x1024", "3 columns by 1 rows", "[row 1, column 2] Seeker", "uniform navy outline", "Must not contain: text", "No text, letters"]:
            self.assertIn(needle, text)
        self.assertEqual(sheet["warnings"], [], "a 512 px cell still gives ~358 subject px, enough for 30 mm at 300 dpi")

    def test_prompt_warns_when_cells_are_too_small_for_the_target_dpi(self):
        code, out, _ = run("prompt", "--workdir", self.wd, "--canvas", "768x256")
        self.assertEqual(code, 0)
        self.assertTrue(out["sheets"][0]["warnings"])

    def test_two_empty_cells_are_declared_empty(self):
        plan = json.loads((self.wd / "elements.json").read_text())
        plan["elements"] = plan["elements"][:2] + [{"id": "a", "description": "x"}, {"id": "b", "description": "y"}, {"id": "c", "description": "z"}]
        (self.wd / "elements.json").write_text(json.dumps(plan))
        code, out, _ = run("prompt", "--workdir", self.wd)
        text = (self.wd / out["sheets"][0]["prompt_file"]).read_text(encoding="utf-8")
        self.assertEqual(out["sheets"][0]["grid"], [3, 2])
        self.assertIn("Leave these cells completely empty", text)

    def test_solo_and_explicit_sheets(self):
        plan = json.loads((self.wd / "elements.json").read_text())
        plan["elements"][0]["sheet"] = "solo"
        (self.wd / "elements.json").write_text(json.dumps(plan))
        code, out, _ = run("prompt", "--workdir", self.wd)
        ids = [s["sheet_id"] for s in out["sheets"]]
        self.assertIn("solo-counselor", ids)
        self.assertIn("sheet-01", ids)

    def test_full_chain_cutout_split_qa_place(self):
        run("prompt", "--workdir", self.wd, "--canvas", "1536x1024", "--key", "#00FF00")
        self.make_sheet(["ellipse", "rect", "ellipse"])
        code, cut, _ = run("cutout", "--workdir", self.wd, "--sheet-id", "sheet-01")
        self.assertEqual(code, 0)
        self.assertEqual(cut["key_requested"], "#00FF00")
        self.assertLess(cut["transparent_fraction"], 1.0)
        code, split, _ = run("split", "--workdir", self.wd, "--sheet-id", "sheet-01")
        self.assertEqual(code, 0)
        self.assertEqual([e["status"] for e in split["elements"]], ["ok", "ok", "ok"])
        for element_id in ("counselor", "seeker", "memory"):
            with Image.open(self.wd / "assets" / f"{element_id}.png") as asset:
                self.assertEqual(asset.mode, "RGBA")
                self.assertEqual(asset.getchannel("A").getextrema()[0], 0)

        code, qa, _ = run("qa", "--workdir", self.wd)
        self.assertEqual(code, 0, qa)
        self.assertEqual(qa["summary"]["fail"], 0)
        self.assertTrue(Path(qa["outputs"]["contact_sheet"]).exists())
        self.assertTrue(Path(qa["outputs"]["final_size_strip"]).exists())

        code, drawio, _ = run("place", "--workdir", self.wd, "--backend", "drawio")
        self.assertEqual(code, 0)
        self.assertEqual([c["element"] for c in drawio["calls"]], ["counselor", "seeker", "memory"])
        args = drawio["calls"][0]["arguments"]
        self.assertEqual(drawio["calls"][0]["tool"], "drawio_live_add_image")
        self.assertTrue(args["atomic_raster_unit"] and not args["contains_reconstructable_content"])
        self.assertTrue(Path(args["image_path"]).is_absolute() and Path(args["image_path"]).exists())
        self.assertGreater(args["width"], 0)
        # The visible subject is centred inside its 500x500 slot even though the file has transparent padding.
        manifest = json.loads((self.wd / "manifest.json").read_text())
        entry = manifest["elements"][0]
        scale = args["width"] / entry["size_px"][0]
        vis = entry["visible_bbox_px"]
        centre_x = args["x"] + (vis[0] + vis[2]) / 2 * scale
        self.assertAlmostEqual(centre_x, (100 + 600) / 2, delta=2)

        code, ppt, _ = run("place", "--workdir", self.wd, "--backend", "pptx", "--slide-index", 3)
        self.assertEqual(ppt["canvas"], [960, 540])
        self.assertEqual(ppt["calls"][1]["arguments"]["slide_index"], 3)
        self.assertEqual(ppt["calls"][1]["tool"], "powerpoint_add_image")
        # 3000 px reference -> 960 pt slide: the 500 px slot is 160 pt wide and the subject stays centred in it.
        first = ppt["calls"][0]["arguments"]
        entry = json.loads((self.wd / "manifest.json").read_text())["elements"][0]
        ratio = first["width"] / entry["size_px"][0]
        centre = first["left"] + (entry["visible_bbox_px"][0] + entry["visible_bbox_px"][2]) / 2 * ratio
        self.assertAlmostEqual(centre, (100 + 600) / 2 * 0.32, delta=1)

    def test_real_generator_artifacts_do_not_break_the_cell_bbox(self):
        # Observed with a real model: #00FF00 arrives as ~#07F600, and a few edge pixels drift into the transition band.
        run("prompt", "--workdir", self.wd, "--canvas", "1536x1024", "--key", "#00FF00")
        layout = json.loads((self.wd / "prompts" / "sheet-01.layout.json").read_text())
        image = painted_sheet(tuple(layout["canvas_px"]), tuple(layout["grid"]), ["ellipse", "rect", "ellipse"], bg=(7, 246, 0))
        arr = np.asarray(image).copy()
        arr[0, 0] = (30, 235, 20)
        arr[1023, 1535] = (28, 236, 18)
        arr[512, 700] = (25, 238, 15)
        (self.wd / "sheets").mkdir(exist_ok=True)
        Image.fromarray(arr).save(self.wd / "sheets" / "sheet-01.png")
        code, cut, _ = run("cutout", "--workdir", self.wd, "--sheet-id", "sheet-01")
        self.assertEqual(cut["key_requested"], "#00FF00")
        self.assertEqual(cut["key_source"], "measured border")
        used = np.array(assets.hex_to_rgb(cut["key_used"]), dtype=float)
        self.assertLess(float(np.linalg.norm(used - np.array([7, 246, 0]))), 5, "the painted color, not the requested one, is the reference")
        self.assertGreaterEqual(cut["removed_specks"], 1)
        code, split, _ = run("split", "--workdir", self.wd, "--sheet-id", "sheet-01")
        self.assertEqual([e["status"] for e in split["elements"]], ["ok", "ok", "ok"], split)
        first = split["elements"][0]["visible_px"]
        self.assertLess(first[0], 0.7 * 512, "stray corner pixels would inflate the box to the whole 512 px cell")

    def test_a_forced_key_is_used_as_given(self):
        run("prompt", "--workdir", self.wd, "--canvas", "1536x1024", "--key", "#00FF00")
        self.make_sheet(["ellipse", "rect", "ellipse"])
        code, cut, _ = run("cutout", "--workdir", self.wd, "--sheet-id", "sheet-01", "--key", "#00FF00")
        self.assertEqual(cut["key_source"], "forced")
        self.assertEqual(cut["key_used"], "#00FF00")

    def test_place_honours_the_bottom_anchor(self):
        plan = json.loads((self.wd / "elements.json").read_text())
        for element in plan["elements"][:3]:
            element["slot"]["anchor"] = "bottom"
            element["slot"]["bbox_px"] = [element["slot"]["bbox_px"][0], 100, element["slot"]["bbox_px"][2], 900]  # much taller than the art
        (self.wd / "elements.json").write_text(json.dumps(plan))
        run("prompt", "--workdir", self.wd, "--canvas", "1536x1024", "--key", "#00FF00")
        self.make_sheet(["ellipse", "rect", "ellipse"])
        run("cutout", "--workdir", self.wd, "--sheet-id", "sheet-01")
        run("split", "--workdir", self.wd, "--sheet-id", "sheet-01")
        code, placed, _ = run("place", "--workdir", self.wd, "--backend", "drawio")
        manifest = {e["id"]: e for e in json.loads((self.wd / "manifest.json").read_text())["elements"]}
        for call in placed["calls"][:3]:
            arguments, entry = call["arguments"], manifest[call["element"]]
            scale = arguments["height"] / entry["size_px"][1]
            visible_bottom = arguments["y"] + entry["visible_bbox_px"][3] * scale
            self.assertAlmostEqual(visible_bottom, 900 * placed["canvas"][1] / 1500, delta=1.5, msg=call["element"])

    def test_a_clipped_element_fails_the_split_and_qa(self):
        run("prompt", "--workdir", self.wd, "--canvas", "1536x1024", "--key", "#00FF00")
        self.make_sheet(["ellipse", "bleed", "ellipse"])
        run("cutout", "--workdir", self.wd, "--sheet-id", "sheet-01")
        code, split, _ = run("split", "--workdir", self.wd, "--sheet-id", "sheet-01")
        statuses = {e["id"]: e["status"] for e in split["elements"]}
        self.assertEqual(statuses["seeker"], "fail")
        self.assertIn("touches its cell border", split["elements"][1]["problems"][0])

    def test_qa_rejects_an_opaque_asset_and_place_skips_failures(self):
        run("prompt", "--workdir", self.wd, "--canvas", "1536x1024", "--key", "#00FF00")
        self.make_sheet(["ellipse", "rect", "ellipse"])
        run("cutout", "--workdir", self.wd, "--sheet-id", "sheet-01")
        run("split", "--workdir", self.wd, "--sheet-id", "sheet-01")
        Image.new("RGB", (200, 200), (10, 10, 10)).save(self.wd / "assets" / "memory.png")  # no alpha at all
        code, qa, _ = run("qa", "--workdir", self.wd)
        self.assertEqual(code, 1)
        bad = next(e for e in qa["elements"] if e["id"] == "memory")
        self.assertEqual(bad["status"], "fail")
        self.assertTrue(any("transparency" in p for p in bad["problems"]))
        code, placed, _ = run("place", "--workdir", self.wd, "--backend", "drawio")
        self.assertEqual([u["id"] for u in placed["unplaced"]], ["memory"])

    def test_low_resolution_is_reported_against_the_physical_size(self):
        run("prompt", "--workdir", self.wd, "--canvas", "1536x1024", "--key", "#00FF00")
        self.make_sheet(["ellipse", "rect", "ellipse"])
        run("cutout", "--workdir", self.wd, "--sheet-id", "sheet-01")
        run("split", "--workdir", self.wd, "--sheet-id", "sheet-01")
        plan = json.loads((self.wd / "elements.json").read_text())
        plan["elements"][0]["width_mm"] = 120  # far larger than the pixels allow
        (self.wd / "elements.json").write_text(json.dumps(plan))
        code, qa, _ = run("qa", "--workdir", self.wd)
        self.assertEqual(code, 1)
        first = qa["elements"][0]
        self.assertLess(first["effective_dpi"], 150)
        self.assertIn("dpi", " ".join(first["problems"]))

    def test_split_requires_the_cutout_first(self):
        run("prompt", "--workdir", self.wd)
        code, _, err = run("split", "--workdir", self.wd, "--sheet-id", "sheet-01")
        self.assertEqual(code, 2)
        self.assertIn("run cutout first", err)

    def test_init_creates_a_valid_example_plan(self):
        fresh = Path(self.tmp.name) / "fresh"
        code, out, _ = run("init", "--workdir", fresh)
        self.assertEqual(code, 0)
        assets.load_plan(fresh / "elements.json")
        code, _, err = run("init", "--workdir", fresh)
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
