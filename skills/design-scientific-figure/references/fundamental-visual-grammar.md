# Fundamental Visual Grammar

Use this reference for every publication-facing scientific overview, architecture figure, workflow, mechanism diagram, graphical abstract, or substantial aesthetic redesign. Read it before publication drawing starts. The purpose is to freeze the visual logic that makes the scientific claim readable before choosing decorative details.

## First principle

A scientific figure expresses an argument through information roles, visual mass, spacing, line behavior, type and color. For overviews, [Overview Narrative](overview-narrative.md) defines how the scientific contract becomes a multi-level explanation. Use that narrative to choose a grammar; the examples below are defaults, not a universal template.

The reader should be able to identify, without the title:

- where the story begins;
- what the scientific novelty or decisive mechanism is;
- how the main path proceeds;
- which information is supporting context, a skip, evidence, or training-only metadata;
- where the story ends.

For a new design, if those answers are unclear at thumbnail scale, repair the composition before cosmetic refinement. For an already approved reference or a micro-edit, report the concrete reading problem and propose a separate structural change; the rules below do not override the user's layout lock.

## Learn rules from references, not templates

### When the user has already approved a reference composition

Treat the selected image's layout as a task constraint, not merely a mood reference. Distinguish faithful reproduction (preserve its visible content) from manuscript adaptation (preserve its composition and visual language, replace content from the paper). If both are requested, deliver separately named artifacts so content corrections are not passed off as faithful copying.

Read its aspect ratio, relative band heights, column widths, exterior padding, gutters, text-to-graphic balance and local object scale. Record these in the existing design or reconstruction specification. Fill each region with the actual scientific objects and transformations before adjusting local fit. Dense feature stacks, grid/sequence correspondences and real evidence fields can carry explanatory content that a few labeled rectangles cannot.

Preserve substantial mechanism regions and populated support panels. Emphasis can come from reading order, typography and contrast; the main pipeline need not occupy the greatest area. If a region feels empty, enlarge or arrange its meaningful objects, reclaim unneeded panel space, or bring an already in-scope explanatory relation into view. Do not fill it with decorative objects, repeated prose or invented experiments. If crowded, shorten repeated wording and adjust local widths while preserving readable scientific relations.

Compare the actual complete render with the approved image at equal display size. An unfilled wireframe cannot establish comparable graphic density. Judge grouping and focal clarity in context: approved dashed panels, balanced columns and narrow bold header bands are not defects merely because a default style heuristic discourages them. Reference-specific proportions belong to this task, not a universal template for every paper.

On a micro-edit, freeze canvas size, region bounds, relative scales, typography, palette, major routes and unaffected objects. Apply only named text/data/asset changes and their necessary local fit. Do not use publication-size concerns, general anti-dashboard rules or an aesthetic finding to split, merge, resize or rearrange approved panels without user agreement. Report real inherited defects separately; a local regression pass does not certify the whole figure for publication.

### When independently selecting references

Retrieve references by communication role rather than by superficial resemblance. Useful roles include:

- **story reference**: how a method becomes a short visual narrative;
- **mechanism reference**: how one technical operation is isolated and explained;
- **evidence reference**: how real outputs or measurements are integrated without overwhelming the method;
- **visual-language reference**: how line, type, icon, and restrained hand-drawn cues create a coherent voice.

For every selected source, record:

```text
source:
role:
transferable_abstractions:
forbidden_transfer: topology | wording | coordinates | source-specific iconography | result values
```

Transfer only abstract decisions such as “one recognizable mechanism glyph,” “a single continuous reading spine,” or “secondary context recedes.” Never transfer the source's scientific topology, labels, coordinate arrangement, or distinctive composition into an unrelated figure.

