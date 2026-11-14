# Sheet Prompting

## Why a key-color sheet

Whether an image model returns transparency depends on the provider and the deployment, so treat it as something to verify from real alpha, never to assume.

- Asking for transparency **in the prompt only** does not work: the model returns an opaque image, often with a painted grey checkerboard that looks transparent in many viewers. (Observed on an Azure `gpt-image-2.5` deployment: an RGB file whose corner pixels were grey.)
- The API parameter `background=transparent` is honoured by some deployments and rejected or ignored by others. On the same Azure deployment it returned a clean RGBA image for a detailed element (a seated robot with white and pale parts): no interior holes, light parts fully opaque, no fringe on white, dark or saturated green backgrounds. That is one deployment and one element, not a guarantee.

If your provider supports the parameter, a single element can be generated with `imagegen.mjs generate --background transparent`, skip `cutout`, and go straight to `split --sheet <that file>` (a one-cell sheet needs a `"sheet": "solo"` element). Check the alpha with `qa` either way.

The route that does not depend on provider support is to ask for a perfectly flat key color and remove it locally. Pixels at the edge of an object are a blend of the object and the background; because the background is known, the cut-out solves each edge pixel's alpha and re-estimates its true color from the neighbouring solid pixels. This leaves no colored halo, keeps white and light parts of the artwork (a white robot on a green sheet stays white) and costs about a second per sheet.

One sheet per request also keeps the elements stylistically consistent, and one generation call replaces six; separate calls to a transparent-capable endpoint give no such consistency guarantee.

## Choose the key color

`palette` ranks pure green, magenta, cyan, yellow, orange and blue by their distance to the approved palette and recommends the farthest. The key must not appear inside any element: a green plant on a green sheet loses its leaves. Rule of thumb: pick the candidate whose nearest palette color is more than about 150 away in RGB. Models usually paint the requested key slightly off (`#00FF00` arrives as `#08F601`); the cut-out measures the painted border and uses that.

## What the prompt contains

The template `references/templates/element-sheet.txt` fills these parts from `elements.json`:

1. **Background rule first and in capitals**: one perfectly uniform color, no gradient, floor, shadow, glow or checkerboard, and the key color forbidden inside elements.
2. **Grid**: columns by rows, equal cells in pixels, one element per cell, centered, filling 65 to 75% of the cell's shorter side with at least 12% margin, nothing crossing a border, no grid lines or frames. Unused cells are declared empty.
3. **Content in reading order**, one numbered line per element with its row and column, description, view, must-show and must-not-contain.
4. **Style lock**: rendering, palette, line weight, shading and an explicit consistency sentence.
5. **Hard exclusions**: no text, digits, labels, logos, arrows, connectors, legends, frames or decorative filler.

Element prompts are not subject to the whole-figure length floor in [ImageGen Prompt Detail](../../design-scientific-figure/references/imagegen-prompt-detail.md); that rule applies to complete figure generations and revisions. Each element still needs concrete subject, pose and part descriptions rather than adjectives.

## Sizes

The default canvas is 1024x1024 for square grids, 1536x1024 for wide and 1024x1536 for tall grids, which every `gpt-image` family accepts. `gpt-image-2` deployments accept any size whose edges are multiples of 16 (long edge up to 3840, aspect at most 3:1, 0.66 to 8.3 megapixels); pass `--canvas 2048x1360` to `prompt` and the same `--size` to `imagegen.mjs` when elements need more pixels. The subject of a cell is about 70% of its shorter side, so a 512 px cell gives roughly 360 px: 30 mm at 300 dpi needs 355 px. `prompt` reports cells that are too small.

## Style references

For consistency across several sheets, or to match the approved overview, attach reference crops: `imagegen.mjs edit --image overview-crop.png --prompt-file ...`. Say in the prompt which properties to copy (palette, outline weight, shading) and that the subjects are new. Keep invariants explicit; an edit with no stated invariants drifts.

## Reading the result

Open the raw sheet before cutting it out and answer:

- Is the background flat, and is it the requested hue?
- Are all elements present, each inside its cell, none touching a border?
- Is any text, number, arrow or frame painted anywhere?
- Do the elements share outline weight, palette and detail level?
- Is any part of an element the key color or very close to it?

A "no" is a generation defect. Change the prompt or the plan and regenerate that sheet (or only the failing element as `solo`); do not keep post-processing a sheet that violates the contract.

## What a real run looked like

Recorded from the first end-to-end run (Azure `gpt-image-2.5` deployment, 1536x1024, `high` quality, six elements in a 3x2 grid, about 36 s). It is one sample, not a guarantee:

- All six elements arrived inside their cells, in the requested order, in one consistent flat style, with no text, arrows or shadows painted. The prompt's style lock and exclusions were followed.
- The requested `#00FF00` arrived as about `#08F601`, uniform to within 2 to 3 levels across the sheet.
- A few isolated pixels at the image edge drifted into the key-color transition band. Cut-out removes components that never reach solid alpha, so they do not stretch an element's bounding box.
- White and pale parts of the artwork (robot bodies, paper) and a muted green island survived the cut-out; the saturated key was far enough from both.
- Seven or more elements per sheet (`--per-sheet 9`) are supported by the layout code but were not evaluated for quality. The default is six.

Treat any deviation from these points as a reason to inspect the sheet, not as an expected quirk.
