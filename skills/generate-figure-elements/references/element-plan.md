# Element Plan

`elements.json` is the one input the pipeline reads. It records which objects of the approved overview become independent pictures, how each must look and where each goes. It extends the existing design/reconstruction notes; it is not a new registry, and an element's id should match the object id the Drawer already uses.

## Decide what belongs in it

Classify every visible object with the table in [Asset Production](../../design-scientific-figure/references/asset-production.md) first. Only these routes enter the plan as `generate`:

- a detailed illustration whose parts have no editable meaning (a robot, a patient, an organ, a building);
- a small decorative or contextual icon that must match the others' rendering.

Keep everything else out of the plan, or list it with another `route` so the inventory is complete:

| route | meaning |
| --- | --- |
| `generate` | produced on an element sheet by this skill |
| `extract` | a clean crop or original asset the user already has; drop the file in `assets/<id>.png` and it joins QA and placement |
| `native` | drawn from shapes, lines and text by the Drawer (recorded only so the inventory is whole) |
| `data` | exported from measurements or arrays; never generated |

## Fields

Top level:

| field | notes |
| --- | --- |
| `figure.ref_size_px` | `[width, height]` of the approved overview. Slots are in these pixels |
| `figure.width_mm` | printed width of the whole figure; it turns slots into physical sizes for the dpi check |
| `figure.target_dpi` | planning target, default 300. A working target, not a journal rule |
| `figure.background` | hex color of the figure page; QA also tests assets on it |
| `style.summary`, `line`, `shading` | one sentence each; copied into every sheet prompt so elements agree |
| `style.palette` | hex colors of the approved overview; the key color is chosen away from them |
| `style.avoid` | list of motifs to forbid (photorealism, gradients, text) |
| `style.references` | optional image paths; when present the prompt command suggests `imagegen.mjs edit --image ...` |
| `sheet_rules` | extra sentence appended to every sheet prompt |

Each element:

| field | notes |
| --- | --- |
| `id` | lowercase slug, unique, becomes `assets/<id>.png` and the draw.io cell id `img-<id>` |
| `route` | see above, default `generate` |
| `description` | one concrete sentence: subject, pose, key parts. No scientific claims the paper does not make |
| `label` | short human name used in the prompt and alt text |
| `view` | camera or pose: front, three-quarter facing left, isometric |
| `must_show` / `must_not_contain` | lists. Always forbid text and arrows unless a part is genuinely needed |
| `slot.bbox_px` | `[x0, y0, x1, y1]` in the approved image where the Drawer will put it. Required for `place` |
| `slot.anchor` | `center` (default), `bottom` or `top`. A figure standing on a pedestal or floor should be `bottom` with the slot floor at the pedestal line, so every figure keeps its feet there whatever its aspect ratio |
| `width_mm` | overrides the width derived from the slot |
| `sheet` | group name, or `solo` for one element on its own sheet (hero elements, retries) |
| `alt_text` | accessibility text for the picture object |
| `raster_reason`, `decomposition_note` | optional replacements for the default declarations the placement tools require |

## Getting slots from the approved image

Inspect the overview at full resolution and read each object's bounding box in its own pixels; round outward to a multiple of ten. The slot is where the artwork should sit, not a tight box: the subject is fitted inside it, aspect-preserved and centered (or anchored to the bottom or top edge with `slot.anchor`). A slot that is much larger than the final subject wastes sheet pixels; one that is much smaller makes the asset small and soft. Check the physical size: `slot width / ref width * figure width_mm`.

## What the pipeline writes next to it

```text
figure-elements/
  elements.json          # you write this
  style-lock.json        # palette + recommended key (palette command)
  prompts/sheet-01.txt   # exact text sent to the image model
  prompts/sheet-01.layout.json
  sheets/sheet-01.png    # raw model output (+ .json record from imagegen.mjs)
  sheets/sheet-01.rgba.png
  assets/<id>.png        # tight transparent crops with 12 px transparent padding
  qa/contact-sheet.png, qa/final-size.png, qa/qa-report.json
  manifest.json          # per element: file, size, visible box, source cell, key, sha256, qa result
  placement.drawio.json  # or placement.pptx.json
```
