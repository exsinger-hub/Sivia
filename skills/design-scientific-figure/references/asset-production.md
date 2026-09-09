# Produce assets by semantic role

Read when a figure mixes native drawing, vector artwork, empirical fields or generated illustrations, especially when an approved overview will become editable. This reference plans assets; it does not authorize launching PowerPoint/WPS, creating a deck, generating a new image during a native-only task, or altering an approved composition. Image-only delivery still ends at the feedback/PPT-choice pause.

## Choose the representation before extracting pixels

The absence of a built-in PowerPoint icon is not a reason to crop it from the overview. Choose by what the object means and what must remain editable:

| Object | Production route | Editable boundary |
| --- | --- | --- |
| Modules, tensors, token strips, grids, scan paths, simple robot glyphs, connectors | Native shapes/lines or grouped editable primitives; compute geometry from the algorithm when it encodes method behavior. | Keep meaningful parts, labels and semantic connectors individually editable. |
| Custom regular silhouettes or complex line art | Native freeform/polyline/path if the selected backend supports it; otherwise an editable primitive composite. Consider an original SVG for artwork whose internal editing is not required. | SVG scales cleanly but insertion alone does not make its paths native editable objects. Verify conversion/ungrouping in the actual backend before claiming deep editability. |
| Quantitative curves, bars, tables and coordinates | Replot from original measurements into native charts or editable geometry with exact values and scales. | Axes, ticks, curves, legends and labels stay editable. A screenshot is not the underlying data. |
| Medical slices, microscopy, predictions, masks, learned feature maps, spectra | Export the individual field from original image/array/tensor or the verified experiment output. | One atomic image per field; separate native labels, borders, scale annotations and arrows. |
| Detailed robot/organ illustration, textured scene or other illustrative artwork | Reuse a suitable original high-resolution asset, or generate the individual asset with ImageGen when generation is in scope. | One independent picture per irreducible illustration; its labels and mechanism arrows remain native. A simple glyph still belongs in the first row. |

Do not turn every complex object into hundreds of tiny shapes for nominal editability. Preserve editable scientific structure; allow genuinely irreducible artwork to be a picture. Conversely, do not vector-trace an entire screenshot into thousands of paths and call its labels or topology semantically editable.

Construct line-based regions from planned coordinates, repeated motifs and named groups. Batch the objects according to the selected Drawer: PowerPoint COM uses background region batches, while other adapters retain their documented commit/pacing rules. Native reconstruction does not inherently require slow one-line-at-a-time playback. Capability discovery belongs to the authorized native stage, not image-only planning.

## Export empirical fields; do not recreate their appearance

Prefer original data/arrays and lossless individual exports over paper screenshots. If only a PDF exists, first extract its embedded raster or vector object; rendering a low-resolution embedded picture at higher DPI does not recover source detail. Crop a supplied figure only when it is the best available source and contains the correct atomic field. Record that fallback.

Bind input, target and prediction to the same case, slice/time point, orientation and crop. Bind activations and spectra to their actual producer, layer and computation. Use consistent documented windowing, normalization and color scales for comparisons; preserve categorical masks without interpolating new classes. Keep native source resolution even when acquisition pixels are coarse. No ImageGen replacement, generative super-resolution or invented texture may stand in for measured fields. Ordinary display interpolation is not additional measured detail.

Use measurement files for plots. If only a plotted image is available, retain it as an explicitly limited reference or request the values; do not infer precise results from visually plausible curves. Digitization, when requested, is an approximate reconstruction with source/uncertainty recorded, not original measurements. A retained reference plot does not pass a fully editable chart requirement.

Illustrative brains, heatmaps or spectra may explain a mechanism, but cannot acquire empirical status by resembling data. Distinguish them in the caption/design notes and use a concise in-figure "schematic" label only when needed to prevent a scientific misreading. Keep production receipts and pending-work notes outside the figure.

## Generate complex illustrations as independent assets

For a robot or detailed context illustration that would otherwise be a tiny overview crop, generate a standalone composition-matched asset. Specify its silhouette/pose, orientation, viewing angle, palette, line weight, shading, intended physical size, minimum useful subject pixels and padding. Request a transparent background when supported; inspect the actual alpha/background instead of assuming the prompt guarantees transparency. Do not bake in labels, legends, panel frames or method arrows. Preserve the approved asset's visual role; regeneration that changes its meaning or approved design needs agreement.

Use the available image-generation tool and its image skill; save the exact asset prompt and returned image, inspect both the standalone asset and its final-size placement, and keep the asset independently replaceable. A separate illustration prompt describes that illustration completely; it need not inherit an unrelated whole-overview template. This is not a shortcut for generating a whole figure or panel: complete figure generations/revisions still obey their bound template and exact-submitted-prompt length check. Honor any user-specified asset template/length floor as well.

## Judge the retained pixels at the final size

Cropping without resampling does not blur the retained pixels; enlarging a small crop reveals how few pixels it retained. Prefer the original vector, original raster export or separately generated illustration before enlarging an overview crop. Changing DPI metadata, interpolation, or sharpening cannot restore missing source information.

Compute per axis:

`effective_dpi = retained_pixels * 25.4 / placed_size_mm`

`required_pixels = ceil(placed_size_mm * target_dpi / 25.4)`

For example, 30 mm at a working target of 300 dpi needs 355 pixels across; an 80-pixel crop placed at 30 mm supplies about 68 dpi, regardless of the full overview's dimensions or embedded DPI tag. Use the publication's actual target when supplied. A 300-dpi default is a planning target for raster artwork, not a universal journal rule or a scientific-quality verdict; line art/text generally belongs in vectors/native objects.

