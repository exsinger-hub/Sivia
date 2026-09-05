# Evidence-gated overview forward test

The frozen deliverable is [evidence-gated-overview.pptx](../../assets/examples/evidence-gated-overview.pptx), a single native PowerPoint slide at 170 × 80 mm. The matching [evidence-gated-overview.png](../../assets/examples/evidence-gated-overview.png) is an actual PowerPoint export. The current corrected review set is `review/v3/`. Original `review/v1/` and `review/v2/` files are preserved. The source attribution is the synthetic regression brief defined for this plugin test (B1–B6). Reproduction runs write to new directories and do not replace these files.

## Files

- `design.mjs`: generates the frozen backend-neutral handoff, review plan, and coarse composition study before slide construction.
- `design-spec.json`: exact object names, geometry, text, visual grammar, source clauses B1–B6, narrative map, node/edge abstraction map, and explicit assumptions.
- `detail.md`: scientific explanation of the linked a/b expansions and the three-attempt interpretation.
- `generate.ps1`: native PowerPoint COM generator, target renderer, helper invocation, and raw structure inventory.
- `review-plan.json`: exact annotation names supplied to the repository review-copy helper.
- `make-review-images.py`: grayscale and 850-pixel previews derived from both actual PowerPoint variant renders.
- `verify-reproduction.py`: compares the retained v2 baseline with v3 pixels, native structure, and corrected notes; writes `review/v3/reproduction-check.json`.
- `silhouettes.svg`: coarse composition study only; not target-renderer evidence.

## Review order and renderer evidence

In `review/v3/`, `view-01-gray.png` is the actual title-and-L3-hidden view converted to grayscale. `view-02-gray.png` is the title-hidden view with full detail density. Their color sources are `view-01.png` and `view-02.png`. The `-gray-850.png` files are screen previews of the same images. The helper-generated editable copies are `detail-hidden.pptx` and `title-hidden.pptx`.

`renderer-evidence.json` records PowerPoint version/build, native dimensions, timestamps, exact export paths, shape counts and text bounds. `structure.json` records native object geometry and connector attachment. `derived-image-evidence.json` records the source of each grayscale image. The helper's `review-manifest.json` deliberately retains its preparation-only `pending` renderer field; actual export evidence is separate.

The completed [independent reading record](review/independent-reading.md) preserves reduced and full-density grayscale readings before revealing the claim. Both recovered the intended mechanism. The [final audit](audit-report.md) combines those observations with actual source-package and rendering checks, including the v2/v3 continuity evidence.

The first actual render exposed connectors crossing the policy note and checker label, plus the wrong octagon connection port. The corrected source uses an explicit left-boundary abstain endpoint, a route below the policy note, and a source-to-check route around the label into the top of the circle. The supported branch is horizontal. The text-bounds measurement alone did not detect those connector defects. This is a construction correction record, not an independent review or aesthetic score.

Intermediate v2 preparations and repeated reproduction trials are retained locally but excluded from the published example. The repository preserves v1 diagnostic, v2 reader-tested and v3 final evidence. Use only `review/v3/` for the current source.

## Reproduce

Requirements: Windows, installed Microsoft PowerPoint, Arial, PowerShell with COM support, and bundled Python with Pillow. `generate.ps1` reads the checked-in `design-spec.json` and `review-plan.json`; it does not require a JavaScript presentation package. The repository helper is `../../scripts/prepare-overview-review.py`.

The optional `-PythonExe` parameter defaults to `python` on PATH. Run from this directory in PowerShell, using a new review directory name. The example overrides Python with the bundled path supplied by `load_workspace_dependencies`:

```powershell
.\generate.ps1 -ReviewVersion 'repro-next' -PythonExe 'C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& 'C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' .\make-review-images.py .\review\repro-next
```

This produces `review/repro-next/source.pptx`, `full.png`, both native review copies, color and grayscale views, and structure/renderer/session records. A pre-existing run directory is rejected before PowerPoint is accessed. The generator renders through `PowerPoint.Slide.Export` at 2040 × 960 pixels and leaves its new source in a visible document window. Existing presentations, including the publication source, remain untouched. `review/v3/session-handoff.json` records the generated v3 document; `review/v3/publication-handoff.json` records the corrected source copied to `assets/examples/evidence-gated-overview.pptx` and left open for handoff.

To regenerate the design handoff itself after an intentional design-code edit, run the following separately. It writes `design-spec.json`, `review-plan.json`, and the silhouette study, so it is unnecessary for reproducing the frozen v3 scene:

```powershell
& 'C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe' .\design.mjs
```

The final code was exercised in `review/v3/`. `review/v3/reproduction-check.json` records seven corresponding v2/v3 images with equal pixels, unchanged native structure/text metrics, and corrected PPTX notes. Native slide XML differs only in PowerPoint-generated creation IDs. The v2 publication source and full image are retained as `review/v3/baseline-v2.pptx` and `baseline-v2.png` for repeatable comparisons. This checks reproducibility and attribution; it is not another blind reading or independent acceptance.

## Limitations

The independent reader is an AI agent, not a human participant study. Attempt counting needs the companion explanation or caption: one draft/check cycle is one attempt, with the initial cycle counted as 1. All drawing primitives are editable, but the routed edges use multiple native connector segments with fixed waypoints; node movement requires rerouting those segments. Font sizes are 7.2–13 physical points at the declared publication size. No empirical data is available. The design depicts cited-claim checking without adding a checker-accuracy or factual-completeness guarantee.