Representative role anchors include [SWE-agent](https://arxiv.org/abs/2405.15793) for a compact method story built from recognizable native glyphs, [Mamba](https://arxiv.org/abs/2312.00752) for isolating a mechanism with whitespace and a repeated grammar, and [SAM 2](https://arxiv.org/abs/2408.00714) for separating a dominant trunk from supporting context and decoding. These are analysis anchors, not templates.

## Freeze a visual-grammar receipt

Before the Drawer creates publication objects, add a `visual_grammar_receipt` to the design specification containing:

```yaml
visual_grammar_receipt:
  claim_in_one_sentence:
  primary_reading_spine:
  entry_and_exit:
  dominant_focal_zone:
  hierarchy_levels:
  role_to_shape_mapping:
  connector_prominence_levels:
  typography_roles:
  semantic_palette:
  grayscale_plan:
  meaningful_content_hull:
  whitespace_functions:
  evidence_role:
  expressive_layer_if_any:
  forbidden_motifs:
  reference_firewall:
  review_sizes:
```

Do not accept placeholders such as “clean,” “modern,” “professional,” or “paper style.” Every field must constrain a visible decision. Do not enter publication drawing until the receipt and the scientific node/edge contract agree.

## Compose one primary sentence

- Use one dominant organizing logic, such as a reading spine, cycle or parallel comparison, selected from the scientific topology.
- Give one zone the largest semantic and visual importance. This is normally the novel mechanism, decisive comparison, or principal result—not merely the largest enclosing box.
- Organize first-glance, working and technical reading into L1/L2/L3. Interpretation-changing conditions remain L1/L2 even when drawn small.
- Let secondary branches leave and rejoin the spine locally. Avoid routes that orbit the entire canvas.
- Size content for the declared publication slot. Large empty regions must separate hierarchy, protect the focal zone, reserve a connector lane, or frame evidence.
- Use grouping backgrounds only when they express a real scientific boundary. Do not place every stage inside an equal-size card.

The meaningful-content hull should occupy the canvas confidently without crowding. If the figure could be enlarged substantially while preserving all routes and margins, the content is probably underscaled.

## Map information roles to different shapes

Use a stable role grammar:

| Information role | Preferred representation | Avoid |
| --- | --- | --- |
| Operator or transformation | concise bounded shape with a verb or recognized operator name | a large card containing paragraphs |
| Feature, state, or tensor | port, strip, token sequence, band, or compact labeled state | another operator-shaped box |
| Focal mechanism | a distinctive but simple native glyph plus nearby operators | an oversized generic rounded rectangle |
| Evidence or output | atomic field, chart, mask, image, or comparison with a restrained frame | a UI card pretending to be evidence |
| Context or metadata | small detached note, tab, brace, or quiet label | a full-width footer competing with the method |
| Group or scope | whitespace, shared baseline, subtle wash, or one light enclosure | nested dashboard panels |

A reader should be able to distinguish “something happens,” “a representation exists,” and “this is evidence” before reading the labels. Do not encode every noun as the same rounded rectangle.

## Separate connector semantics and prominence

All semantic routes must remain exact even in a hand-drawn direction.

Start with two line-weight/contrast levels, primary and secondary; use tertiary prominence only when needed for annotations. Separately assign relation semantics and a visible convention: data flow, supervision, feedback, update, sharing, association or inhibition. A feedback loop can be primary. An inset association should not look like a causal or data arrow.

Color may distinguish semantic families, but line prominence must still work in grayscale. Keep bends few, reserve lanes, enter the destination from the facing side, and maintain arrowhead clearance. A long skip should travel behind or below the main content and re-enter locally. Never route a line through a label, unrelated object, or focal glyph.

Dashed supervision or correspondence, blunt inhibition, brackets for sharing and curved feedback are valid when their meaning is explicit and consistent. Judge exact endpoints and unambiguous interpretation, not whether every line is solid.

## Limit typography

- Use sentence case for labels and headings unless the source requires an acronym.
- Start with two font weights and three functional sizes: figure/section, operator and annotation. Derive effective sizes at the physical publication width; adapt to notation and publication requirements.
- Make hierarchy through position, size, and whitespace before using bold or color.
- Keep labels short enough to remain readable at the declared publication width. If text does not fit, rewrite or recompose; do not solve the problem by shrinking all type.
- Avoid all-caps section banners, repeated pill labels, decorative microcopy, and UI-like status chips.

## Make color semantic

- Start with a neutral canvas and one ink color.
- Add a small semantic palette, normally two to four accents, and keep each color's meaning stable.
- Concentrate the strongest saturation near the dominant focal zone or a scientifically important distinction.
- Do not use a different color for every box and do not rely on hue alone for topology.
- Check a title-hidden grayscale version. The main spine, focal zone, and primary/secondary distinction must survive.

## Keep hand-drawn character restrained

Hand-drawn style is an expressive layer over exact scientific geometry.

- Keep macro alignment, semantic connectors, arrowheads, and text bounds crisp.
- Place stronger expressive cues only on the focal mechanism, one narrative transition, small native doodles, or restrained emphasis marks.
- Use controlled asymmetry, not random jitter.
- Do not add paper textures, raster overlays, global roughness, double outlines on every object, or deliberately crooked semantic routes.

If removing the expressive layer leaves an ordinary card-based flowchart, the style grammar is incomplete. If the expressive layer makes topology or labels less clear, it is too strong.

## Anti-dashboard rejection gate

Reject the composition and return to the Designer when its global silhouette is dominated by any combination of:

- equal-weight rounded cards for every stage;
- repeated pills, tabs, chips, or UI chrome with no scientific role;
- a full-width footer that competes with the main mechanism;
- long dashed skip rails spanning the canvas;
- all-caps bold typography at multiple levels;
- nested background panels used only to fill space;
- an icon swarm with no stable role grammar;
- a focal point created only by brighter color rather than structure.

Judge the actual reading failure, not motif presence alone. Scope containers, balanced experiment arms and a bottom evidence/training strip are useful when science requires them. A motif becomes a class-A failure when it obscures the organizing logic or focal hierarchy. Then replace the silhouette, redistribute visual mass and remap roles before surface polish.

## Review at three scales

Use fresh renders from the selected backend whenever available.

1. **Title-hidden thumbnail**: judge silhouette, first focal point, and reading direction. If the figure reads as a card wall or the first focus is wrong, redesign globally.
2. **Declared physical publication width**: verify effective type size, main groups and readable expansions. A 600 px screen preview is useful but cannot establish print readability.
3. **Title-and-L3-hidden grayscale**: verify hierarchy and routing without color. Actually remove the named objects in review copies and export them; a full render with a visible title is not this test.

At readable scale, inspect text fit, connector endpoints, line crossings, repeated alignment and local finish. Follow the unprimed review order in Overview Narrative. Passing object-structure checks does not override a failed reading test or supply missing target-renderer evidence.

## Correct in dependency order

Apply corrections in this order:

1. scientific contract and missing relations;
2. global silhouette, reading spine, and focal hierarchy;
3. region proportions, content hull, and whitespace;
4. role-to-shape grammar and connector lanes;
5. typography and semantic color;
6. decorative or hand-drawn finish.

When a higher layer changes, rerender and reassess dependent lower layers. Do not polish a local object while a class-A global defect remains.

## Acceptance

The fundamental grammar passes only when:

- the figure communicates one primary scientific sentence;
- the novelty or decisive result is the first focal point without relying on the title;
- operators, features, evidence, and metadata are visually distinguishable;
- primary and secondary routes remain clear in grayscale;
- no anti-dashboard class-A defect remains;
- the declared publication-width and grayscale renders preserve the intended hierarchy;
- reference influence is traceable to abstract visual traits and does not copy scientific content or topology.
