# Placement

`place` converts the manifest into the arguments of the existing image tools. It never opens an application; the Drawer runs the calls.

```sh
python scripts/sivia_assets.py place --workdir DIR --backend drawio [--canvas 1800x800]
python scripts/sivia_assets.py place --workdir DIR --backend pptx --slide-index 2 --canvas 960x426.7
```

## Output

`placement.<backend>.json`:

```json
{
  "backend": "drawio",
  "canvas": [1800, 800],
  "units": "px",
  "warnings": [],
  "calls": [
    { "element": "persona", "tool": "drawio_live_add_image", "arguments": { "id": "img-persona", "image_path": "/abs/assets/persona.png", "x": 134.5, "y": 323.2, "width": 150.9, "height": 253.6, "raster_reason": "...", "source_is_tightly_cropped": true, "atomic_raster_unit": true, "contains_reconstructable_content": false, "decomposition_note": "...", "preserve_aspect": true }, "warnings": [] }
  ],
  "unplaced": []
}
```

Pass each `arguments` object unchanged to the tool named in `tool`. The arguments are validated against the live tool schemas by the repository tests, including the mandatory raster declarations (`atomic_raster_unit: true`, `contains_reconstructable_content: false`, a specific `raster_reason` and `decomposition_note`). Edit the wording of the two declaration strings per element in `elements.json` when the default is too generic for the figure notes.

## Coordinates

- The approved image's pixel space is scaled to the target: draw.io uses canvas units (default one unit per reference pixel), PowerPoint uses points (default 960x540 for a 16:9 slide).
- The tight visible region of the asset is fitted inside the slot, centered, aspect preserved (`--fit contain`, default). The transparent padding saved with each asset is added around it, so the subject lands where the slot says. `--fit fill` stretches to the slot and should be avoided for illustrations.
- The command warns when the canvas aspect differs from the reference by more than 2%. Use the suggested `--canvas` and size the slide to match; otherwise slot positions stretch non-uniformly.
- `effective_dpi` is recomputed for the placed size when `figure.width_mm` is known, and a per-call warning appears when it is below the target.

## Order and layering

Calls are emitted in plan order. Draw backgrounds and panels first, then call the placement list, then native labels, arrows and annotations, so connectors stay above pictures. After grouping, re-inspect external arrows: group creation can cover them with panel fills.

## Elements that failed QA

`place` leaves out elements whose QA status is `fail` and lists them under `unplaced` with the reason. Fix and rerun `qa`, or pass `--allow-failed` only for a clearly labelled draft.

## Backend notes

- **draw.io live**: the image is embedded in the cell style. Servers older than this repository's fix cut the data at `;base64` and show a broken-image icon; update before debugging anything else. The saved `.drawio` grows by the size of its images (about 230 KB per element in the first run); regenerate smaller only if file size matters.
- **PowerPoint / WPS**: use absolute paths (the command writes them). Keep `lock_aspect_ratio` true. Slide size is a property of the presentation: set it to match `--canvas` before placing.
- **Replacing an element**: regenerate its sheet, rerun `split` and `qa`, then update the existing cell with the same id (`drawio_live_update_cell` or `powerpoint_update_shape`) or delete and re-add it; position and size come from the same slot.
