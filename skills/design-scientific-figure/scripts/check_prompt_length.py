#!/usr/bin/env python3
"""Check a production prompt's non-whitespace length against its template."""

import argparse
import json
from pathlib import Path


def compare_lengths(template_text: str, prompt_text: str) -> dict:
    template_length = sum(not char.isspace() for char in template_text)
    prompt_length = sum(not char.isspace() for char in prompt_text)
    if not template_length or not prompt_length:
        raise ValueError("Template and production prompt must both be non-empty.")
    return {
        "metric": "non_whitespace_unicode_characters",
        "template_length": template_length,
        "prompt_length": prompt_length,
        "ratio": prompt_length / template_length,
        "length_pass": prompt_length >= template_length,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--template", type=Path, required=True)
    parser.add_argument("--prompt", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = compare_lengths(
            args.template.read_text(encoding="utf-8-sig"),
            args.prompt.read_text(encoding="utf-8-sig"),
        )
    except (OSError, UnicodeError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps({
        "template": str(args.template.resolve()),
        "prompt": str(args.prompt.resolve()),
        **result,
    }, ensure_ascii=False, indent=2))
    return 0 if result["length_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
