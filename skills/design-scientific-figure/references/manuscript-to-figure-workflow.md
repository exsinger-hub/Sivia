# Manuscript-to-Figure Workflow

Use this reference when the source of a new scientific figure is a manuscript, paper PDF, method section, equations, supplementary text, or an evidence pack rather than a short free-form brief. It also governs blind Figure Gym runs in which a target figure is sealed until after an independent design is frozen.

Preserve the manuscript's scientific argument in a figure whose visible topology can be reconstructed at publication size. For independent design, resemblance to an existing figure is not the objective. For a user-approved reference adaptation, composition fidelity is also part of the objective; the manuscript remains the authority for replacement scientific content.

## 1. Declare source authority and mode

Before extracting content, record:

- exact manuscript/PDF version and source locations;
- whether the task is ordinary design, reference-led reconstruction, or blinded independent design;
- which captions, figures, supplementary files, code, and evidence assets are allowed;
- which target figures or derivative assets are sealed or excluded;
- intended publication slot, final display width, and output formats.

In blinded independent design, do not inspect the target figure, its crop, its alt text, or layout-descriptive caption passages before the design is frozen. If reference retrieval is used, exclude the target paper and derivative assets before candidates are materialized. Use stable identifiers available for the paper, such as DOI, arXiv/OpenReview id, exact title, and canonical source URL; do not rely on title substring matching alone when a stable id exists.

Do not apply the exclusion rule to an ordinary redesign in which the user explicitly supplied the target figure as a reference.

## 2. Translate the paper, then scope the scientific contract

Start with the title, abstract, introduction's organizing argument and conclusion to identify what the paper asks the reader to understand. Read the relevant methods, equations, captions and results to establish how it works and what evidence actually supports it. Section order is a reading aid, not the figure's composition. For an allowed reference-led redesign, distinguish the source figure's argument from its particular arrangement of boxes.

Do the editorial pass below before a full object inventory. Then freeze the existing contract artifacts for the selected figure scope; do not turn every method operation into a required overview box.

### Figure Claim

Write one sentence stating what a reader must understand after viewing the figure. A list of modules is not a Figure Claim.

### Editorial pass: evidence to visual scene

Use a short working note or the existing `narrative_map`, not a second ledger system. Trace each proposed scene through four decisions:

**Source statement → editorial role → visible change → drawing instruction.**

1. **Choose the role.** Does this statement establish the problem, explain the distinctive mechanism, orient the reader within the system, or support an evidence claim? Keep essential explanation in the overview; group routine implementation, link necessary technical expansions, and leave unrelated detail in the manuscript. Record the reason, not a score. Preserve interpretation-changing conditions even when small.
2. **Show the scientific verb.** Replace a noun-only instruction such as "draw an alignment block" with objects and a relation the reader can see. For example, matched-scale fusion uses feature fields brought to the same spatial size; serialization uses a grid and token strip with traceable position identities; coordinate restoration returns responses to corresponding grid locations before combination. Which property changes, and which correspondence remains invariant? Do not imply unchanged feature values merely because position markers are retained.
3. **Assign visual carriers.** Use a real sample field for an input/evidence role, a grid or stack for a representation, an ordered strip for a sequence, and a visible merge, selection, reordering or boundary for an operation when scientifically appropriate. Text names what the picture already explains. A box remains useful for a component, but every scene must not collapse into interchangeable labeled boxes. Inspect available scientific assets before deciding what they can carry.
4. **Set emphasis from the argument.** Give explanatory space to the distinctive transformation, not to whichever equation is longest. Arrange the scenes only after their roles are clear. A diagnosis strip, system spine and evidence footer may suit an alignment paper; these are not mandatory rows for other papers.

A worked translation:

