# Bundled prompt templates

These complete templates ship inside Sivia. They are internal production resources, not commands that users must paste. A paper and a request for an overview are enough to start. Read the paper first; select a template for the scientific question second.

The [public visual knowledge base](../../../knowledge-base/README.md) ships six topic-specific **actual ImageGen image + full submitted prompt** cases. After understanding the scientific argument, inspect both the relevant `figure.png` and `prompt.txt`, plus the case notes and any reference input. An image alone or a long screenshot is not a complete generation case. Use the full text templates below for the default length baseline; when the user explicitly selects a knowledge-base case, its complete prompt is the baseline, not a summary. Preserve all relevant scene detail and the user's approved layout. Generated examples are not user-approved examples unless approval is explicitly recorded. Do not require access to the original local collection when the bundled case is available.

## Choose by figure role

| Role | Full template | Use |
| --- | --- | --- |
| Method overview | [overview-template.txt](templates/overview-template.txt) | Orient the reader to the problem, distinctive transformation and complete input-to-output method. |
| Mechanism detail | [mechanism-template.txt](templates/mechanism-template.txt) | Explain one construction, correspondence, branching operation, restoration or aggregation at closer reading depth. |

These are roles, not mandatory Fig.1/Fig.2 assignments. One requested overview does not authorize producing two figures. If a paper uses a different scientific topology, instantiate the relevant role with that topology; do not import SBF-Mamba modules or require three rows. Preserve the user's explicitly bound template and any already approved composition ahead of these defaults. An explicit native-only or reference-reconstruction task does not acquire an ImageGen step merely because templates are available.

## Compile after understanding the paper

1. Read the paper using the [manuscript workflow](manuscript-to-figure-workflow.md). Establish the research problem, actual limitation, contribution, method dependencies and evidence. Write a concise Figure Claim and decide the figure's scope before choosing its silhouette.
2. Read the selected template completely. Its bracketed fields are authoring slots for the assistant. Resolve them from source-grounded scenes, notation, available assets and the chosen composition. Users do not fill these slots.
3. Rewrite conditional sections into concrete instructions for this figure. Remove inapplicable training strips, branches, counterexamples or quantitative panels; expand the relevant scene geometry and relationships instead. The final prompt must contain no unfilled authoring slots, alternative layouts awaiting selection or SBF-specific facts imported from a reference.
4. Save the full instantiated prompt in the task's output folder. Check its exact submitted text against the selected full template with [the length checker](../scripts/check_prompt_length.py), following [Prompt Detail and Length](imagegen-prompt-detail.md). Keep the original template unchanged as the baseline. Do not use the short README example as the production prompt or lower the baseline after deleting optional material.
5. Generate and inspect the visual draft, then obtain the requested visual approval before editable reconstruction. If a visual has already been approved, retain that layout and approval rather than restarting generation. Authentic image/data insertion remains a local operation within that layout.

The two templates contain **15,356** and **17,973** non-whitespace Unicode characters respectively. Both are longer than the historical combined Web prompt (**12,021**) from which the SBF-Mamba figure work began. These are full production-detail templates, not heading-only outlines. Compare against the actual installed file at execution time; numbers in this document do not substitute for checking the submitted prompt. An externally selected longer template still takes precedence.

## What was learned and retained

The templates were distilled from the locally saved SBF-Mamba prompt history, the user's reference collection at `D:/Desktop/zuotuzhishiku`, and the subsequent figure revisions. The original combined prompt is retained in the working project's `output/overview-test-20260905/web-original-overview-prompt.txt`; it was not previously bundled with the plugin. The revised overview prompt was in `output/fig1-revision-20260906/fig1-revised-prompt.txt`, and the companion mechanism source was in `output/web-prompt-trial-20260906/fig2-source-prompt.txt`. Those local paths describe provenance; an installed Sivia does not need access to them.

Transferable visual choices include concrete grids/stacks/sequences instead of noun-only boxes; a larger focal mechanism; nonuniform region widths; compact occupied regions with deliberate connector lanes; short technical labels; restrained role-based fills; and atomic empirical image fields. The local library included compact mathematical narratives, pastel modular method boards, restrained technical sketches and neural-framework diagrams. Select a coherent visual family instead of mixing their conflicting typography and panel arrangements.

The root README displays all six generated knowledge-base cases, each paired with its full prompt. The SBF-Mamba [overview](../../../assets/examples/sbf-mamba-fig1.png) and [mechanism](../../../assets/examples/sbf-mamba-fig2.png) are retained as historical project assets, not README examples. They are visual anchors, not universal scientific templates or proof that the newly generalized templates have been generation-tested. Inspect them only when relevant and allowed; exclude them in a blinded SBF-Mamba design task. A source-grounded correction takes precedence over an incidental generated label or route.

When a user approves a new visual, retain its actual full prompt, corresponding image, reference inputs and useful feedback as a new local case. Record visual approval separately from scientific validation. Promote transferable composition rules, not paper-specific modules or unverified metrics. Public contribution is a separate step requiring permission; invite the user to share a publishable pair through the knowledge-base contribution guide rather than automatically uploading future private work.

The new templates intentionally do not inherit the old evidence-status board, automatic geometry footer, repeated claims of bijection, fabricated numerical entries, unverified medical windows or fixed SBF-Mamba architecture. They retain the prompt's useful way of describing a picture: purpose → visible objects → transformation → correspondence → composition → concise labels → rendering detail. Permission to publish the current knowledge-base cases does not authorize publishing other manuscripts, future private cases or empirical arrays; follow the public knowledge base's source and contribution guidance.
