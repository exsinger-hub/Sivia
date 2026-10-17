---
name: generate-figure-elements
description: Produce independent, transparent, correctly sized illustration elements (characters, organs, devices, scene objects, icons) for an editable draw.io or PowerPoint figure. Generates one flat key-color asset sheet with an image model, cuts it out locally, splits it into atomic assets, checks alpha, edges, clipping and effective dpi, and emits ready-to-run drawio_live_add_image / powerpoint_add_image arguments. Use after an overview draft is approved and the Drawer needs artwork with no native equivalent, or when a native figure needs a few stylistically consistent illustrations. Also the host-neutral image-generation step (Azure OpenAI, OpenAI, compatible endpoints) for hosts without a built-in image tool.
---

# Generate Figure Elements

Act as the asset producer between the Designer and the Drawer. The overview image shows what the figure should look like; this skill turns its illustrative objects into separate pictures that the Drawer places next to native text, shapes and arrows. It does not draw the figure, choose the composition or touch an approved layout.

## Host notes

- Other Sivia skills are loaded by name: Codex mentions `$name`, Claude Code uses `/sivia:<name>`, OpenCode and OpenWork call the `skill` tool with `{ name }`.
- MCP tools are written by bare name (`drawio_live_add_shape`). Some hosts prefix the server name, for example `sivia-drawio-live_drawio_live_add_shape` in OpenCode; use the tool whose name ends with the bare name.
- Paths in this file are relative to this skill's directory.
- Sivia-wide paths (`scripts/`, `knowledge-base/`) are relative to the Sivia root, the directory that contains `skills/`. When this skill was installed as a link (OpenCode and OpenWork do this), `..` from the link's location is not the Sivia root: resolve the link first (`realpath`, or `(Get-Item <skill-dir>).Target` in PowerShell). A copied skill records its origin in `.sivia-installed.json` next to `SKILL.md`. Paths inside a skill are relative to that skill's directory.
- Image generation: Codex and any host with a built-in image tool use it. Otherwise run `node scripts/imagegen.mjs` (Azure OpenAI, OpenAI or an OpenAI-compatible endpoint, configured through environment variables).

## When to use it

Choose the representation first with [Asset Production](../design-scientific-figure/references/asset-production.md). This skill covers only the row "detailed illustration, textured scene or other illustrative artwork", plus the retained-pixel and transparency checks around it.

| Use it for | Do not use it for |
| --- | --- |
| A robot, patient, organ, building, device or scene object that a native shape cannot express and that must stay independently replaceable | Boxes, arrows, token strips, grids, simple glyphs, operators: draw them natively |
| Several such objects that must look drawn by one hand | Measured results: plots, microscopy, masks, activations, spectra come from the original data |
| Replacing a tiny, blurry crop of the draft with a clean standalone asset | A whole panel or the whole overview: that is the ImageGen-first workflow with its full template |

Generated elements are schematic. Never present them as measurements, and never let them stand in for a field that must be exported from real data.

## Gate

Run this only inside an authorized stage: the user has approved a visual draft and asked for the editable figure, or has explicitly asked for generated elements. An approved image alone does not authorize it. Do not launch PowerPoint, WPS or draw.io from here; hand the placement arguments to the Drawer.

## Image generation setup

Codex and any host with a built-in image tool use it. Otherwise `scripts/imagegen.mjs` calls an endpoint configured through environment variables; nothing is read from files and no credential is ever printed or written to a record.

| Provider | Variables |
| --- | --- |
| Azure OpenAI / Microsoft Foundry | `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT` (or `AZURE_OPENAI_BASE_URL`; the `.../openai/v1` URL), `AZURE_OPENAI_DEPLOYMENT`. Legacy resource URLs also need `AZURE_OPENAI_API_VERSION` |
| OpenAI | `OPENAI_API_KEY`, optional `OPENAI_BASE_URL`, `OPENAI_IMAGE_MODEL` (default `gpt-image-1`) |
| Any OpenAI-compatible server | `SIVIA_IMAGE_BASE_URL`, `SIVIA_IMAGE_MODEL`, optional `SIVIA_IMAGE_API_KEY` |

`node scripts/imagegen.mjs status` reports which provider it will use. `--dry-run` prints the request with the key redacted. Image deployments differ: check the returned size and transparency instead of assuming them (see [Sheet Prompting](references/sheet-prompting.md) for what was observed).

## Workflow

Work in one folder per figure (`--workdir`, default the current directory). Run the scripts by their full path inside this skill directory, for example `python <skill-dir>/scripts/sivia_assets.py prompt --workdir figure-elements`; the commands below abbreviate it to `scripts/...`. Every command prints JSON; read its `warnings`.

