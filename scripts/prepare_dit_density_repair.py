from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
case = ROOT / "knowledge-base" / "cases" / "dit"

directive = """FINAL DENSITY REPAIR — HIGHEST PRIORITY

Edit the supplied DiT concept figure while preserving its scientific story, labels, palette, and clean publication style. Remove the remaining lower-right empty pocket that caused the automated whitespace screen to fail by a narrow margin. Recompose existing elements only: make the bottom conditioning/support strip span nearly the full usable width, carry the existing “t + class” embeddings and their modulation connections across that strip, and extend the pale VAE/Image support field down to align with the bottom of the main DiT stack. Enlarge the existing output image and decoder carrier slightly so their combined region reaches the lower content boundary. Keep 2–4% outer margins and 1–2% internal gutters. Every large rectangle must contain a scientific element, label, or connector; no lower-right white island and no broad empty bottom band may remain. Do not add stages, metrics, claims, decorations, or source-paper pixels. The correct left-to-right flow remains noisy latent → patchify → repeated DiT blocks with timestep/class conditioning → unpatchify → VAE decoder → image. Render a single complete figure.

"""

for name in ("figure.png", "prompt.txt"):
    src = case / name
    suffix = ".png" if name.endswith(".png") else ".txt"
    stem = "figure" if name.endswith(".png") else "prompt"
    dst = case / f"{stem}.v2{suffix}"
    if not dst.exists():
        dst.write_bytes(src.read_bytes())

prompt = case / "prompt.txt"
text = prompt.read_text(encoding="utf-8")
if not text.startswith("FINAL DENSITY REPAIR"):
    prompt.write_text(directive + text, encoding="utf-8", newline="\n")

print(prompt)
print(len(prompt.read_text(encoding="utf-8")))
