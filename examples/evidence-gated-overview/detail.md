# Evidence-gated retrieval agent

The [single-slide figure](../../assets/examples/evidence-gated-overview.pptx) maps a user question to a candidate answer, then makes cited-claim support the condition for release, revision, or abstention. The small `a` and `b` references connect the main groups to the two explanations on the same slide. This document expands their interfaces without adding a second slide.

## Retrieval

Detail `a` separates index preparation from online retrieval. Preparation chunks the source material, embeds the chunks, and stores the searchable representations with their source text and provenance. This creates an index; it does not train or update a model.

At inference, the question conditions index lookup. Reranking produces the passages used to draft an answer. Source text and provenance remain available so cited spans can also enter the checker. The raised source-span route depicts that evidence input separately from the draft-to-checker route.

## Drafting

Detail `b` expands the draft/revise group: prompt assembly, generation, and claim parsing. The assembled prompt contains the user question, the retrieved evidence, and the agent's task instructions. Retrieved text has evidence status throughout; its contents never acquire instruction authority. The user question remains part of the online task context even when it is not redrawn on every edge.

Generation produces a candidate answer. Parsing produces cited claims and their cited source references. The checker compares each cited claim against the corresponding source span. The glyph's claim and span strips are abstract editable operands, not examples of measured results. Release requires support for every cited claim. The brief does not specify an entailment algorithm or claim-completeness criterion, so the figure does not invent either.

## Attempts

One attempt is one draft/check cycle. The initial cycle is attempt 1. If every cited claim is supported, return the supported answer with citations. If any cited claim remains unsupported and fewer than three attempts have occurred, retrieve more evidence, revise, parse the revised claims, and check again. If support is still incomplete at attempt 3, abstain. Thus the figure allows at most three total attempts, including the initial one.

The rust route represents control feedback and carries unresolved support needs into additional retrieval. It never denotes a parameter update. All model weights, including any learned retrieval, reranking, generation, or checking components, remain frozen.

## Logging

Logging may record operations and outcomes. It has no causal role in the specified evidence gate and is therefore omitted from the figure, as permitted by the brief's classification of logging as an implementation detail.

## Source and scope

The scientific source is the synthetic regression brief defined for this plugin test (B1–B6), recorded in [design-spec.json](design-spec.json). Its `abstraction_map.nodes` and `abstraction_map.edges` map the contract to visible objects, grouped expansions, fixed scope annotations, or an explicitly permitted omission. Each relation records semantics independently of line prominence. The main diagram retains evidence status, frozen weights, support conditions, retry bound, and abstention when L3 detail is removed. No external experimental evidence, measured performance, checker accuracy, or empirical results are claimed.
