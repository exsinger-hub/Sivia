"""Exercise crop, placement and read-only behavior without a presentation app."""

import json
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest

from PIL import Image


SCRIPT = (Path(__file__).resolve().parents[1] / "skills" /
          "design-scientific-figure" / "scripts" / "inspect_raster_asset.py")
placement_report = runpy.run_path(str(SCRIPT))["placement_report"]


class RasterAssetTests(unittest.TestCase):
    def test_small_crop_does_not_inherit_overview_resolution(self):
        full = placement_report((1600, 1000), 30)
        crop = placement_report((1600, 1000), 30, crop_px=(100, 100, 180, 180))
        self.assertTrue(full["sampling_sufficient"])
        self.assertFalse(crop["sampling_sufficient"])
        self.assertEqual(crop["retained_size_px"], [80, 80])
        self.assertAlmostEqual(crop["effective_dpi_xy"][0], 67.7333333333)
        self.assertEqual(crop["required_size_px"], [355, 355])

    def test_ceil_boundary_and_user_target(self):
        self.assertFalse(placement_report((354, 354), 30)["sampling_sufficient"])
        self.assertTrue(placement_report((355, 355), 30)["sampling_sufficient"])
        self.assertEqual(placement_report((600, 600), 25.4, target_dpi=600)["required_size_px"], [600, 600])

    def test_default_height_preserves_crop_not_full_image_aspect(self):
        report = placement_report((1000, 1000), 40, crop_px=(50, 50, 450, 250))
        self.assertEqual(report["placement_mm"], [40, 20])
        self.assertEqual(report["display_aspect_ratio_relative_to_pixels"], 1)
        self.assertEqual(report["effective_dpi_xy"][0], report["effective_dpi_xy"][1])

    def test_stretched_placement_reports_both_axes(self):
        report = placement_report((400, 200), 25.4, height_mm=25.4)
        self.assertEqual(report["effective_dpi_xy"], [400, 200])
        self.assertEqual(report["display_aspect_ratio_relative_to_pixels"], 0.5)
        self.assertFalse(report["sampling_sufficient"])

    def test_invalid_crop_rejected(self):
        for crop in [(0, 0, 101, 100), (-1, 0, 90, 90), (1, 1, 1, 90),
                     (0, 30, 40, 20), (0, 0, 50), (0, 0, 10.5, 20)]:
            with self.subTest(crop=crop), self.assertRaises(ValueError):
                placement_report((100, 100), 30, crop_px=crop)

    def test_invalid_placement_rejected(self):
        for key in ("width_mm", "height_mm", "target_dpi"):
            for value in (0, -1, float("nan"), float("inf")):
                args = {"width_mm": 30, key: value}
                with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                    placement_report((100, 100), **args)

    def cli(self, image, *args):
        return subprocess.run(
            [sys.executable, "-X", "utf8", str(SCRIPT), "--image", str(image), "--width-mm", "30", *args],
            capture_output=True, text=True, encoding="utf-8", check=False,
        )

    def test_cli_ignores_dpi_metadata_and_does_not_change_source(self):
        with tempfile.TemporaryDirectory(prefix="sivia-raster-test-") as folder:
            reports = []
            for dpi in (72, 1200):
                source = Path(folder) / f"asset-{dpi}.png"
                Image.new("RGBA", (800, 500), (80, 100, 120, 255)).save(source, dpi=(dpi, dpi))
                original_bytes = source.read_bytes()
                result = self.cli(source, "--crop-px", "50", "20", "130", "100")
                self.assertEqual(result.returncode, 0, result.stderr)
                reports.append(json.loads(result.stdout))
                self.assertEqual(source.read_bytes(), original_bytes)
            self.assertEqual(reports[0]["effective_dpi_xy"], reports[1]["effective_dpi_xy"])
            self.assertFalse(reports[0]["sampling_sufficient"])

    def test_cli_invalid_file_or_crop_has_no_success_report(self):
        with tempfile.TemporaryDirectory(prefix="sivia-raster-test-") as folder:
            source = Path(folder) / "asset.png"
            Image.new("RGB", (100, 100)).save(source)
            for path, args in [(Path(folder) / "missing.png", ()), (source, ("--crop-px", "0", "0", "101", "100"))]:
                result = self.cli(path, *args)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")

    def test_transparent_requirement_rejects_an_opaque_high_resolution_picture(self):
        with tempfile.TemporaryDirectory(prefix="sivia-raster-test-") as folder:
            source = Path(folder) / "opaque.png"
            Image.new("RGB", (800, 800), "white").save(source)
            result = self.cli(source, "--require-transparent")
            self.assertEqual(result.returncode, 1, result.stderr)
            report = json.loads(result.stdout)
            self.assertTrue(report["sampling_sufficient"])
            self.assertFalse(report["alpha_check"]["pixel_requirement_pass"])

    def test_transparent_requirement_measures_subject_bounds_without_writing(self):
        with tempfile.TemporaryDirectory(prefix="sivia-raster-test-") as folder:
            source = Path(folder) / "cutout.png"
            fixture = Image.new("RGBA", (800, 800), (0, 0, 0, 0))
            fixture.paste((255, 255, 255, 255), (100, 150, 650, 700))
            fixture.save(source)
            original_bytes = source.read_bytes()
            result = self.cli(source, "--require-transparent", "--crop-px", "50", "50", "750", "750")
            self.assertEqual(result.returncode, 0, result.stderr)
            alpha = json.loads(result.stdout)["alpha_check"]
            self.assertEqual(alpha["visible_bbox_px"], [100, 150, 650, 700])
            self.assertTrue(alpha["pixel_requirement_pass"])
            self.assertEqual(source.read_bytes(), original_bytes)

    def test_alpha_channel_alone_or_blank_canvas_is_not_a_valid_cutout(self):
        with tempfile.TemporaryDirectory(prefix="sivia-raster-test-") as folder:
            for opacity in (0, 255):
                source = Path(folder) / f"alpha-{opacity}.png"
                Image.new("RGBA", (800, 800), (255, 255, 255, opacity)).save(source)
                result = self.cli(source, "--require-transparent")
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertFalse(json.loads(result.stdout)["alpha_check"]["pixel_requirement_pass"])

    def test_transparency_is_checked_inside_the_selected_crop(self):
        with tempfile.TemporaryDirectory(prefix="sivia-raster-test-") as folder:
            source = Path(folder) / "crop.png"
            fixture = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
            fixture.paste((255, 255, 255, 255), (20, 20, 80, 80))
            fixture.save(source)
            result = self.cli(source, "--require-transparent", "--crop-px", "20", "20", "80", "80")
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertFalse(json.loads(result.stdout)["alpha_check"]["pixel_requirement_pass"])


if __name__ == "__main__":
    unittest.main()
