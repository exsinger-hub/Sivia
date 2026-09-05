# Overview workflow validation

This update was tested through a text-design comparison, three scientific structures, a native review-copy helper and an editable figure exercise. These verify particular workflow behaviors; they are not a benchmark establishing publication aesthetics across papers.

## Observed baseline and changed behavior

An independent designer used the previous instructions on a retrieval-agent brief with an evidence gate, bounded revision, fixed model weights and no empirical data. The baseline already grouped implementation operations appropriately, chose the evidence gate as the focus and declined to invent the missing identities in a stated 22-node inventory. Therefore the update does not claim that the old instructions could not abstract.

The same text task with the updated instructions produced these differences:

| Decision | Before | After |
| --- | --- | --- |
| Contract mapping | Implementation nodes grouped, consequential edges retained | Nodes **and edges** mapped across main groups and linked expansions, including internal order |
| Key feedback | Automatically thinner than the progression | Primary prominence because revision is central to the Figure Claim; semantic type remains feedback |
| Critical cues | Present in the planned figure | Also excluded from the actual L3 removal set |
| Print size | Reasonable physical size and type choices | Explicit effective type calculation using the inserted crop width |
| Visual review | Requested title-hidden/grayscale views with confidence thresholds | Actual review copies, unprimed staged reading, source comparison and evidence verdicts |

Both design handoffs were text-only. No visual pass was inferred from either. Full-density grayscale review was added subsequently so removing detail cannot conceal a cluttered final figure.

## Counterexamples exercised

- **Transform pipeline:** preserve transform/inverse order, frozen/trainable ownership and train-only supervision; use an inset for index and repeated-layer detail.
- **Cell signaling:** the updated designer retained parallel branches, compartments, activation and blunt inhibition; it did not invent a convergence or force a serial pipeline.
- **Observational cohorts:** it retained parallel longitudinal lanes, exclusion and loss-to-follow-up branches, cohort identity and denominator provenance; it did not invent counts, randomization or causal effects.

The latter two are design exercises, not rendered domain examples. Their purpose was to check that pipeline-specific style advice does not overwrite the scientific structure.

## Review-copy implementation

```sh
python -B -m unittest discover -s tests -p test_prepare_overview_review.py -v
node --test tests/*.test.mjs
```

The final helper passed 16 targeted tests, including actual title/detail removal, nested groups, unchanged source/package parts, reordered slide relationships, unknown or duplicate names, dangling connector references and output overwrite rejection. A read-only code review found that native ink plus fallback pictures could be only partly removed. Four additional regression tests cover selected alternate representations and preservation of unselected alternate content; the implementer observed failing cases before adding the rejection. The existing 23 Node contract tests passed. The 16 helper tests were also run from the final installed plugin cache, verifying that installation contains the working helper and its references.

Preparing copies deliberately emits `renderer_status: pending`. Actual renderer exports and a reader's observed interpretation are separate evidence.

## Editable exercise

The [evidence-gated overview](evidence-gated-overview/) applies the revised instructions to a schematic retrieval agent. It uses no empirical performance claims. Its design, editable source and renderer evidence are separate from the text-design comparison above. Consult that exercise's review record for the current visual verdict and any remaining issue.
