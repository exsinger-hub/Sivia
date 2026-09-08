---
name: design-scientific-figure
description: Translate a research brief or manuscript into an overview, architecture or mechanism figure. Use for source-grounded visual scenes, detailed template-led ImageGen prompts, visual-draft approval and faithful editable PPT reconstruction, or explicitly requested native design in PowerPoint, WPS or draw.io. Existing reference-only reconstruction belongs to recreate-scientific-figure.
---

# Design Scientific Figure

Act as the Designer in the four-role Sivia protocol. Produce a backend-neutral design specification before the Drawer adds any object. The selected backend affects object mapping, not the design quality or acceptance gate.

## Start from the paper, not a workflow-shaped user prompt

A request such as "Use Sivia to read this paper and draw its overview as editable PowerPoint" is sufficient. Read the paper before choosing a template: identify the research problem, prior limitation, distinctive method, input/output and supporting evidence, then decide what this figure should explain. Users do not have to supply a production prompt, template file, length rule or list of internal stages.

For a new ImageGen-led figure without an explicitly selected template, read [Bundled Prompt Templates](references/prompt-templates.md), choose the role that matches that scientific argument, and read the selected full template. Instantiate it from the paper rather than sending its unfilled slots to ImageGen. Template choice, detailed prompt writing and length validation are internal responsibilities. Preserve an existing bound template and approved layout when continuing a figure; an internal default never overrides either.

## Bind the requested execution

For new manuscript overviews, prefer the [ImageGen-first workflow](references/imagegen-first-workflow.md) when the image-generation tool is available. Read that reference completely when using this route or continuing an already approved visual draft. Respect explicit native-only, prompt-only, reference-reconstruction and read-only requests; do not insert generation into those tasks. If ImageGen-first is requested but unavailable, continue source/prompt preparation and report the missing rendering capability rather than silently switching production methods.

Record `execution` in the existing `design_spec`: requested deliverable, renderer, output path and whether editability is required. For editable PowerPoint/draw.io requests, use the native Drawer and its fresh renderer export. A PNG, including one inserted into a slide, does not satisfy that contract.

For a requested raster image, ImageGen rendition or bitmap-reference visual study, use the available image-generation tool after the same source-to-scene design work. Inspect local references before passing them to the renderer, preserve the approved composition, save the prompt and actual output, and compare that output with the reference and source. Report it as raster, not native reconstruction or preserved empirical pixels. Reading this skill or writing a prompt without producing and inspecting the requested artifact is not an execution test. In raster mode, the native capability probes, object-level handoff and native editability gates below do not apply; scientific and visible-reference checks still do.

For template-led ImageGen prompts, including the ImageGen-first then editable-PPT workflow, read [ImageGen Prompt Detail and Length](references/imagegen-prompt-detail.md) completely before drafting. Each complete generation or revision prompt must be at least as long as its bound template and specify the figure region by region. Run its length check on the exact text to be submitted; do not generate with a shorter summary or change-only instruction after checking a longer draft.

## Detect constraints

Before native construction, read the selected backend's capabilities. Use `powerpoint_status` then `powerpoint_get_capabilities` for PowerPoint/WPS, or `drawio_live_get_capabilities` for draw.io. When live Mac PowerPoint is requested, also require `powerpoint_officejs_status` to report a connected task pane. Design only with semantic objects the selected adapter can create editably; use declared editable composites when a native monolithic object is unavailable. Raster/prompt preparation does not require launching or connecting a presentation application.

## Define the message

Record:

- one sentence stating the scientific message;
- intended audience and reading order;
- required stages, entities, evidence, comparisons, and causal links;
- target aspect ratio and output size;
- labels or facts that must remain exact;
- uncertainty or content still needing user input.

## Derive from a manuscript

When the source is a manuscript, paper PDF, method section, equations, supplementary text, or an evidence pack, read [Manuscript-to-Figure Workflow](references/manuscript-to-figure-workflow.md) completely before freezing the design.

First translate the paper into a Figure Claim and source-linked visual scenes using the manuscript workflow's editorial pass. Decide what this figure explains, what belongs in a linked detail, and what stays in the paper before assigning coordinates. A complete module inventory is not this translation.

Then freeze the Paper Figure Signature and the in-scope node, edge, operand and evidence ledgers. Derive the publication slot and composition family from this contract before reference retrieval. In blinded independent design, also require a target-paper and derivative-asset exclusion receipt before retrieved assets are materialized.

