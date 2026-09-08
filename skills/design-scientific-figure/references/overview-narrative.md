# Overview: scientific contract to readable argument

Use for research overviews, graphical abstracts, and dense method figures. Keep the complete scientific contract, but draw a hierarchy of explanations. Contract coverage is not a requirement to put every implementation operation on the main path.

## Choose what the reader learns

Write three short answers before coordinates or colors:

- **First glance (3 seconds):** input/problem, distinctive transformation, outcome, and dominant reading logic. A few semantic groups should carry this; their count is an editorial choice.
- **Working understanding (30 seconds):** the steps and conditions that explain why the mechanism works, including relevant branches, feedback and scope boundaries.
- **Technical inspection (3 minutes):** exact operands, local order, parameter ownership and source-bound evidence in readable insets or companion detail panels.

These are reading tasks, not measured timing claims. A comparison may need balanced arms; a biological circuit may need a cycle; a pipeline may need a left-to-right spine. Choose one dominant organizing logic. A focal region can contain multiple objects.

Every region answers a question: what enters, what changes, what matters, or what follows? A bottom strip or side region is useful when it has a specific role such as training, evidence, stages, variants or downstream use. Include it only when the scientific story needs it. An architecture-only brief may end at an output; do not invent experiments or applications to fill a closure panel.

Write each region as a short visual scene, not a module inventory: the question, the observable change, the objects showing that change, and any asset ids from the existing evidence ledger. For example, an alignment mechanism can preserve position markers while two traversal orders return to matching grid coordinates before fusion. The markers identify positions, not unchanged feature values. An evidence region instead shows the measured difference and its scope. Use problem–mechanism–evidence when the paper supports it, without imposing three rows or repeating the entire pipeline in a diagnosis strip.

## Make the abstraction explicit

Add `narrative_map` and `abstraction_map` to the existing `design_spec`; reference existing ledgers instead of copying them into more files.

```yaml
narrative_map:
  first_glance: "Evidence checks decide whether to revise, answer, or abstain."
  reading_logic: directed_spine_with_bounded_feedback
  entry: question
  focal_region: evidence_gate
  exit: supported_answer_or_abstention
  levels:
    L1: [question, retrieve, draft, evidence_gate, outcome]
    L2: [source_spans, repair_loop, retry_bound, frozen_weights]
    L3: [retrieval_inset, gate_inset]
  regions:
    - id: gate_inset
      question: "What makes a claim supported?"
      role: mechanism
      visible_change: "A candidate claim is linked to its source span; unmatched claims take the repair path."
      visual_carriers: [claim_text, source_span, correspondence_link, repair_branch]
      asset_refs: [] # ids in the existing evidence ledger, not duplicated provenance
  mandatory_visible_cues: [source_to_gate, supported_branch, retry_limit, abstain_branch]
  expected_reading:
    L1: "A question becomes a checked answer or abstention."
    L2: "Unsupported claims trigger bounded retrieval and revision; weights stay fixed."
    L3: "Candidate claims are checked against retrieved source spans."
  forbidden_readings: [retrieved_text_controls_policy, feedback_updates_weights]

abstraction_map:
  - contract_ids: [chunk, embed, search, rerank]
    visual_id: retrieve
    mode: grouped
    level: L1
    expansion: retrieval_inset
    invariant: "Retrieval returns evidence, never an instruction or weight update."
    source_ref: brief.retrieval
  - contract_ids: [claim_extract, span_lookup, support_check]
    visual_id: evidence_gate
    mode: inset
    level: L2
    expansion: gate_inset
    invariant: "Check candidate claims against retrieved source spans."
    source_ref: brief.checking
```

Map every in-scope node **and relation**, including operands and negative paths, to `direct`, `grouped`, `inset`, `textual` or `permitted_omission`. For grouped internal edges, identify the composite and expansion that preserve their order. An external edge still needs a visible endpoint and direction. Textual representation is suitable for a fixed scope label, equation or shared-parameter annotation; proximity of words cannot replace a data-flow edge.

`permitted_omission` needs a source-grounded reason. `grouped` is not an omission. Preserve exact input/output interfaces across every abstraction boundary. Do not merge operations when doing so hides distinctions in direction, conditions, update ownership, parameter sharing, evidence scope or inverse order. Keep a claim-critical transform/inverse pair visibly cued in the main mechanism; use its linked inset for indexing details. Likewise, a main-view boundary or state cue must expose critical train/inference and freeze/update distinctions. A generic “restore” label is insufficient.

Classify objects by scientific importance, not visual size. Train/inference, frozen/updated, branch conditions and other interpretation-changing cues belong to L1/L2 even when typeset small. They must survive the L3-removal review. Routine implementation details may move to L3. If required detail does not fit at final size, recompose or add an explicitly linked detail panel; do not shrink all text.

## Separate edge meaning from prominence

Extend the existing edge ledger with independent fields:

```yaml
id: unsupported_retry
source: evidence_gate
target: retrieve
semantics: feedback
condition: "unsupported and attempts < 3"
prominence: primary
must_survive_at: L2
label: "retrieve more evidence"
route_lane: return_lane
line_style: solid
arrow_convention: directed
```

`semantics` may be data, transform, inverse, supervision, update, feedback, association, inhibition or a domain-specific relation. `prominence` controls line weight/contrast; it is not the relation's type. A feedback edge can be primary. A leader to an inset is association, not data or causation, and normally has no directed arrowhead. Use dashed supervision, blunt inhibition, bidirectional exchange or shared-parameter brackets when supported by the science and a consistent visible convention.

## Explore the composition cheaply

For a new overview or rejected global composition, explore low-fidelity silhouettes before publication objects when useful. Compare the reading logic, focal mass, evidence placement and available type size. Do not build multiple polished variants unless requested. Select a direction using the user's established preferences. In the ImageGen-first route, the actual raster draft must be shown and approved before native reconstruction; a skeleton or design handoff does not substitute for that approval. If an approved reference already exists, continue from it rather than reopening composition selection.

Reference retrieval follows the scientific story. Extract one useful principle from a role-specific reference and record what is actually visible versus inferred. Low-resolution material can support composition analysis, not the reading of scientific labels or edge semantics. Hand-drawn cues are optional and should clarify a mechanism or human role. Do not impose a handwritten style on all scientific figures.

## Review physical size, not an arbitrary pixel count

Declare intended width in mm (or journal column width), aspect ratio and minimum effective text size. Compute:

```text
effective_font_pt = source_font_pt × final_width_mm / inserted_source_width_mm
```

Use the actual inserted crop width when the figure is cropped, otherwise the full canvas width. Choose the threshold from the publication requirement. If none is provided, start with 8 pt effective labels and 7 pt secondary annotations as a working assumption, then inspect the actual fit. These are starting values, not journal standards. A 600 px preview helps screen review but does not establish physical print readability; high export DPI does not rescue 4 pt labels.

## Reviewer evidence and order

Prepare actual full-color, title-hidden and title-and-L3-hidden images, plus grayscale versions of both hidden-title views. The reduced grayscale tests the main story; full-density grayscale tests whether retained detail disrupts it. Record renderer, source version/file, selected slide/page, physical width and exact removed object names. Removal must happen in disposable review copies; the editable final source retains all content. An ordinary render cannot be called title-hidden while its title remains visible.

The removal set includes an annotation's dedicated leader and decoration. A removable group must not contain surviving L1/L2 content. Check for orphan labels and free-line endpoints as well as attached connectors. If removing a detail changes the scientific main path, fix its level assignment; do not invent a simplified path only for the review copy.

1. Give an independent Reviewer the reduced grayscale image with a neutral filename and final size first. Withhold caption, notes, Figure Claim, ledgers, object counts and previous verdicts. Ask them to identify entry, focal transformation, outcome, main direction and uncertainty. Save their actual response. Next show the full-density title-hidden grayscale image and save whether their reading changes. Preserve both responses unchanged before revealing the intended story; append later comparisons separately.
2. Reveal the full color image and Figure Claim. Compare the recorded reading with the level-specific expected reading and forbidden readings (reference the existing negative-path ledger). Judge semantic agreement, not word-for-word matching, and inspect L1/L2 conditions.
3. Reveal source contract, abstraction map, detail panels and structure evidence. Reconstruct required relations at their assigned level, then inspect negative paths and editability.

Record prior exposure to the claim, draft, reference or full figure. A same-context Reviewer is `self_review`; an independent Reviewer already exposed to the story is `informed_review`, not unprimed. A blind response records observed meaning and uncertainty, not a grade against a hidden rubric. After reveal, compare it with the frozen expected reading and negative paths without rewriting it; keep this informed comparison separate. Blurring labels or hiding a legend does not require the reader to guess an exact acronym, mathematical claim or edge convention.

Preparing copies is not rendering them. An SVG made from the same coordinates is a design preview, not evidence of how a PPTX renders. When the target application is unavailable, keep target-rendering and dependent visual gates `pending`; deliver the editable candidate and name the missing evidence. Counts and numeric confidence never turn a pending gate into a pass.

## Regression scenarios

Test decisions on briefs with different scientific structures:

- **ML transform pipeline:** a frozen encoder, trainable decoder, train-only loss and exact inverse. The main mechanism and linked inset must preserve transform/inverse order and update scope after L3 removal.
- **Cell signaling:** compartments, inhibition, parallel branches and feedback. Preserve boundary crossings and edge meaning; a serial pipeline with generic arrows is wrong.
- **Parallel cohort study:** treatment arms, exclusions, loss to follow-up and observed outcomes. Keep arms and denominators traceable; illustrative participants cannot become empirical evidence or imply causal effects.

Use real output and reader reconstruction to judge each scenario. A schema-valid handoff or successful preparation script verifies only its own part of the workflow.
