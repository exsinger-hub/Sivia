"""Behavioral coverage for the template-led ImageGen prompt length gate."""

import json
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest


SCRIPT = (Path(__file__).resolve().parents[1] / "skills" /
          "design-scientific-figure" / "scripts" / "check_prompt_length.py")
compare_lengths = runpy.run_path(str(SCRIPT))["compare_lengths"]


class PromptLengthTests(unittest.TestCase):
    def test_boundary(self):
        for text, expected in [("abc", False), ("abcd", True), ("abcde", True)]:
            with self.subTest(text=text):
                self.assertEqual(compare_lengths("abcd", text)["length_pass"], expected)

    def test_whitespace_cannot_pad_length(self):
        result = compare_lengths("a b c d\r\n", "a b\t c\n\u3000")
        self.assertEqual(result["template_length"], 4)
        self.assertEqual(result["prompt_length"], 3)
        self.assertFalse(result["length_pass"])

    def test_unicode(self):
        result = compare_lengths("网格 Π", "网格\tΠ →")
        self.assertEqual(result["template_length"], 3)
        self.assertEqual(result["prompt_length"], 4)
        self.assertTrue(result["length_pass"])

    def test_empty_inputs_rejected(self):
        for template, prompt in [("", "abc"), (" \n", "abc"), ("abc", "\t")]:
            with self.subTest(template=template, prompt=prompt):
                with self.assertRaises(ValueError):
                    compare_lengths(template, prompt)

    def run_cli(self, template, prompt):
        with tempfile.TemporaryDirectory(prefix="sivia-prompt-test-") as folder:
            template_path = Path(folder) / "template.txt"
            prompt_path = Path(folder) / "prompt.txt"
            if template is not None:
                template_path.write_text(template, encoding="utf-8-sig")
            prompt_path.write_text(prompt, encoding="utf-8")
            return subprocess.run(
                [sys.executable, "-X", "utf8", str(SCRIPT),
                 "--template", str(template_path), "--prompt", str(prompt_path)],
                capture_output=True, text=True, encoding="utf-8", check=False,
            )

    def test_cli_pass_handles_utf8_bom(self):
        result = self.run_cli("网格 Π", "网格 Π")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["template_length"], 3)
        self.assertTrue(report["length_pass"])

    def test_cli_short_prompt_fails(self):
        result = self.run_cli("abcd", "abc")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertFalse(json.loads(result.stdout)["length_pass"])

    def test_cli_invalid_inputs_fail(self):
        for template, prompt in [(None, "abc"), ("\n", "abc"), ("abc", "")]:
            with self.subTest(template=template, prompt=prompt):
                result = self.run_cli(template, prompt)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
