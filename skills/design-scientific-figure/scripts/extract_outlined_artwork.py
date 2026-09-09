#!/usr/bin/env python3
"""Make a candidate alpha mask for isolated, closed dark-outline artwork on a lighter background.

Use only for authorized local illustration editing, not photos or empirical fields.
Requires Pillow. Keeps source RGB unchanged; the candidate needs visual review.
"""

import argparse
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter


def outline_mask(source, threshold=64):
    if not 0 < threshold < 255:
        raise ValueError("threshold must be between 1 and 254")
    if source.convert("RGBA").getchannel("A").getextrema()[0] < 255:
        raise ValueError("source already has transparency; inspect/reuse its alpha instead")
    rgb = source.convert("RGB")
    red, green, blue = rgb.split()
    maximum = ImageChops.lighter(ImageChops.lighter(red, green), blue)
    barrier = maximum.point(lambda value: 255 if value < threshold else 0)
    # Bridge only small antialiasing gaps, not a substantially open silhouette.
    barrier = barrier.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3))
    width, height = barrier.size
    for edge in ((0, 0, width, 1), (0, height - 1, width, height),
                 (0, 0, 1, height), (width - 1, 0, width, height)):
        if barrier.crop(edge).getbbox() is not None:
            raise ValueError("dark outline touches the canvas edge; use a complete isolated source")
    outside = barrier.copy()
    ImageDraw.floodfill(outside, (0, 0), 128)
    if outside.histogram()[0] == 0:
        raise ValueError("no enclosed interior found; choose another masking method")
    return outside.point(lambda value: 0 if value == 128 else 255)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path, help="New RGBA PNG, never overwrites a file")
    parser.add_argument("--mask", required=True, type=Path, help="New grayscale PNG candidate mask for review")
    parser.add_argument("--threshold", type=int, default=64, help="All RGB channels below this value form the dark barrier")
    args = parser.parse_args()
    try:
        targets = (args.output.resolve(), args.mask.resolve())
        if len(set(targets)) != 2 or any(path == args.image.resolve() or path.exists() for path in targets):
            raise ValueError("output and mask must be distinct new files, not the source")
        if any(path.suffix.lower() != ".png" for path in targets):
            raise ValueError("output and mask must use .png")
        with Image.open(args.image) as source:
            alpha = outline_mask(source, args.threshold)
            result = source.convert("RGB")
        result.putalpha(alpha)
        for path in targets:
            path.parent.mkdir(parents=True, exist_ok=True)
        result.save(targets[0])
        alpha.save(targets[1])
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps({
        "image": str(args.image.resolve()), "output": str(targets[0]), "mask": str(targets[1]),
        "size_px": list(result.size), "visible_bbox_px": alpha.getbbox(),
        "rgb_operation": "unchanged source RGB; alpha added only", "threshold": args.threshold,
        "review_required": "Check silhouette, enclosed background holes, detached marks and light foreground on light/dark backgrounds.",
    }, indent=2))


if __name__ == "__main__":
    main()
