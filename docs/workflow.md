# Sivia workflow

English | [简体中文](workflow_ZH.md) · [Back to README](../README.md)

The outcome is a source-grounded figure whose important relationships are readable, and—when requested—editable. Testing drives corrections; it is not a substitute for producing the artifact.

## Enter at the stage you requested

| Request | Start here | Stop here |
| --- | --- | --- |
| Paper → overview | Scientific argument and visual references | Actual image + full prompt; ask for feedback and the optional PPT step. |
| Prompt only | Scientific argument and full prompt | Prompt, without image generation. |
| Revise an image | Current image/prompt and named changes | Revised image + full prompt; wait again. |
| Approved image → editable PPTX | Locked reference and object inventory | Native file, preview and editing/source notes. |
| Edit named PPT objects | Exact document/slide and allowed changes | Scoped corrections with regression review. |

An already approved reference does not need another image-generation round. Faithful copying and manuscript adaptation are different requests: the former preserves visible content; the latter grounds permitted replacements in scientific sources.

## 1. Establish the scientific message

Read the relevant paper text, equations and supplied implementation. Identify the research problem, the important prior limitation, the contribution, and input–operation–output relationships. Resolve contradictions that affect the explanation before fixing them in a diagram. Use one sentence to define what the reader should understand.

Choose the content that earns space in this figure. Mechanism verbs such as rearrange, select, merge or supervise need visible objects and operations, not a wall of module names. Keep implementation detail in the paper unless it changes the figure's meaning.

Scientific authority comes from the manuscript, verified code and real results. Reference images supply visual language. An approved image additionally fixes composition; it does not validate invented measurements.

## 2. Select paired visual references

Inspect a relevant [knowledge-base image](../knowledge-base/README.md) and its **complete prompt**, or the user's reference. Select by communication task rather than superficial topic similarity. Extract region proportions, focal hierarchy, graphic objects, colors, labels and connection rules.

Organize the new method around its own reading path. Record the selected template; do not transplant its model structure, equations or reported results. See [template selection](../skills/design-scientific-figure/references/prompt-templates.md).

## 3. Write and check the complete production prompt

Describe the figure's claim, canvas, reading path, and each region's objects, position, relative scale, relationships, exact short labels, palette and typography. Keep production instructions outside the printed artwork.

Save the exact text to be submitted. Validate its **non-whitespace character count** against the full bound template for that figure; it must not be shorter. Do not satisfy the floor with repeated adjectives or fabricated science. Revisions integrate all retained constraints into a full prompt rather than submitting only a short difference description. The [prompt-detail reference](../skills/design-scientific-figure/references/imagegen-prompt-detail.md) defines the check and helper usage.

## 4. Generate, inspect and pause

Call the available image-generation tool and inspect the returned image, not just its prompt. Check method relationships, arrow direction, labels, hierarchy and reduced-size legibility. Correct observed defects within the requested scope; preserve image/prompt pairs by version.

Deliver the actual image, full prompt and short design explanation. Ask what should change and whether the user wants an editable PPT, then stop. Do not connect to PowerPoint/WPS during this pause. A positive reaction to the image alone is not permission to create a deck.

## 5. Lock and decompose the approved reference

After an explicit editable request, record the approved version, aspect ratio, panel bounds, object coordinates, palette, font hierarchy, reading order and routes. Use stable object names and a single reconstruction specification. Reuse already provided approval; do not ask the user to repeat it.

Classify assets before cropping:

- Rebuild labels, shapes, operators, grids, simple icons and diagrams as native objects or meaningful composites.
- Build plots from original values. Export experimental images and learned features from their actual sources; keep paired samples and display conditions consistent.
- Retain a detailed illustration as one independent asset with separate native labels and arrows. Reuse approved character artwork when regeneration would change its identity. Generate a standalone replacement only when permitted.

For a crop, calculate `effective_dpi = retained_pixels × 25.4 / placed_size_mm`. A 30 mm image at a 300 dpi planning target needs 355 pixels across; increasing its DPI tag cannot supply missing information. Check real alpha as well as edges on light/dark backgrounds. The [asset-production reference](../skills/design-scientific-figure/references/asset-production.md) covers authorized local masking when generation fails to produce usable transparency.

