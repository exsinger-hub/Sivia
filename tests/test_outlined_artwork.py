"""Behavioral tests for the narrowly scoped local artwork mask fallback."""

import json
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest

from PIL import Image, ImageChops, ImageDraw


SCRIPT = (Path(__file__).resolve().parents[1] / "skills" /
          "design-scientific-figure" / "scripts" / "extract_outlined_artwork.py")
outline_mask = runpy.run_path(str(SCRIPT))["outline_mask"]


def fixture():
    image = Image.new("RGB", (160, 160), (170, 170, 170))
    draw = ImageDraw.Draw(image)
    for y in range(0, 160, 8):
        for x in range(0, 160, 8):
            if (x // 8 + y // 8) % 2:
                draw.rectangle((x, y, x + 7, y + 7), fill=(220, 220, 220))
    draw.rounded_rectangle((30, 20, 130, 140), radius=20, fill="white", outline="black", width=5)
    draw.rectangle((55, 55, 105, 90), fill=(0, 180, 220))
    return image


class OutlinedArtworkTests(unittest.TestCase):
    def test_checkerboard_removed_and_light_and_colored_interior_preserved(self):
        source = fixture()
        mask = outline_mask(source)
        self.assertEqual(mask.getpixel((0, 0)), 0)
        self.assertEqual(mask.getpixel((150, 150)), 0)
        self.assertEqual(mask.getpixel((80, 40)), 255)
        self.assertEqual(mask.getpixel((80, 70)), 255)
        self.assertEqual(mask.getbbox(), (30, 20, 131, 141))

    def test_open_outline_does_not_silently_produce_a_cutout(self):
        source = Image.new("RGB", (100, 100), "white")
        ImageDraw.Draw(source).line([(20, 20), (20, 80), (80, 80), (80, 20)], fill="black", width=5)
        with self.assertRaisesRegex(ValueError, "enclosed"):
            outline_mask(source)

    def test_existing_alpha_and_canvas_edge_contact_rejected(self):
        source = fixture().convert("RGBA")
        source.putpixel((0, 0), (0, 0, 0, 0))
        with self.assertRaisesRegex(ValueError, "already has transparency"):
            outline_mask(source)
        source = fixture()
        ImageDraw.Draw(source).rectangle((0, 0, 4, 159), fill="black")
        with self.assertRaisesRegex(ValueError, "canvas edge"):
            outline_mask(source)

    def test_blank_image_and_invalid_threshold_rejected(self):
        with self.assertRaises(ValueError):
            outline_mask(Image.new("RGB", (50, 50), "white"))
        for threshold in (0, 255):
            with self.assertRaises(ValueError):
                outline_mask(fixture(), threshold)

    def run_cli(self, source, output, mask):
        return subprocess.run([sys.executable, "-B", str(SCRIPT), "--image", str(source),
                               "--output", str(output), "--mask", str(mask)],
                              capture_output=True, text=True, check=False)

    def test_cli_preserves_rgb_and_source_bytes(self):
        with tempfile.TemporaryDirectory(prefix="sivia-outline-test-") as folder:
            root = Path(folder)
            source, output, mask = root / "source.png", root / "cutout.png", root / "mask.png"
            fixture().save(source)
            before = source.read_bytes()
            result = self.run_cli(source, output, mask)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["visible_bbox_px"], [30, 20, 131, 141])
            with Image.open(source) as original, Image.open(output) as cutout, Image.open(mask) as alpha:
                self.assertEqual(cutout.mode, "RGBA")
                self.assertIsNone(ImageChops.difference(original, cutout.convert("RGB")).getbbox())
                self.assertIsNone(ImageChops.difference(cutout.getchannel("A"), alpha).getbbox())
            self.assertEqual(source.read_bytes(), before)

    def test_cli_will_not_overwrite_or_create_outputs_for_invalid_source(self):
        with tempfile.TemporaryDirectory(prefix="sivia-outline-test-") as folder:
            root = Path(folder)
            source, output, mask = root / "source.png", root / "cutout.png", root / "mask.png"
            fixture().save(source)
            before = source.read_bytes()
            self.assertEqual(self.run_cli(source, source, mask).returncode, 2)
            self.assertEqual(source.read_bytes(), before)
            self.assertFalse(mask.exists())
            Image.new("RGB", (50, 50), "white").save(source)
            self.assertEqual(self.run_cli(source, output, mask).returncode, 2)
            self.assertFalse(output.exists())
            self.assertFalse(mask.exists())


if __name__ == "__main__":
    unittest.main()
