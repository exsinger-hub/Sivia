"""Compare v3 render pixels and native slide XML with v2; verify corrected notes."""
import json
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET
from PIL import Image, ImageChops

sample = Path(__file__).resolve().parent
repo = sample.parents[1]
current = sample / 'review' / 'v3'
baseline = sample / 'review' / 'v2'
published = current / 'baseline-v2.pptx'
pairs = [('full', current / 'baseline-v2.png', current / 'full.png')]
for name in ('view-01.png', 'view-02.png', 'view-01-gray.png', 'view-02-gray.png',
             'view-01-gray-850.png', 'view-02-gray-850.png'):
    pairs.append((name, baseline / name, current / name))
comparisons = []
for label, before, after in pairs:
    with Image.open(before) as a, Image.open(after) as b:
        equal = a.size == b.size and ImageChops.difference(a.convert('RGB'), b.convert('RGB')).getbbox() is None
        comparisons.append({'view': label, 'baseline': str(before), 'candidate': str(after),
                            'pixels': list(b.size), 'pixel_equal': equal})
with ZipFile(published) as a, ZipFile(current / 'source.pptx') as b:
    slide_equal = a.read('ppt/slides/slide1.xml') == b.read('ppt/slides/slide1.xml')
    roots = [ET.fromstring(z.read('ppt/slides/slide1.xml')) for z in (a, b)]
    creation_tags = {'{http://schemas.microsoft.com/office/drawing/2014/main}creationId',
                     '{http://schemas.microsoft.com/office/powerpoint/2010/main}creationId'}
    # PowerPoint assigns fresh creation IDs on each native generation. Retain
    # every other attribute, including fonts, geometry, object and connector IDs.
    ignored = []
    for root in roots:
        count = 0
        for node in root.iter():
            if node.tag in creation_tags:
                node.attrib.clear()
                count += 1
        ignored.append(count)
    content_equal = ET.tostring(roots[0]) == ET.tostring(roots[1])
    notes = ET.fromstring(b.read('ppt/notesSlides/notesSlide1.xml'))
    note_text = '\n'.join(notes.itertext())
    attribution = 'synthetic regression brief defined for this plugin test (B1–B6)'
    notes_correct = attribution in note_text and 'user-provided' not in note_text
structure_before = json.loads((baseline / 'structure.json').read_text(encoding='utf-8-sig'))
structure_after = json.loads((current / 'structure.json').read_text(encoding='utf-8-sig'))
structure_equal = structure_before == structure_after
evidence = json.loads((current / 'renderer-evidence.json').read_text(encoding='utf-8-sig'))
result = {'scope': 'Reproducibility only; not another blind reading or independent review.',
          'baseline': 'Frozen v2 before publishing the notes-corrected v3 source.',
          'pixel_comparisons': comparisons, 'native_slide_xml_equal': slide_equal,
          'slide_xml_equal_except_powerpoint_creation_ids': content_equal,
          'ignored_creation_id_elements': ignored,
          'native_structure_and_text_metrics_equal': structure_equal,
          'native_shape_count': evidence['native_shape_count'],
          'pptx_notes_attribution_correct': notes_correct,
          'expected_attribution': attribution}
(current / 'reproduction-check.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
print(json.dumps(result, indent=2))
if not (all(x['pixel_equal'] for x in comparisons) and content_equal and structure_equal
        and notes_correct and evidence['native_shape_count'] == 55):
    raise SystemExit('Reproduction or attribution mismatch: do not replace the publication source.')
