# Prepare real overview review views

Use when auditing an overview saved as PPTX. Work on disposable copies so the full editable source retains its content.

Give every title and L3 annotation a stable shape name while drawing. Small critical conditions, inverse operations and training/freeze cues remain L1/L2 and are excluded from `detail_names`. Define a plan:

```json
{
  "slide": 1,
  "title_names": ["figure_title"],
  "detail_names": ["retrieval_note", "implementation_note"],
  "publication_width_mm": 170
}
```

Run from the plugin root with Python 3 (standard library only):

```sh
python scripts/prepare-overview-review.py figure.pptx review-plan.json review-v1
```

The helper produces `title-hidden.pptx`, `detail-hidden.pptx` and `review-manifest.json`. It removes exact named objects from the selected slide in full deck copies. A named group includes its children. Unknown or ambiguous names fail rather than silently yielding a fake masking test. Use a new output directory per version.

Selected objects involving OOXML alternate representations are rejected before writes. For example, PowerPoint ink can have native content plus a fallback picture ([Microsoft's ink example](https://learn.microsoft.com/en-us/openspecs/office_standards/ms-odrawxml/a1a880a0-1d58-4a39-80c8-6f87161671fb)); deleting only the fallback would falsely report a hidden annotation. In that case prepare the disposable copies in PowerPoint itself, delete the actual annotation, and verify both exports. Unselected alternate content remains untouched.

If the publication figure has no title or no L3 objects, record that specific view as not applicable with the actual object inventory and review the naturally reduced view. Do not add a dummy title or decorative details to satisfy this helper's nonempty-name requirement. Keep any surviving connector's target out of a removal set; the helper rejects dangling endpoints.

Before preparing copies, include annotation-only leaders and decorations in the removal set and verify that named groups contain no L1/L2 content. The helper can detect attached connector references but cannot infer scientific levels or the meaning of a free line. Inspect the resulting render for orphan labels and free-line endpoints. Fix the level assignment rather than adding a review-only replacement path.

The manifest reports copy preparation with rendering pending. Export the source and both copies through the selected application, then derive grayscale from both actual copy exports. The reduced view tests the main story; the full-density title-hidden view tests interference from detail. Record renderer, image paths, output dimensions, physical width and removed names alongside the observations. Copy generation, grayscale conversion and source-object counting do not establish visual quality.

For draw.io, use a duplicated page or disposable saved copy and hide/remove the same named title/L3 cell sets before capturing the current draw.io renderer. Preserve scientific boundaries and claim-critical labels. Do not mask rectangles over the full figure or change the delivery source during read-only review.

Give the reduced grayscale image to an unprimed Reviewer, save their response, then show full-density title-hidden grayscale and save that response too. Freeze both before revealing full color, Figure Claim and the scientific contract for deeper review. Record prior exposure and uncertainty honestly. If the needed renderer is unavailable, deliver the candidate with the dependent gate pending.