Do not enter publication drawing until the selected direction maps every required node and edge or records a source-grounded permitted omission. A missing operand, condition, inverse/alignment step, evidence producer, or update owner is a contract failure rather than a styling choice.

### Run a blind Figure Gym comparison

When the user asks to design independently without seeing an existing overview and then compare against it, read [Blind Figure Gym Protocol](references/blind-figure-gym.md) completely. Apply its sealed-target sequence in addition to the manuscript contract.

Do not inspect the target figure, its caption, alt text, layout description, or derivative diagram before the editable artifact and fresh review render pass the pre-reveal gate. Record an exclusion receipt and freeze receipt in human-readable form. After reveal, preserve the blind artifact unchanged, compare communication decisions rather than pixel similarity, and put any revised response in a separately identified version.

## Build the layout system

When the user has selected a supplied image's composition, follow the approved-reference procedure in [Fundamental Visual Grammar](references/fundamental-visual-grammar.md). Preserve its useful region proportions and graphic density while filling it with source-grounded scenes. Default simplicity or focal-point heuristics do not authorize replacing that layout with a sparse pipeline.

For an overview, graphical abstract or dense method figure, read [Overview Narrative](references/overview-narrative.md) completely first. Freeze a `narrative_map` for first-glance, working and technical reading, plus an `abstraction_map` linking the complete scientific contract to main groups and readable expansions. Coverage spans the main figure and linked detail panels; it does not require every implementation node to be directly visible in the overview. Preserve all interpretation-changing boundaries and operations at L1/L2.

Specify before drawing:

- outer margins, panel grid, gutters, and shared alignment anchors;
- panel ids, bounds, hierarchy, and construction order;
- standard node sizes, corner radii, stroke widths, and spacing tokens;
- title, section, label, annotation, and caption typography;
- a limited semantic palette with accessible contrast;
- reserved connector lanes and permitted entry/exit sides;
- legend, annotation, table, chart, and raster-evidence locations;
- z-order and meaningful grouping.

Choose a dominant organizing logic from the science: a spine, loop, parallel comparison or another justified composition. Use L1/L2/L3 for reading depth; a focal region may contain several objects.

## Define publication aesthetics before drawing

For a publication-facing figure, graphical abstract, style comparison, or any request involving aesthetics, visual quality, or beautification, first read [Fundamental Visual Grammar](references/fundamental-visual-grammar.md) completely and freeze its `visual_grammar_receipt`. Then read [Publication Aesthetic Review](../audit-scientific-figure/references/publication-aesthetic-review.md) completely before freezing the `design_spec`.

When the requested direction is hand-drawn, sketchnote, pencil, doodle, whiteboard, or Excalidraw-like, also read [Hand-drawn Technical Style](references/hand-drawn-technical-style.md) completely. Declare its `style_family`, `imperfection_budget`, typography split, and backend-native drawing strategy in the `design_spec`. For a paper overview, default to restrained technical hand-drawing unless the communication purpose and final display size genuinely support a denser sketchnote or pencil treatment.

For each direction, define a `style_dna` that changes drawing decisions, not just surface decoration:

- composition skeleton and reading path;
- dominant focal zone and primary silhouette at thumbnail scale;
- relative visual mass of scientific novelty, process, and real evidence;
- shape grammar, line behavior, arrow convention, icon language, and depth treatment;
- typography roles, semantic palette, and contrast hierarchy;
- whitespace strategy, including the intended function of every large empty region;
- forbidden motifs that would create a generic PPT, dashboard, poster, or AI-generated appearance.

Treat whitespace as functional only when it separates hierarchy, protects a focal point, reserves a connector lane, or improves grouping. Do not shrink the scientific content to preserve empty bands that have no stated function. Plan the meaningful-content hull inside the usable canvas and reject a layout when the main content can be enlarged substantially without harming hierarchy or connector clarity.

When proposing multiple style directions, compare their `style_dna` before drawing. Two directions are cosmetic variants if they preserve the same composition skeleton, reading path, focal zone, major module proportions, and evidence placement while changing only palette, font, border, or corner radius. A distinct direction must change the composition skeleton or reading path and at least one of focal strategy, evidence-to-mechanism weighting, or shape/line grammar, with a scientific communication reason for the change. Reject cosmetic variants before the Drawer creates slides. Also compare equal-size grayscale thumbnails with style titles hidden; if their large-scale mass distribution and first focal point remain interchangeable, return the directions for redesign.

