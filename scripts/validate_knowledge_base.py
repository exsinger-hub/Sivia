#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / "knowledge-base"
index = json.loads((KB / "index.json").read_text(encoding="utf-8"))
errors = []

if index["total_pairs"] != 42:
    errors.append(f"expected 42 pairs, found {index['total_pairs']}")
if index["paper_sourced_pairs"] != 36 or index["new_pairs"] != 24:
    errors.append("paper-sourced/new counts do not equal 36/24")
ids = [x["id"] for x in index["records"]]
if len(ids) != len(set(ids)):
    errors.append("duplicate case ids")
if sum(x["count"] for x in index["categories"]) != 42:
    errors.append("category counts do not sum to 42")

for row in index["records"]:
    prompt = KB / row["prompt"]
    image = KB / row["image"]
    readme = KB / row["readme"]
    for path in (prompt, image, readme):
        if not path.is_file():
            errors.append(f"missing {path.relative_to(ROOT)}")
    if not prompt.is_file() or not image.is_file():
        continue
    prompt_bytes = prompt.read_bytes()
    image_bytes = image.read_bytes()
    if image_bytes[:8] != b"\x89PNG\r\n\x1a\n":
        errors.append(f"invalid PNG signature: {row['id']}")
    if hashlib.sha256(prompt_bytes).hexdigest() != row["prompt_sha256"]:
        errors.append(f"prompt hash mismatch: {row['id']}")
    if hashlib.sha256(image_bytes).hexdigest() != row["image_sha256"]:
        errors.append(f"image hash mismatch: {row['id']}")
    if not row["density"]["density_screen_pass"]:
        errors.append(f"density gate failed: {row['id']}")
    text = prompt.read_text(encoding="utf-8")
    if row["tier"].startswith("paper-sourced") and sum(not c.isspace() for c in text) < 15356:
        errors.append(f"paper-sourced prompt below length floor: {row['id']}")
    if row["tier"] == "paper-sourced-new" and ("[" in text and "]" in text and "[TITLE]" in text):
        errors.append(f"unresolved template placeholder: {row['id']}")

for name in ("README.md", "README_ZH.md", "knowledge-base/README.md"):
    text = (ROOT / name).read_text(encoding="utf-8")
    if "42" not in text or "36" not in text or "24" not in text:
        errors.append(f"count summary missing from {name}")

if errors:
    print("\n".join(errors))
    raise SystemExit(1)
print(json.dumps({"valid": True, "pairs": 42, "paper_sourced": 36, "new": 24, "density_pass": 42}, ensure_ascii=False))
