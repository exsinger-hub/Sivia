---
name: audit-scientific-figure
description: Review a scientific figure or overview in draw.io, PowerPoint or WPS for readable scientific narrative, source fidelity, publication-size layout, routing and editability. Use for independent visual review, candidate comparison or verification after corrections.
---

# Audit Scientific Figure

Act as the Reviewer. Review read-only evidence and issue findings; do not draw during the review phase. A successful MCP call is not evidence that the figure is visually or structurally correct.

## Resolve review scope

Distinguish a new/full-publication review from scoped regression after an approved micro-edit. In scoped regression, inspect changed objects, their interfaces and a fresh whole-figure render for collateral changes; compare unchanged layout and style with the accepted baseline. Apply the categories below to that scope. Do not require fresh masked-view reading of an unchanged narrative just to approve a label or image replacement. Report inherited/out-of-scope defects separately without silently authorizing their repair; a scoped pass is not renewed whole-figure publication approval. A structural change or explicit full-publication review uses all applicable gates below.

## Collect both evidence channels

For PowerPoint or WPS, inspect the deck, run `powerpoint_audit_figure`, and export the slide through `powerpoint_export_slide_image`. Record whether the renderer is Office.js PowerPoint, COM PowerPoint, or the OOXML fallback. Treat renderer differences as application-specific evidence, not permission to flatten editable content. In Office.js, treat `connector_mode=geometry_backed` and `implementation=officejs_editable_shape_composite` as declared limitations that still require visual routing and editability review.

For draw.io, inspect the live model, run `drawio_live_audit_figure`, and capture the current renderer through `drawio_live_screenshot`.

When a reference exists, inspect the full reference and the crop matching the current region. Compare at readable resolution.

When the figure is derived from a manuscript, paper PDF, method section, equations, or an evidence pack, read [Manuscript-to-Figure Workflow](../design-scientific-figure/references/manuscript-to-figure-workflow.md) completely. Obtain the frozen Figure Claim, Paper Figure Signature, required-node and required-edge ledgers, equation-operand ledger, evidence ledger, publication display width, and permitted omissions. Review the source contract and the artifact; do not infer a missing manuscript fact from the Drawer's visual intent.

## Apply the publication aesthetic gate

For a paper overview, graphical abstract, teaser, final whole-figure review, or comparison of candidate style directions, first read [Fundamental Visual Grammar](../design-scientific-figure/references/fundamental-visual-grammar.md) completely and verify the frozen `visual_grammar_receipt`. Then read [references/publication-aesthetic-review.md](references/publication-aesthetic-review.md) completely and apply it to the fresh render. These gates are mandatory even when deterministic structure audit reports zero hard failures.

Review the figure at thumbnail scale for silhouette and focal hierarchy, fit-to-slide scale for composition and rhythm, and readable scale for typography, spacing, connectors, and local finish. When multiple style candidates are presented, compare them together; palette, font, corner-radius, or border changes alone do not constitute different directions.

Judge containers, bottom strips and line styles by their scientific role and effect on the reading logic. Treat an equal-weight card wall or decorative hierarchy as class A only when it obscures the intended focal hierarchy. Recommend recomposition for that failure, subject to the user's change scope; useful scope containers and parallel study arms remain valid. The user's approved composition cannot be replaced solely because a generic style heuristic prefers another layout.

For overviews, read [Overview Narrative](../design-scientific-figure/references/overview-narrative.md) completely. First give an independent Reviewer only the title/L3-hidden grayscale view and physical size, record their reading, then show the full-density title-hidden grayscale view and save that reading too. Freeze both original responses before revealing the full color image and Figure Claim, then the contract, abstraction map and structure evidence. Withhold object counts and previous verdicts until after the visual readings. Record prior exposure: same-context judgment is `self_review`; an independent Reviewer already told the story is `informed_review`, not unprimed evidence.

Require actual exported review views. For saved PPTX sources, use [prepare-overview-review.py](../../scripts/prepare-overview-review.py) as described in [Review Copies](references/review-copies.md). The helper creates editable copies, not rendered images. The Drawer renders these copies; the Reviewer remains read-only.

When the declared style is hand-drawn, sketchnote, pencil, doodle, whiteboard, or Excalidraw-like, also read [Hand-drawn Technical Style](../design-scientific-figure/references/hand-drawn-technical-style.md) completely. Review scientific clarity and hand-drawn fidelity as separate questions. A clean diagram can pass semantics yet miss the requested style; a visibly rough diagram fails when its jitter, texture, font, or doodles reduce publication-width legibility or make topology ambiguous. Do not reward noise as authenticity.