## Design connectors

- Route process flow through reserved lanes with few bends; choose orthogonal or curved routes appropriate to the scientific grammar.
- Connect from the side facing the destination and avoid immediate backtracking.
- Keep arrows outside unrelated shapes and labels.
- Separate parallel routes by a consistent lane gap.
- Avoid ambiguous crossings. For unavoidable network crossings, use clear separation, ports or bridges without changing topology.
- Distinguish process, inhibition, feedback, grouping, and association with consistent conventions.
- Reserve endpoint clearance so arrowheads touch a boundary without covering the target fill or text.

## Plan editability

Classify every planned element as editable text, shape, line, connector, table/chart, repeated motif, or irreducible raster evidence. Split any multi-image evidence block into one atomic image per field and plan its title, border, grid, legend, arrows, and annotations as editable objects.

## Produce the design handoff

Return a `design_spec` containing:

- canvas/slide geometry and layout tokens;
- region and object ids with bounds and styles;
- exact text and scientific topology;
- connector source, target, sites, waypoints, lanes, and arrow convention;
- for overviews, `narrative_map`, node-and-edge `abstraction_map`, independent edge `semantics`/`prominence`, physical publication width, effective font sizes, and named title/L3 objects for real review variants;
- the requested `execution` binding, and region-level visible changes with references to inspected assets in the existing evidence ledger;
- grouping and z-order;
- raster decomposition declarations;
- artifact mode (`direction_review` or `publication`), final display size, and figure archetype;
- the frozen `visual_grammar_receipt`, including the primary spine, dominant focal zone, role-to-shape mapping, two connector prominence levels, typography roles, semantic palette, grayscale plan, whitespace functions, forbidden motifs, reference firewall, and review sizes;
- `style_dna`, focal hierarchy, evidence weighting, and forbidden motifs;
- for a hand-drawn direction, its style family, controlled-imperfection budget, exact-versus-expressive line split, typography split, native doodle inventory, and style-source firewall;
- usable canvas bounds, meaningful-content hull, intended canvas-utilization range, and the function of each planned large whitespace region;
- an evidence budget for overview figures that states the placement and relative visual mass of representative real results, or the scientific reason no real evidence is available;
- for manuscript-derived work, source locations, Figure Claim, Paper Figure Signature, complete node/edge/operand/evidence ledgers, publication display width, permitted omissions, and any blind-exclusion receipt;
- for a blind comparison, allowed and sealed source sets, a pre-reveal freeze receipt, and the intended post-reveal comparison dimensions;
- when alternatives are requested, a style-divergence comparison showing why each direction is structurally distinct;
- local construction order and acceptance conditions.

Do not improvise geometry one object at a time after drawing begins.

## Enter the construction loop

Hand the design to `$edit-powerpoint-live` or `$recreate-scientific-figure-in-drawio`. After each region, require `$audit-scientific-figure`; when it finds a defect, require `$correct-scientific-figure`, return the object-level plan to the Drawer, rerender, and review again. For an overview, graphical abstract, teaser, final whole figure, or style-direction comparison, require the Reviewer to apply its publication aesthetic reference before approval.

Require source-faithful readable semantics at each assigned level, full reconstructable editability, no clipping or unintended overlap, and unambiguous routing in the current target-renderer evidence. Apply the Reviewer's `pass | fail | pending` evidence gates; self-assigned confidence thresholds are not acceptance evidence. For overviews, the actual title-hidden and title/L3-hidden grayscale views must support the intended reading logic. Complete contract coverage includes visible main groups and linked readable expansions; check positive and negative relations at their declared level. Missing target-renderer evidence leaves publication approval pending.

## Delivery

Save the editable source and requested exports. Report the selected backend, design tokens, object counts, raster declarations, local gates, whole-figure gate, and remaining content ambiguity.

For a completed blind comparison, also deliver the frozen source contract, frozen editable artifact and render, target attribution, and a post-reveal verdict that preserves what each design does better. Do not silently retrofit the blind artifact after seeing the target.

In `publication` mode, remove style numbers, reference-DNA labels, selection instructions, reviewer notes, and other direction-review scaffolding from the final figure.