1. **Inventory.** From the approved overview (or the design spec) list each element that needs artwork. Write `elements.json` following [Element Plan](references/element-plan.md): id, one-sentence description, view, what it must not contain, and its slot (bounding box in the approved image's pixels) when the layout is fixed. `python scripts/sivia_assets.py init --workdir DIR` writes an example.
2. **Style lock.** `python scripts/sivia_assets.py palette --image approved.png --workdir DIR` extracts the palette and recommends a key color far from it. Add a short `style` block (rendering, line weight, shading) to the plan so every element shares it. See [Sheet Prompting](references/sheet-prompting.md).
3. **Prompt.** `python scripts/sivia_assets.py prompt --workdir DIR` writes one prompt per sheet (up to six elements each, in a grid, on a flat key color) plus a layout file. Read the prompt and its `warnings`: a cell too small for the element's physical size is reported before any image is generated. Give an element `"sheet": "solo"` when it needs more pixels. The whole-figure length floor does not apply to element prompts.
4. **Generate.** Use the host's image tool with the exact prompt file, or `node scripts/imagegen.mjs generate --prompt-file DIR/prompts/sheet-01.txt --size 1536x1024 --quality high --out DIR/sheets/sheet-01.png`. Attach style references with `edit --image ref.png`. The CLI writes `<file>.json` with the exact prompt, model and hash. **Look at the sheet**: count the objects, check the background, and confirm no text or arrows were painted.
5. **Cut out and split.** `cutout --sheet-id sheet-01`, then `split --sheet-id sheet-01`. Cut-out measures the background that was actually painted and solves edge transparency against it, so no key-color fringe remains. Split crops each grid cell to a tight transparent PNG under `assets/` and records it in `manifest.json`.
6. **Check.** `qa --workdir DIR [--bg "#RRGGBB"]` tests real alpha, clipping, key spill, stray specks and effective dpi at the planned physical size, and writes `qa/contact-sheet.png` (checker, white, dark and your panel colors) and `qa/final-size.png`. Open both images: metrics cannot see a missing hand, a wrong silhouette or a baked-in label. Fix by the table below, then rerun.
7. **Place.** `place --backend drawio` (or `pptx --slide-index N`) writes `placement.<backend>.json`: complete arguments for `drawio_live_add_image` / `powerpoint_add_image`, with every raster declaration filled, the visible subject centered in its slot and transparent padding accounted for. The Drawer executes the calls in order, then runs the normal Reviewer loop on the native structure and a fresh render. Match `--canvas` to the real canvas or slide; the command warns when its aspect differs from the approved reference.

Keep `elements.json`, the prompts, the sheets, `manifest.json` and the contact sheet with the figure's other production notes. To change one element later, edit its description, mark it `"sheet": "solo"`, rerun steps 3 to 7 for that sheet and call `place` again; the id and slot stay the same.

## Failure to next action

| Observed | Change |
| --- | --- |
| Background is a gradient, textured, or has a floor or shadow | Regenerate with the background rule moved to the first line of the prompt; or run `cutout --lo 40 --hi 110`. A missing flat key is a generation defect, not something to mask around |
| Painted key differs from the requested one (`#08F601` for `#00FF00`) | Nothing: cut-out uses the measured color. Only force `--key` if the border is covered by artwork |
| An element touches its cell (`split` fails it) | Regenerate that element as `solo`, or pass `--box id=x0,y0,x1,y1` when the object is intact but the grid was ignored |
| Subject colors collide with the key (a hole or green patch inside an object) | Pick another key with `prompt --key #FF00FF`; the palette step already ranks the safest |
| Text, arrows or a frame were painted | Add them to `must_not_contain`, regenerate that sheet. Labels and arrows are native objects |
| Elements look like different artists | Attach the approved overview crop or a finished element as `edit --image`, restate the style lock, keep elements in one sheet |
| `effective_dpi` below target | Larger `--canvas`, fewer elements per sheet, or `solo`; otherwise reduce the placed size. Do not upscale |
| White parts of an object vanished | The key was too light or close; use a saturated key and `--hi` lower than the distance to white |
| draw.io shows a broken-image icon | Update Sivia: older servers cut the embedded data at `;base64` |

## Rules

- One element per picture. Never merge elements, add labels, arrows, frames or panel backgrounds to an asset; the Drawer builds those natively.
- Keep the generation prompt, returned image and sheet alongside the asset so any element can be regenerated or replaced independently.
- The role is `schematic illustration`. Record it in the figure notes and use a short in-figure "schematic" label only when a reader could mistake the artwork for data.
- Inspect the placed result at final size, not only the standalone asset.
- Report what is native, what is an independent raster asset and each asset's effective dpi and source prompt.