## Review taxonomy

Review every region and the whole figure for:

1. scientific semantics, exact readable text, topology, and arrow direction;
2. editability coverage and meaningful object hierarchy;
3. raster irreducibility and decomposition metadata;
4. geometry, repeated alignment, equal spacing, margins, and whitespace;
5. text fit, wrapping, font hierarchy, and color consistency;
6. clipping, unintended overlap, z-order, and object bounds;
7. arrowhead clearance, connector path-through-object, label intersection, backtracking, and route crossings;
8. reference correspondence or no-reference design consistency.

For manuscript-derived figures, require complete coverage of non-omissible nodes and edges across the main view and linked readable expansions. Use the abstraction map to reconstruct internal grouped relations at their declared level and external relations from visible ports and routes. Check operands, inverse order, producer scope, training/inference and update/freeze ownership wherever they affect the claim. These critical cues must survive L3 removal. Object ids alone do not establish correct visible relations.

Inspect a title-hidden grayscale thumbnail at the declared review size. Confirm that the Figure Claim's mechanism or result is the first focal point and that overview/detail hierarchy survives without color. Re-run the affected render-scale checks after each structural correction.

Use the same categories and thresholds for draw.io and PowerPoint.

## Deep editability audit

Inspect pictures semantically, not only by object count. Fail the region when one image still contains separable content such as:

- a row or grid of predictions, masks, heatmaps, or microscopy fields;
- a before/after or method comparison;
- multiple independent photographs or channels;
- editable titles, labels, borders, arrows, legends, axes, tables, or regular plots.

Require one image object per irreducible visual field. Require the surrounding frame, grid, heading, legend, connector, and annotation to be separate editable objects. A crop that merely removes the outer panel border is not sufficient when the remaining crop is still composite.

Every retained image must have a precise reason, tight crop, `atomic_raster_unit=true`, `contains_reconstructable_content=false`, and a useful decomposition note.

## Finding format

Emit one record per defect:

```text
region: stable region id
objects: exact names/ids
category: shared defect category
severity: hard | warning
evidence: measurable structure or renderer observation
correction: required outcome, not vague advice
acceptance: condition the next audit can verify
evidence_status: measured | observed | inferred | pending
```

Treat wrong text/direction, reconstructable content inside a picture, a non-atomic picture, clipping, arrow intrusion, a route through an unrelated label/object and ambiguous connector crossings as hard failures. A necessary network crossing with clear ports or bridges is not automatically a defect.

For aesthetic findings, use the A/B/C classification and the location, defect, cognitive impact, severity, exact correction, and expected-effect fields required by the publication aesthetic reference. Do not hide a concrete aesthetic defect behind an averaged score.

## Evidence verdict

Report `pass | fail | pending` separately for scientific reconstruction, editability, target rendering, physical-size legibility and visual narrative. Each verdict names the concrete artifact or observation that supports it. Use counts for measured coverage and object inventory; do not invent calibrated confidence or derive beauty from object count.

Pass requires correct readable semantics at the assigned levels, reconstructable native content, no clipping or ambiguous routes, zero unresolved hard findings, no class-A failure and no class-B issue that blocks reading. A local geometry check can pass while publication approval is pending. An unavailable target renderer, missing masked view or unperformed review remains `pending`; a same-coordinate SVG is a design preview, not a PPTX render.

When the user explicitly asks for ratings, label subjective ratings as such and keep them separate from evidence gates. No numeric average can cancel a real defect or missing evidence.

## Review loop

While construction is partial, scope local checks to completed objects and their boundary interfaces. Mark whole-figure narrative and final masked-view checks pending until the relevant content exists; this is not a local defect or a reason to prevent the next planned region. Apply the staged overview reading test to a complete candidate, before overall approval.

1. Review one completed region in whole-slide/canvas context.
2. Send findings to `$correct-scientific-figure`.
3. Let the backend Drawer execute the correction plan.
4. Collect a fresh structure audit and fresh render.
5. Review again from new evidence.
6. Approve the region only after the pass gate is satisfied.
7. After all regions pass, repeat for the whole figure.

Never approve based on the Drawer or Corrector claiming success. Never reuse a stale screenshot.

## Review report

Return the evidence verdicts, observed findings, native/composite/raster counts, raster declarations and any unresolved source ambiguity. For overviews include the recorded unprimed reading (or self-review disclosure), actual review-image paths and hidden object sets, physical size and comparison with the intended narrative. Identify up to three changes with the highest real visual impact; do not invent defects to fill a quota.
