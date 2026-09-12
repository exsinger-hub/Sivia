#!/usr/bin/env python3
"""Prepare a second, stronger density repair for the eight remaining drafts."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TARGETS=['blip2','instructblip','flamingo','controlnet','dit','dreambooth','tube-link','diffusion-policy']
REPAIR="""FINAL CANVAS-OCCUPANCY REPAIR — APPLY TO THE ATTACHED CURRENT IMAGE.
Retain the current scientific topology, all seven named stages, every arrow direction, the same miniature examples, and the same concise labels. Rebuild only the panel geometry and local scaling. Use the native 3:2 landscape canvas as a nearly edge-to-edge scientific plate: put the title inside a shallow header embedded in the panel system; start the colored panel backgrounds at y=3% and end them at y=97%; start the first panel at x=1.5% and end the last at x=98.5%. Stretch every existing panel to this height and enlarge its internal objects to use the new area. When the current figure has a support strip or return loop, integrate it inside the full-height panel hull rather than leaving a white lower band. Every column must contain either a large representation, a concrete scene, or a necessary multi-step mechanism. Use pale tinted panel backgrounds so occupied scientific regions are visibly distinct from white canvas. Keep gutters below 1% and outer white margins below 2%. No white banner, no empty lower third, no isolated floating title, and no new prose, module, result, metric, logo, or decoration. The largest contiguous unused white rectangle must be less than 7% of canvas area. All text must remain uncut and at least as readable as the attached version.

The complete source-grounded contract follows and remains authoritative for scientific content. Where it mentions wider margins, 16:9, or a separate title band, the native 3:2 and edge-to-edge panel rules above take precedence.

"""
for cid in TARGETS:
    d=ROOT/'knowledge-base'/'cases'/cid
    existing=sorted(d.glob('figure.v*.png'))
    next_version=max([int(p.stem.split('.v')[-1]) for p in existing]+[0])+1
    (d/f'figure.v{next_version}.png').write_bytes((d/'figure.png').read_bytes())
    (d/f'prompt.v{next_version}.txt').write_bytes((d/'prompt.txt').read_bytes())
    (d/'prompt.txt').write_text(REPAIR+(d/f'prompt.v{next_version}.txt').read_text(encoding='utf-8'),encoding='utf-8',newline='\n')
    print(cid,'attached version',next_version,'-> next',next_version+1)
