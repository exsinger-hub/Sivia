# Renderer corrections for v2

The main agent supplied three observed connector findings from the actual v1 PowerPoint image. They were consistent with the constructor's same-context image inspection. This record is not an independent review or a visual-quality verdict.

| Object | Observed failure | Current correction |
| --- | --- | --- |
| `abstain_branch` | Octagon connection site 2 pulled the line through the output and text. | Explicit native endpoint at (143, 53) mm on the left boundary; no assumed octagon port. |
| `retrieve_to_spans` | The x=41 mm rise crossed the evidence boundary note. | Route (41,31) → (41,23) → (82.5,23) → (82.5,21) mm, below the note and into the source operand. |
| `spans_to_gate` | The x=107 mm drop crossed the checker label. | Route (96,16.5) → (128,16.5) → (128,25) → (107,25) → (107,26) mm, ending at the circle's top. Label moved to (96.8,19,30,5) mm to clear the source operand as well. |
| `supported_branch` | The document's native port produced a slight slope. | Keep the gate's right attachment; use the explicit target boundary point (143,37) mm. |
| `autoshape_count` | v1 counted native connectors again as autoshapes. | Classify connectors first with `Shape.Connector`; count nonconnector Type 1 shapes separately from Type 17 text. |

The current native inventory is 55 = 25 text boxes + 20 connectors + 10 nonconnector autoshapes. Picture count is zero. `structure.json` includes `is_connector` so the categories can be reconstructed. PowerPoint's text-bound check found no overflowing text boxes; that measurement did not detect the v1 connector crossings and is not a substitute for image review.

The source and all current images were exported through PowerPoint 16.0, build 19530. Exact times and paths are in `renderer-evidence.json`; both grayscale views derive from the corresponding target PNGs. The main agent coordinates a separate fresh independent reviewer. No independent verdict is claimed here.

`review/v1/` remains unchanged. The corrected deliverable is the source at `assets/examples/evidence-gated-overview.pptx` plus the current `review/v2/` evidence.
