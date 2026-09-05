"""Derive both grayscale views only from fresh PowerPoint PNG exports."""
import argparse
import json
from pathlib import Path
from PIL import Image, ImageOps

parser = argparse.ArgumentParser()
parser.add_argument('review_directory', type=Path)
args = parser.parse_args()
review = args.review_directory.resolve()
derived = []
for stem in ('view-01', 'view-02'):
    source = review / f'{stem}.png'
    with Image.open(source) as image:
        gray = ImageOps.grayscale(image)
        gray_path = review / f'{stem}-gray.png'
        gray.save(gray_path, dpi=(304.8, 304.8))
        preview_path = review / f'{stem}-gray-850.png'
        gray.resize((850, 400), Image.Resampling.LANCZOS).save(preview_path)
        derived.append({'source': str(source), 'grayscale': str(gray_path),
                        'screen_preview': str(preview_path), 'native_pixels': list(image.size),
                        'preview_pixels': [850, 400], 'publication_width_mm': 170,
                        'method': 'Pillow luminance conversion of actual PowerPoint Slide.Export PNG'})
(review / 'derived-image-evidence.json').write_text(json.dumps(derived, indent=2)+'\n', encoding='utf-8')
print(json.dumps(derived, indent=2))