| Source statement | Editorial decision | Visible scene | Production instruction |
| --- | --- | --- | --- |
| A reverse response is flipped back, then inverse-mapped before fusion. | Make coordinate agreement the focal mechanism; keep routine normalization secondary. | Two responses with position markers return to matching spatial locations before a shared fusion node. | Draw separate forward and reverse lanes; on the reverse output place flip-back before inverse restoration; show two restored grids feeding the fusion. Markers denote positions, not identical values. |
| A spectral objective uses one target-derived support for prediction and target, only in training. | Keep this a subordinate training explanation, not another inference stage. | The target alone creates a support mask, which applies to both image branches before their profiles are compared. | Draw the mask-generation edge from the target only; connect the same mask to both branches inside a training-only region. |

### Learn from a successful prompt and its actual output

Inspect the manuscript, the prompt and the supplied result separately. Reconstruct the observable editorial transformation; do not claim access to the prompt author's hidden reasoning. Identify (a) which source claims were selected, (b) how prose became visible objects and changes, and (c) what the renderer added, omitted or altered. A pleasing result can teach composition while still containing scientific errors. Transfer its useful visual grammar without promoting those errors or its incidental panel count into rules.

Compile a production prompt in this order: figure purpose and one claim; scene roles and reading order; concrete objects, transformations and visual emphasis; exact labels and critical scientific boundaries; asset use and rendering instructions. Put positive, drawable scenes before negative style constraints. "Publication quality", "not a dashboard", or a long prohibition list cannot specify a composition by themselves. The same visual script must guide a native Drawer as well as any explicitly requested raster concept; selecting a different renderer does not repair a missing script.

For ImageGen-first production, use [ImageGen-first workflow](imagegen-first-workflow.md) to separate visual approval from native translation. Template-led generation and revision prompts must follow [ImageGen Prompt Detail and Length](imagegen-prompt-detail.md), including the exact-submitted-text length gate. The scientific contract is concise working material; it does not replace the required detailed generation prompt.

If a draft is rejected as visually weak, compare its visible scenes with the reference before adding styling rules. If the reference explains a transformation through geometry and the draft merely names it, repair that scene first. Do not compensate with more modules, smaller text or more evidence panels.

### Paper Figure Signature

Record:

- causal and data-flow topology;
- scientific novelty and intended first focal point;
- input, output, condition, supervision, state, operator, and evidence roles;
- training-only, inference-only, shared, updated, and frozen boundaries;
- overview/detail hierarchy;
- required real evidence and its scientific scope;
- publication slot and reading order.

When selecting references independently, derive the needed composition family from this signature before retrieval. Search for role-specific anchors for structure, mechanism, evidence, and visual language. When the user has already approved a reference layout, map source-grounded scenes into its regions and follow the approved-reference procedure in Fundamental Visual Grammar; adapt local fit where the science requires it rather than replacing the whole composition.

### Required-node ledger

For every node, record a stable id, exact label or notation, semantic type, source location, condition membership, visual priority, and whether omission is allowed. If omission is allowed, give a source-grounded reason.

### Required-edge ledger

For every relation, record a stable id, source node, target node, relation type, direction, condition, source location, and visual encoding. Include scientifically meaningful absent relations as negative-path checks when a false connection would change interpretation.

### Equation-operand ledger

For each equation that affects topology, conditioning, alignment, optimization, or update ownership, record:

- output quantity;
- all operands and operators;
- index or axis scope when it changes the operation;
- parameter sharing or independence;
- train/inference status;
- planned visual representation or an explicit reason it remains textual.

Do not silently reduce an operand-bearing relation to a module label. A missing conditioning operand, inverse mapping, alignment step, weighted contribution, or update target is a source-contract failure.

### Evidence ledger

For every proposed raster or empirical result, record producer/model stage, sample-level or paper-level scope, allowed claim, source binding, crop/atomicity declaration, and whether it is representative, quantitative, or schematic. Proximity, a shared frame, color, or a leader line must not imply a stronger claim than the ledger authorizes.

When project imagery exists, inspect relevant candidate fields before allocating evidence space. Extend their existing evidence-ledger entries with the inspected file/region, intended visual role and reuse decision. Choose among direct atomic insertion, crop with native overlays, native reconstruction, or omission; briefly state why. Filename discovery alone is not visual inspection. Keep provenance unresolved when the producer, sample pairing or model version cannot be established: a real modality illustration is not automatically a prediction, a geometric proxy is not a learned activation, and a historical result is not current-model evidence.

