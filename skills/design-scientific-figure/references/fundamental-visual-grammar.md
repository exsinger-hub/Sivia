# Fundamental Visual Grammar

Use this reference for every publication-facing scientific overview, architecture figure, workflow, mechanism diagram, graphical abstract, or substantial aesthetic redesign. Read it before publication drawing starts. The purpose is to freeze the visual logic that makes the scientific claim readable before choosing decorative details.

## First principle

A scientific figure is a visual sentence, not a collection of labeled containers. Its style is the repeated relationship between information roles, visual mass, spacing, line behavior, type, and color. A palette or font change cannot repair a weak sentence.

The reader should be able to identify, without the title:

- where the story begins;
- what the scientific novelty or decisive mechanism is;
- how the main path proceeds;
- which information is supporting context, a skip, evidence, or training-only metadata;
- where the story ends.

If those answers are unclear at thumbnail scale, redesign the composition. Do not proceed to cosmetic refinement.

## Learn rules from references, not templates

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

- Use one dominant reading spine: left-to-right, top-to-bottom, or a clearly labeled cycle.
- Give one zone the largest semantic and visual importance. This is normally the novel mechanism, decisive comparison, or principal result—not merely the largest enclosing box.
- Keep at most three hierarchy levels: primary claim, supporting stages, and annotations or metadata.
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

## Use two connector prominence levels

All semantic routes must remain exact even in a hand-drawn direction.

1. **Primary flow** carries the main scientific sentence. Use the strongest solid line and the clearest arrowheads.
2. **Secondary flow** carries context, skips, supervision, or local returns. Keep it solid unless dashing has an explicit scientific meaning; reduce contrast and visual mass rather than creating a dashed railway.

Color may distinguish semantic families, but line prominence must still work in grayscale. Keep bends few, reserve lanes, enter the destination from the facing side, and maintain arrowhead clearance. A long skip should travel behind or below the main content and re-enter locally. Never route a line through a label, unrelated object, or focal glyph.

Use dashed lines only when the scientific semantics genuinely mean optional, latent, uncertain, proposed, or otherwise non-solid relation. Do not use dashes merely to make a crowded route look lighter.

## Limit typography

- Use sentence case for labels and headings unless the source requires an acronym.
- Use no more than two font weights and three functional sizes: figure/section, operator, and annotation.
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

These are class-A composition failures. Do not respond by changing palette, corner radius, shadows, font family, or line texture. Replace the silhouette, redistribute visual mass, and remap roles to shapes first.

## Review at three scales

Use fresh renders from the selected backend whenever available.

1. **Title-hidden thumbnail**: judge silhouette, first focal point, and reading direction. If the figure reads as a card wall or the first focus is wrong, redesign globally.
2. **Declared publication width**: use the actual target; use 600 px as a practical fallback when the target is unknown. Verify that every required stage and relation remains legible.
3. **Title-hidden grayscale, approximately 400 px**: verify hierarchy and primary/secondary routing without color.

At readable scale, inspect text fit, connector endpoints, line crossings, repeated alignment, and local finish. Passing object-structure checks does not override a failed thumbnail or grayscale judgment.

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