## 6. Build, recover and keep moving

Identify the actual application, backend and document, and preserve foreground focus. Tool names and Windows COM display names can be misleading: if detection conflicts with observed behavior, inspect the executable path/registration read-only. Never modify another open document to get past a failed binding.

Use isolated files by default for new work. Construct one region from background to foreground, keeping native text and semantic object names. Batch where the backend supports it; slow one-line playback is not required. After styling text, verify fixed bounds. After grouping, inspect every external route again because group creation can cover arrows with panel fills.

When a call fails, change the action that controls the failed property:

| Failure | Next action |
| --- | --- |
| A small crop looks soft | Find the original asset, redraw native geometry, or independently regenerate allowed illustration artwork; report genuine source limits. |
| Painted checkerboard instead of alpha | Correct the background through the image tool; if still unsuccessful, use an authorized appropriate mask and inspect its edges. |
| Setter succeeds but radius/text/arrow is wrong | Inspect the actual property/render; restore bounds or use a supported native representation. |
| A host call stalls | Stop further mutations to that busy host, preserve the draft/specification, and continue independent work. |
| The requested PPTX can still be built without the blocked host | Use an available isolated native OOXML candidate, without mixing old live handles or changing an explicitly required application. |
| Exact target rendering is unavailable | Inspect the actual PPTX through another already available import renderer; keep target-application verification pending. |

An isolated file recovery is a construction method, not a claim of live editing or an automatic bundled service. Honor tool restrictions and explicit live-document requirements. If recovery needs broader authority, new science or a changed composition, ask for that specific choice. Do not repeatedly retry the same stalled operation or close the user's application.

The [runtime recovery reference](../skills/edit-powerpoint-live/references/reconstruction-recovery.md) gives the detailed route and demonstrated object-level fixes.

## 7. Review the file that will be delivered

Use four logical roles: Designer defines the source contract; Drawer builds; Reviewer finds concrete defects; Corrector specifies minimal changes. A single agent may hold the roles, but an informed/self review must not be reported as an unprimed independent review.

Inspect native structure and a fresh **render of the actual PPTX** after each completed region and after grouping/final corrections. Check exact text, endpoints, image atomicity, z-order, clipping and correspondence at the intended size. A separately generated same-coordinate PNG does not prove that a PPTX renders correctly. Correct observed local defects before dependent work; missing target-application evidence stays pending without blocking safe independent construction.

For a complete overview, prepare real title-hidden and title/L3-hidden PPTX copies with [prepare-overview-review.py](../scripts/prepare-overview-review.py). Preserve critical conditions. Render the copies, derive grayscale and record physical width. Show the reduced view to an unprimed reviewer, freeze the response, then show full-density title-hidden grayscale and freeze that response before revealing color and the intended claim. See [review-copy instructions](../skills/audit-scientific-figure/references/review-copies.md). Local micro-edits use scoped regression instead of repeating an unchanged narrative test.

Report evidence separately for scientific fidelity, editability, preview rendering, target-application rendering, narrative and physical-size legibility. No object count, successful script or averaged score can cancel a wrong arrow or missing evidence.

## 8. Package the final artifact

Keep one clearly named source and its current preview in the delivery folder. Archive intermediate versions and audit records outside it. When useful, include independently replaceable illustrations and redistributable fonts with licenses.

Editing notes should explain native versus composite/vector/raster content, whether equations/charts are native specialized objects or shape/text assemblies, and whether routes reattach automatically. State font approximations or installation needs, actual crop resolution and renderer. Keep schematic values separate from measured results.

Example delivery layout:

```text
delivery/
  figure.pptx
  figure-preview.png
  editing-notes.md
  fonts/                 # only when useful and redistribution is permitted
  illustrations/         # optional independent assets
```

The editable file, its reviewed preview and target-application verification are different deliverables. Deliver a candidate with a clear pending gate when a required renderer is unavailable; do not claim a complete visual pass while an observed hard defect remains. Public knowledge-base submission is a separate action requiring authorization for the included material.