For raster assets being cropped, enlarged or prepared for publication, run the read-only helper (Python with Pillow) using the planned crop and placement:

```sh
python skills/design-scientific-figure/scripts/inspect_raster_asset.py --image robot.png --crop-px 100 50 500 450 --width-mm 30 --target-dpi 300
```

Paths above are relative to the Sivia plugin root. Crop coordinates are stored-raster pixel edges `(left, top, right, bottom)`, with right/bottom exclusive. Omit crop for the whole image; omit height to preserve the retained aspect ratio. Transparent/empty margins still consume canvas pixels: use the intended tight subject crop for a meaningful placement estimate. The helper neither crops/resizes files nor detects compression, blur, scientific authenticity or downstream export resampling. Missing Pillow means calculate from known dimensions, not launch a presentation app.

For an explicitly transparent asset, add `--require-transparent`. It reads actual alpha within the retained crop, reports the nontransparent bounding box in source coordinates, and returns exit code 1 if fully transparent pixels or visible content are absent. Opaque RGB without transparency information, fully opaque RGBA and wholly empty transparent canvases do not pass; PNG color-key transparency is honored. Exit code 2 is invalid input; a valid sampling report otherwise returns 0 even if the DPI target is not met. This alpha test is necessary but not sufficient: stray transparent pixels do not establish a clean cutout. Inspect edges/background visually, then use the visible subject bounds for a tight-placement estimate where appropriate. Do not silently trim the source or alter white foreground details.

When sampling is insufficient, first seek an original export/vector; redraw reconstructable content; independently regenerate an illustration if allowed; or reduce its placement within the approved layout. If none is available, state the actual source limitation. Do not invent detail to make genuinely low-resolution empirical data meet a nominal DPI target. Inspect the exported figure at final publication size as well: sufficient source pixels cannot detect renderer compression, illegible baked text or wrong interpolation.

Record these decisions against the existing design/reconstruction object ids, not in a new registry: source path or exact generation prompt, empirical versus schematic role, chosen representation and actual editability, plus crop pixels, placement size and effective DPI when relevant. Retain the existing atomic-image declarations. Delivery should say which parts are native editable, single vector artwork or raster assets, rather than promising every pixel is editable.

## Turn a failed attempt into a different next action

Testing is a means to obtain a usable asset, not a substitute for producing it. When an in-scope attempt fails, identify the smallest failed property, change the production action that controls it, and recheck the actual result. Use the existing notes to keep the failure and effective correction; do not create a new scoring system.

- An overview crop has too few subject pixels: obtain the original asset or regenerate that illustration independently. Repeating an overview at the same effective output size, changing its DPI tag or adding "high quality" to an unchanged prompt does not address the bottleneck. Inspect returned dimensions, not requested dimensions.
- A generated cutout has an opaque background or painted checkerboard: request a background-only correction through the available image editor, preserving the character. Verify real alpha and edges; white robot parts are not background merely because they are white. If that route still returns an opaque image, use an authorized local masking/background-removal method, or a matching opaque backdrop only when the design allows it. Follow the active image tool's permission requirements for changing methods; do not claim alpha support based on repeated prompt requests.
- A picture still contains a separable label, compass, legend or neighboring character: isolate only the irreducible illustration and reconstruct the other objects separately. A generous rectangular crop is not semantic decomposition.
- An asset is sharp in isolation but unreadable at placement size: simplify nonessential illustration detail or rebuild exact text/line structure natively when that stage is authorized. Do not globally enlarge or rearrange an approved figure without agreement.

Reinspect the changed property and its placement before accepting the asset. If the same approach produces the same defect, choose a materially different in-scope representation or source route instead of repeating the attempt without new information. Missing measurements require original data or an explicitly schematic role, not more image generation. Continue independent in-scope work while a source is missing. If success would require an unavailable capability, new scientific content or permission to change the approved composition, state that concrete boundary and request the needed choice; passing unrelated unit tests does not resolve it.

### Local contour-mask fallback for suitable artwork

When local background removal is authorized, inspect the illustration before selecting an algorithm. For one isolated character with a closed dark outer contour, clear canvas margins and a lighter background, the bundled Pillow helper can produce a candidate mask without redrawing the character:

```sh
python skills/design-scientific-figure/scripts/extract_outlined_artwork.py --image robot-opaque.png --output robot-transparent.png --mask robot-alpha.png
```

It treats dark strokes as a barrier, closes only small pixel gaps and floods the connected exterior. It changes alpha only; source RGB and source files are preserved. The grayscale mask is an editable/reviewable asset. The optional `--threshold` controls the dark barrier, not semantic subject recognition. Outputs must be new PNG files; existing transparency should be inspected and reused instead of masked again.

This is not a general photo, hair, glass or medical-image segmentation tool. It can retain enclosed background holes or detached dark marks, and a broken exterior contour may expose the interior. Reject those defects in the mask/render and use a reviewed manual mask or another authorized segmentation method when the contour assumption fails. Do not indiscriminately erase white or grey pixels: light foreground clothes and highlights can share background colors.

After applying a mask, inspect the character on both light and dark backgrounds and at the intended small placement size; verify intact silhouette, foreground whites and absence of background remnants. Run the alpha check and calculate DPI from visible subject bounds, not canvas padding. A successful script exit only means a candidate was produced. Once the user has authorized this local editing method for the task, execute its in-scope corrections without repeatedly asking for the same permission.
