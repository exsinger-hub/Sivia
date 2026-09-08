# ImageGen-first scientific figure workflow

Use for manuscript overviews whose production route is detailed prompt, ImageGen visual draft, user approval, editable reconstruction and local real-data replacement. It is the preferred new-overview route when ImageGen is available. An explicit native-only, prompt-only, read-only or already-approved-reference request keeps its own route. This workflow does not create permission to publish manuscripts or data.

The user-facing entry is the paper plus the desired figure, not a recital of these stages. Do not ask users to write a long ImageGen prompt or find a template as a prerequisite. When no external template is selected, use the [bundled templates](prompt-templates.md) after understanding the paper. Ask only for missing source content or a choice that materially changes the figure.

## Separate scientific authority from visual authority

- Manuscript, equations and verified implementation establish scientific facts. Resolve substantive disagreements from those sources; an attractive generated label is not a new fact.
- Bundled templates, a supplied knowledge library and role-specific references supply visual grammar. An explicitly approved image additionally fixes composition.
- ImageGen supplies a visual prototype, not measured results or preserved empirical pixels.
- Native PowerPoint/draw.io supplies editable translation and assembly, not a second opportunity to redesign an accepted composition.
- Real assets and computed geometry supply the relevant image/data fields. They do not require replacing every schematic with a photograph.

Keep source links and decisions in the existing design/reconstruction notes and evidence ledger. Do not duplicate them into new scoring systems or registries.

## 1. Extract a scientific argument

Read the relevant manuscript text, equations and code. Write one sentence explaining what the reader must understand, then map it into visible scenes using [Manuscript-to-Figure Workflow](manuscript-to-figure-workflow.md). Show scientific verbs: rearrange, select, restore, merge, compare or supervise. A noun-only list of modules is insufficient.

Inspect candidate real assets now, before allocating space. Establish sample pairing, producer/layer and allowed role. Reserve their locations during composition; insert the final fields after native reconstruction. Missing learned activations cannot be substituted with a resized input image or a different case's features.

For multiple figures, assign separate questions. An overview can orient the full method; a detail figure can explain a distinctive operation; a results figure can compare measurements. A training strip is appropriate only if it contributes to that figure's purpose. Do not automatically append evidence-status boards, geometry cards or auxiliary losses to every overview. Splitting an already approved figure needs user agreement.

## 2. Select a template and extract its style grammar

After the scientific argument is established, follow [Bundled Prompt Templates](prompt-templates.md) to select a complete overview or mechanism template unless the user already bound one. If a knowledge folder or reference image is supplied, inspect its relevant images and prompts; record the inspected items, not a claim that the entire folder was indexed. Select by communication role: overall story, mechanism explanation, evidence integration or visual language. Inspect the actual output together with its prompt when both exist. An absent local knowledge folder does not block a task that can use the bundled templates.

Translate the useful choices into drawing instructions: relative panel sizes, reading path, object scale, graphic density, typography, semantic color, connector conventions, spacing and visual carriers. A compact grid/sequence correspondence may be transferable; that source's index values, method topology or experimental results are not.

Use [Fundamental Visual Grammar](fundamental-visual-grammar.md). Tight composition means meaningful objects occupy their regions; it does not mean more paragraphs or decorations. Neither a fixed three-row layout nor a hand-drawn style is universal. For a user-approved reference, preserve the actual proportions and density rather than applying a sparse default template.

## 3. Write the complete production prompt

Read and follow [ImageGen Prompt Detail and Length](imagegen-prompt-detail.md). Bind the actual template, then specify purpose, composition, each region's contents, operations, exact labels/definitions, visual grammar, assets and preservation boundaries. Validate the exact tool-bound text against the template's length floor separately for each figure. Detail cannot be replaced by repetitive adjectives or invented science.

Keep printed labels short. Production prose explains where and how to draw; it is not text to be typeset inside the figure. Disclaimers, internal checkpoint labels, pending-work boards and reviewer notes stay out of a publication figure. Necessary operator definitions, scope boundaries and parameter relationships remain visible where interpretation depends on them.

When the user asks to see prompts first, present the complete prompts before calling ImageGen. Follow any requested approval pause. A prompt-only request ends at the prompt; it does not authorize generation.

## 4. Generate, inspect and lock the visual draft

Use the available image-generation tool and its required image skill. Inspect local image references before attaching them. Preserve both the exact prompt and returned image. Review the complete image for scientific topology, reference fidelity, density, hierarchy and label accuracy. Do not claim that saving a prompt or preparing a script is an executed generation test.

Present the visual draft for approval before native reconstruction. If it is rejected, diagnose the concrete scene that failed; refine the full prompt rather than automatically adding modules, plots or smaller text. Use a full revised prompt that still passes the bound length floor, even for a small raster edit.

Once approved, record the reference path/version, region bounds, proportions, styles, main routes and permitted content corrections. If the user has already approved an image, reuse that approval and skip regeneration. Visual approval does not validate invented numbers or fabricated data; identify source discrepancies and handle them according to whether faithful copying or scientific adaptation was requested.

## 5. Reconstruct faithfully as editable objects

Enter `$recreate-scientific-figure` with the approved reference and source-grounded content decisions. The selected native Drawer recreates text, operators, feature stacks, grids, tokens, arrows, tables and reconstructable charts as native objects or editable composites. Each irreducible image field remains a separate picture with native labels and overlays.

Keep canvas ratio, panel proportions, spacing, object scale, palette and connector routes consistent with the accepted image. Compare fresh native-renderer exports with the reference at equal display size. Do not replace dense scientific glyphs with generic empty boxes or treat a whole-slide PNG embedded in PPT as editable reconstruction.

## 6. Replace only fields that benefit from real sources

| Field | Production decision |
| --- | --- |
| Input, target and prediction images | Insert paired source fields with appropriate, documented display treatment; preserve aspect ratio and medical orientation. |
| Scan paths, index mappings and matching snapshots | Compute from the actual algorithm/settings, then draw the path or table as native objects inside the existing frame. |
| FFT and quantitative profiles | Compute from the bound images/data; retain atomic spectral fields and editable axes, curves and labels where reconstructable. |
| Learned feature maps | Require a real tensor from the relevant sample and model stage, with consistent projection/display for comparisons. |
| Token strips, reversal and coordinate markers | Keep symbolic when their purpose is order or position identity; matching positions do not imply identical activations. |
| A brain or other context icon | Replace only if a real field improves the explanation without suggesting that raw input is a learned tensor. |

Do not mix samples or model stages through proximity. Preserve the surrounding approved geometry when inserting a field. If a source is unavailable, retain an appropriate mechanism schematic, omit the empirical claim or request the missing asset; do not generate evidence-like pixels as a substitute.

## 7. Verify the requested scope and deliver

Separate scientific correctness, visual/reference fidelity and editability. Inspect both native structure and a fresh renderer export. New final figures use the applicable publication-size and narrative checks. Local edits use scoped regression: check the changed objects and necessary interfaces plus the whole image for unintended changes. Report inherited issues separately; local success does not certify untested publication readability.

After approval, micro-edits may change only named text, values, atomic assets and necessary local fit. Split, merge, canvas resize, reordering and global restyling require a separate agreement. If a readability problem needs a larger change, explain it and propose that change rather than executing it under the label of cleanup.

Deliver the requested editable source and exports, with the complete prompt and concise source/change notes in the working output folder. Keep production notes outside the figure. Do not upload the manuscript, private knowledge library or empirical data merely because the plugin itself is being published.
