# v3 provenance correction and reproduction

The scientific source is the synthetic regression brief defined for this plugin test (B1–B6). The v3 PPTX notes, `detail.md`, `design-spec.json`, and the generator now use this attribution. The optional generator parameter `-PythonExe` defaults to `python`; the README shows how to override it with the bundled interpreter.

The v2 visual scene was regenerated without changes to geometry, wording, fonts, routes, or the 55 native objects. PowerPoint 16.0 build 19530 exported the full slide and both native review copies again. Grayscale images were derived from those actual exports.

`reproduction-check.json` records pixel equality for the full image, both review color images, both grayscale images, and both 850-pixel grayscale previews. The native object inventory and text metrics are equal to v2. Raw slide XML is not byte-identical because PowerPoint generates new creation IDs; every remaining XML field is equal. The actual notes contain the corrected attribution. No new blind reading or independent acceptance is claimed.

The existing `review/v1/` and `review/v2/` records are unchanged. `baseline-v2.pptx` and `baseline-v2.png` preserve the previous publication source and full image for repeatable comparison. Historical v1/v2 notes retain their original attribution as part of that record; `source.pptx` is the corrected v3 source.

Independent reader records are supplied by the main agent. The earlier connector correction record remains at `../v2/correction-report.md`.
