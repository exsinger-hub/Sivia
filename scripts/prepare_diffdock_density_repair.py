from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
case = ROOT / "knowledge-base" / "cases" / "diffdock"
directive = """FINAL DENSITY REPAIR — HIGHEST PRIORITY

Edit the supplied DiffDock conceptual figure while preserving every scientific relation, label, molecule identity, pose ordering, training-only boundary, palette, and publication style. The current figure is already scientifically dense, but its meaningful-content grid misses the admission floor by less than one percentage point. Recompose existing content only: enlarge the translate/rotate/twist examples, the central protein-pose sequence, and the right training panels into nearby white pockets; tighten vertical and horizontal gutters; let pale bounded panel fields extend behind each existing scientific group; and align the lowest ranked-pose cards and confidence path close to the bottom content boundary. Keep 2–3% outer margins and 1–2% internal gutters. No broad blank band, isolated white island, or unused corner may remain. Do not add stages, molecules, metrics, claims, decorations, or source-paper pixels. Keep the conceptual-illustration marker and render one complete figure.

"""
for name in ("figure.png", "prompt.txt"):
    src=case/name
    ext=src.suffix
    dst=case/f"{src.stem}.v3{ext}"
    if not dst.exists(): dst.write_bytes(src.read_bytes())
prompt=case/"prompt.txt"
text=prompt.read_text(encoding="utf-8")
if not text.startswith("FINAL DENSITY REPAIR"):
    prompt.write_text(directive+text,encoding="utf-8",newline="\n")
print(len(prompt.read_text(encoding="utf-8")))
