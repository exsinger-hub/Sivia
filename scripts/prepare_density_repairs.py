#!/usr/bin/env python3
"""Create exact full v2 prompts for the six sparse wave-24 drafts."""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TARGETS=['instructblip','latent-diffusion','controlnet','mipnerf360','gaussian-dreamer','diffusion-policy']
REPAIR="""DENSITY REPAIR FOR VERSION 2 — APPLY TO THE ATTACHED VERSION 1 IMAGE.
Preserve every scientific stage, label, operand, arrow direction, object identity, palette, and left-to-right reading order from the attached image. Recompose the same content on the tool's native 3:2 landscape canvas. Enlarge the complete diagram vertically and horizontally so its meaningful-content hull spans at least 94% of canvas width and 88% of canvas height. Reduce the title to at most 4% of canvas height. Remove unused top and bottom bands; distribute existing miniatures, representations and support details within the enlarged panels. Increase panel height rather than adding prose. Keep 1.5% outer margins and 1% gutters. No new stage, metric, logo, footer, decorative object, or source-paper pixel. The largest truly unused rectangular region outside panels and connector lanes must be below 3% of the canvas. All labels remain fully visible and at least as large as version 1.

The remainder is the complete source-grounded production contract. It remains authoritative except where the native 3:2 canvas and tighter occupancy above replace its earlier 16:9 geometry wording.

"""
for case_id in TARGETS:
    folder=ROOT/'knowledge-base'/'cases'/case_id
    prompt=folder/'prompt.txt'
    if not (folder/'prompt.v1.txt').exists():
        (folder/'prompt.v1.txt').write_bytes(prompt.read_bytes())
    prompt.write_text(REPAIR+(folder/'prompt.v1.txt').read_text(encoding='utf-8'),encoding='utf-8',newline='\n')
    figure=folder/'figure.png'
    if figure.exists() and not (folder/'figure.v1.png').exists():
        (folder/'figure.v1.png').write_bytes(figure.read_bytes())
print('prepared',len(TARGETS),'full v2 prompts')