Build the mixed-media figure from those decisions: retain original image pixels and aspect ratios for data fields, and draw labels, axes, grid paths, outlines and connectors as separate native objects. Do not send empirical fields through a generative redraw and then present them as preserved data. Neither zero pictures nor a large native-object count is a quality objective. If suitable evidence is absent, show a clearly scoped mechanism or symbolic output instead of fabricating a result.

## 3. Freeze a direction before publication drawing

When alternatives are useful, keep them low fidelity. Compare equal-size, title-hidden grayscale skeletons. Directions must differ structurally as required by the main design skill; do not build full presentation pages for candidates that can be rejected from a skeleton.

For overviews, read [Overview Narrative](overview-narrative.md) and map every required node and edge through its `abstraction_map` to a visible main object, composite, linked readable inset, textual relation or source-grounded permitted omission. Internal repeated operations may share a composite with a faithful expansion. Preserve external ports, branch conditions, inverse order and parameter ownership. Complete contract coverage spans these levels; it is not one-box-per-node direct visibility. A data-flow edge cannot be replaced with nearby prose.

Derive the canvas ratio and type/evidence budgets from the intended publication slot. Do not default to 16:9. Record the final display width used for review. Any minimum text or evidence size is task-specific and must be declared in the design spec; do not reuse a pixel threshold from another paper without justification.

Build only the selected direction at publication fidelity unless the user explicitly requests multiple finished alternatives.

## 4. Review the visible artifact, not only its object graph

The final review needs both current structure evidence and a fresh renderer export.

At the declared publication display width:

1. identify every required main group and its linked expansions from the render;
2. reconstruct each positive relation at its assigned level from visible endpoints, direction and route, using the abstraction map for internal composite relations;
3. test declared negative paths, including misleading shared containment or leader lines;
4. verify that text and evidence meet their declared minimum size;
5. verify that training/inference and update/freeze semantics do not depend on color alone.

For overview review, first obtain an unprimed reading of an actual title-and-L3-hidden grayscale render, before revealing the Figure Claim or contract. Then inspect the full publication-size render and expansions. A connector id, correct source/target metadata, or zero deterministic findings is supporting evidence, not a substitute for visible-edge reconstruction. Record physical width and effective type size; a pixel thumbnail alone does not verify print readability.

Re-run the affected scale tests after every structural correction. Do not upgrade a verdict from a local geometry fix without refreshing the same evidence that originally failed.

## 5. Attribute and correct the earliest deviation

Classify a failure at the earliest stage where the correct information or relation was lost:

- `parse`: manuscript/equation/evidence extraction omitted or altered a fact;
- `spec`: the frozen contract contradicts the source or itself;
- `retrieval`: references introduced an incompatible topology or leaked the target;
- `direction`: the chosen composition flattened or merged required semantics;
- `draw`: implementation changed visible geometry, routing, text, or evidence binding;
- `review`: available evidence contained the defect but the Reviewer approved it.

Fix the earliest responsible artifact first, then regenerate only the affected downstream objects. Do not conceal an upstream contract defect with a terminal label, decorative cue, or raster replacement.

## 6. Optional blinded comparison

For the full sealed-target sequence, freeze receipt, comparison dimensions, and rule-promotion boundary, read [Blind Figure Gym Protocol](blind-figure-gym.md) completely.

After a blind artifact is frozen and passes its pre-reveal gate, reveal the source figure and compare:

- scientific semantics and causal topology;
- composition, hierarchy, and evidence integration;
- publication legibility, consistency, and editability.

Do not use pixel similarity as the primary verdict. Treat the published figure as a strong reference, not an infallible ground truth. Preserve both generated and original advantages, and attribute each failure to its earliest stage.

Promote a workflow rule only when it recurs across cases or prevents a severe scientific error, and only in a generalized form. Never promote case-specific node counts, edge counts, aspect ratios, pixel thresholds, palettes, or silhouettes as universal rules.
