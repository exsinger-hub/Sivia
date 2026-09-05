"""Exercise the review-copy CLI against small native OOXML packages."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from xml.etree import ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/prepare-overview-review.py"
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
REL = "http://schemas.openxmlformats.org/package/2006/relationships"
SELECTED_PART = "ppt/slides/slide2.xml"  # First in presentation order.
DELIVERABLES = ("title-hidden.pptx", "detail-hidden.pptx", "review-manifest.json")


def text_shape(shape_id, name):
    return (
        f'<p:sp><p:nvSpPr><p:cNvPr id="{shape_id}" name="{name}"/>'
        '<p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr/>'
        f'<p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:r><a:t>{name}</a:t>'
        '</a:r></a:p></p:txBody></p:sp>'
    )


def group(shape_id, name, children):
    return (
        f'<p:grpSp><p:nvGrpSpPr><p:cNvPr id="{shape_id}" name="{name}"/>'
        '<p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/>'
        f'{children}</p:grpSp>'
    )


TITLE = text_shape(2, "Title")
DETAIL = text_shape(4, "Detail")
ANNOTATIONS = group(
    5, "Annotations", text_shape(6, "Caption A")
    + group(7, "Nested annotations", text_shape(8, "Caption B")),
)
PICTURE = (
    '<p:pic><p:nvPicPr><p:cNvPr id="9" name="Image"/>'
    '<p:cNvPicPr/><p:nvPr/></p:nvPicPr><p:blipFill>'
    '<a:blip r:embed="rImage"/><a:stretch><a:fillRect/></a:stretch>'
    '</p:blipFill><p:spPr/></p:pic>'
)
# MS-ODRAWXML 3.2: ink's properties use p14, while its picture fallback uses p.
INK = (
    '<p:contentPart p14:bwMode="auto" r:id="rInk"><p14:nvContentPartPr>'
    '<p14:cNvPr id="13" name="Ink note"/><p14:cNvContentPartPr/>'
    '<p14:nvPr/></p14:nvContentPartPr><p14:xfrm>'
    '<a:off x="1561526" y="971040"/><a:ext cx="3210480" cy="1010160"/>'
    '</p14:xfrm></p:contentPart>'
)
INK_FALLBACK = PICTURE.replace('id="9"', 'id="13"').replace('name="Image"', 'name="Ink note"')


def alternate_content(choice, fallback):
    return (
        '<mc:AlternateContent><mc:Choice Requires="p14">' + choice
        + '</mc:Choice><mc:Fallback>' + fallback
        + '</mc:Fallback></mc:AlternateContent>'
    )


CONNECTOR = (
    '<p:cxnSp><p:nvCxnSpPr><p:cNvPr id="10" name="Connector"/>'
    '<p:cNvCxnSpPr><a:stCxn id="11" idx="0"/>'
    '<a:endCxn id="9" idx="1"/></p:cNvCxnSpPr><p:nvPr/>'
    '</p:nvCxnSpPr><p:spPr/></p:cxnSp>'
)
FIGURE = group(
    3, "Figure", DETAIL + ANNOTATIONS + PICTURE + CONNECTOR
    + text_shape(11, "Body"),
)
SLIDE_XML = (
    f'<p:sld xmlns:p="{P}" xmlns:a="{A}" xmlns:r="{R}" '
    'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
    'xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" '
    'mc:Ignorable="p14"><p:cSld><p:spTree><p:nvGrpSpPr>'
    '<p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/>'
    '</p:nvGrpSpPr><p:grpSpPr/>'
    + TITLE + FIGURE + text_shape(12, "Title extra")
    + '</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/>'
    '</p:clrMapOvr><!-- retain this comment --></p:sld>'
)


class PrepareOverviewReviewTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.source = self.directory / "source.pptx"
        self.plan_path = self.directory / "plan.json"
        self.output = self.directory / "review"
        self.plan = {
            "slide": 1,
            "title_names": ["Title"],
            "detail_names": ["Detail", "Annotations"],
            "publication_width_mm": 170,
        }
        self.write_source()

    def write_source(self, slide_xml=SLIDE_XML, other_slide_xml=SLIDE_XML):
        parts = {
            "[Content_Types].xml": (
                '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                '<Default Extension="xml" ContentType="application/xml"/>'
                '<Default Extension="png" ContentType="image/png"/>'
                '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>'
                '<Override PartName="/ppt/slides/slide1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
                '<Override PartName="/ppt/slides/slide2.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
                '</Types>'
            ),
            "_rels/.rels": (
                f'<Relationships xmlns="{REL}"><Relationship Id="rOffice" '
                f'Type="{R}/officeDocument" Target="ppt/presentation.xml"/></Relationships>'
            ),
            "ppt/presentation.xml": (
                f'<p:presentation xmlns:p="{P}" xmlns:r="{R}"><p:sldIdLst>'
                '<p:sldId id="256" r:id="rFirst"/><p:sldId id="257" r:id="rSecond"/>'
                '</p:sldIdLst><p:sldSz cx="9144000" cy="6858000"/>'
                '<p:notesSz cx="6858000" cy="9144000"/></p:presentation>'
            ),
            "ppt/_rels/presentation.xml.rels": (
                f'<Relationships xmlns="{REL}"><Relationship Id="rFirst" '
                f'Type="{R}/slide" Target="slides/slide2.xml"/>'
                f'<Relationship Id="rSecond" Type="{R}/slide" '
                'Target="/ppt/slides/slide1.xml"/></Relationships>'
            ),
            "ppt/slides/slide1.xml": other_slide_xml,
            SELECTED_PART: slide_xml,
            "ppt/slides/_rels/slide2.xml.rels": (
                f'<Relationships xmlns="{REL}"><Relationship Id="rImage" '
                f'Type="{R}/image" Target="../media/image1.png"/>'
                f'<Relationship Id="rInk" Type="{R}/ink" Target="../ink/ink1.xml"/>'
                f'<Relationship Id="rLink" Type="{R}/hyperlink" '
                'Target="https://example.com" TargetMode="External"/></Relationships>'
            ),
            "ppt/media/image1.png": bytes.fromhex(
                '89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c489'
                '0000000b49444154789c636000020000050001a5f645400000000049454e44ae426082'
            ),
            "ppt/ink/ink1.xml": '<inkml:ink xmlns:inkml="http://www.w3.org/2003/InkML"/>',
        }
        parts["ppt/slides/_rels/slide1.xml.rels"] = parts["ppt/slides/_rels/slide2.xml.rels"]
        with ZipFile(self.source, "w", ZIP_DEFLATED) as archive:
            archive.comment = b"Preserve package comment"
            for name, data in parts.items():
                archive.writestr(name, data)

    def run_helper(self):
        self.plan_path.write_text(json.dumps(self.plan), encoding="utf-8")
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPT), str(self.source),
             str(self.plan_path), str(self.output)],
            capture_output=True, text=True, check=False,
        )

    def assert_rejected(self, result, message):
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(message.lower(), result.stderr.lower())
        self.assertFalse(self.output.exists(), "Validation must precede output writes")

    def test_title_and_detail_copies_preserve_all_other_content_and_relationships(self):
        result = self.run_helper()
        self.assertEqual(result.returncode, 0, result.stderr)
        expected = {
            "title-hidden.pptx": SLIDE_XML.replace(TITLE, ""),
            "detail-hidden.pptx": SLIDE_XML.replace(TITLE, "").replace(
                DETAIL, ""
            ).replace(ANNOTATIONS, ""),
        }
        with ZipFile(self.source) as source:
            for filename, expected_xml in expected.items():
                with self.subTest(filename=filename), ZipFile(self.output / filename) as copy:
                    self.assertEqual(copy.namelist(), source.namelist())
                    self.assertEqual(copy.comment, source.comment)
                    for name in source.namelist():
                        if name != SELECTED_PART:
                            self.assertEqual(copy.read(name), source.read(name), name)
                    xml = copy.read(SELECTED_PART).decode("utf-8")
                    self.assertEqual(
                        ET.canonicalize(xml, with_comments=True),
                        ET.canonicalize(expected_xml, with_comments=True),
                    )
                    self.assertIn('xmlns:p14=', xml)
                    self.assertIn('mc:Ignorable="p14"', xml)
        manifest = json.loads((self.output / "review-manifest.json").read_text("utf-8"))
        self.assertEqual(manifest["source"], str(self.source.resolve()))
        self.assertEqual(manifest["slide"], 1)
        self.assertEqual(manifest["slide_part"], SELECTED_PART)
        self.assertEqual(manifest["publication_width_mm"], 170)
        self.assertEqual(manifest["renderer_status"], "pending")
        self.assertEqual(manifest["variants"]["title-hidden.pptx"]["removed_names"], ["Title"])
        self.assertEqual(manifest["variants"]["title-hidden.pptx"]["removed_count"], 1)
        self.assertEqual(
            manifest["variants"]["detail-hidden.pptx"]["removed_names"],
            ["Title", "Detail", "Annotations", "Caption A", "Nested annotations", "Caption B"],
        )
        self.assertEqual(manifest["variants"]["detail-hidden.pptx"]["removed_count"], 6)
        self.assertEqual({path.name for path in self.output.iterdir()}, set(DELIVERABLES))

    def test_source_bytes_are_preserved(self):
        original = self.source.read_bytes()
        result = self.run_helper()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.source.read_bytes(), original)

    def test_named_group_removes_descendants_once_even_when_child_is_also_named(self):
        self.plan["title_names"] = ["Annotations", "Caption B"]
        self.plan["detail_names"] = ["Detail"]
        result = self.run_helper()
        self.assertEqual(result.returncode, 0, result.stderr)
        manifest = json.loads((self.output / "review-manifest.json").read_text("utf-8"))
        self.assertEqual(
            manifest["variants"]["title-hidden.pptx"]["removed_names"],
            ["Annotations", "Caption A", "Nested annotations", "Caption B"],
        )
        self.assertEqual(manifest["variants"]["title-hidden.pptx"]["removed_count"], 4)

    def test_unknown_exact_name_fails_before_outputs(self):
        for field, name in (("title_names", "title"), ("detail_names", "Missing")):
            with self.subTest(field=field):
                saved = self.plan[field]
                self.plan[field] = [name]
                self.assert_rejected(self.run_helper(), "unknown")
                self.plan[field] = saved

    def test_empty_name_sets_cannot_claim_a_hidden_review_test(self):
        for field in ("title_names", "detail_names"):
            with self.subTest(field=field):
                saved = self.plan[field]
                self.plan[field] = []
                self.assert_rejected(self.run_helper(), field)
                self.plan[field] = saved

    def test_details_already_removed_by_title_group_are_rejected(self):
        self.plan["title_names"] = ["Annotations"]
        self.plan["detail_names"] = ["Caption B"]
        self.assert_rejected(self.run_helper(), "additional")

    def test_duplicate_shape_name_is_ambiguous_before_outputs(self):
        self.write_source(SLIDE_XML.replace('name="Caption B"', 'name="Title"'))
        self.assert_rejected(self.run_helper(), "ambiguous")

    def test_existing_deliverables_are_never_overwritten(self):
        self.output.mkdir()
        for filename in DELIVERABLES:
            with self.subTest(filename=filename):
                existing = self.output / filename
                existing.write_bytes(b"keep existing deliverable")
                result = self.run_helper()
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn("new directory", result.stderr.lower())
                self.assertEqual(existing.read_bytes(), b"keep existing deliverable")
                self.assertEqual(list(self.output.iterdir()), [existing])
                existing.unlink()

    def test_output_cannot_overwrite_source(self):
        self.output.mkdir()
        self.source = self.output / "title-hidden.pptx"
        self.write_source()
        original = self.source.read_bytes()
        result = self.run_helper()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("source", result.stderr.lower())
        self.assertEqual(self.source.read_bytes(), original)
        self.assertEqual(list(self.output.iterdir()), [self.source])

    def test_connector_endpoints_to_removed_shapes_fail_before_either_copy(self):
        for endpoint, target in (("stCxn", "2"), ("endCxn", "8")):
            with self.subTest(endpoint=endpoint):
                old = '<a:stCxn id="11"' if endpoint == "stCxn" else '<a:endCxn id="9"'
                self.write_source(SLIDE_XML.replace(old, f'<a:{endpoint} id="{target}"'))
                self.assert_rejected(self.run_helper(), "connector endpoint")

    def test_slide_number_uses_presentation_order_and_absolute_relationship_targets(self):
        self.plan["slide"] = 2
        result = self.run_helper()
        self.assertEqual(result.returncode, 0, result.stderr)
        with ZipFile(self.output / "title-hidden.pptx") as archive:
            self.assertEqual(archive.read(SELECTED_PART), SLIDE_XML.encode("utf-8"))
            self.assertNotIn(b'name="Title"', archive.read("ppt/slides/slide1.xml"))

    def test_invalid_slide_width_and_name_types_fail_before_outputs(self):
        for field, value in (
            ("slide", 0), ("slide", 3), ("slide", True),
            ("publication_width_mm", 0), ("publication_width_mm", float("nan")),
            ("title_names", "Title"), ("detail_names", [""]),
        ):
            with self.subTest(field=field, value=value):
                saved = self.plan[field]
                self.plan[field] = value
                self.assert_rejected(self.run_helper(), field)
                self.plan[field] = saved

    def test_selected_ink_native_or_fallback_name_rejects_alternate_representation(self):
        for field, replaced in (("title_names", TITLE), ("detail_names", DETAIL)):
            for case, native_name, fallback_name, selected_name in (
                ("same", "Ink note", "Ink note", "Ink note"),
                ("native", "Native ink", "Fallback ink", "Native ink"),
                ("fallback", "Native ink", "Fallback ink", "Fallback ink"),
            ):
                with self.subTest(field=field, case=case):
                    self.output = self.directory / f"{field}-{case}"
                    self.plan["title_names"] = ["Title"]
                    self.plan["detail_names"] = ["Detail", "Annotations"]
                    self.plan[field] = [selected_name]
                    alternate = alternate_content(
                        INK.replace("Ink note", native_name),
                        INK_FALLBACK.replace("Ink note", fallback_name),
                    )
                    self.write_source(SLIDE_XML.replace(replaced, alternate))
                    original = self.source.read_bytes()
                    result = self.run_helper()
                    self.assert_rejected(result, "unsupported alternate representation")
                    self.assertIn(selected_name, result.stderr)
                    self.assertEqual(self.source.read_bytes(), original)

    def test_selected_plain_shapes_inside_choice_or_fallback_are_rejected(self):
        for field, replaced, name in (
            ("title_names", TITLE, "Title"), ("detail_names", DETAIL, "Detail"),
        ):
            for branch in ("choice", "fallback"):
                with self.subTest(field=field, branch=branch):
                    self.output = self.directory / f"{field}-{branch}"
                    other = text_shape(13, "Other representation")
                    alternate = alternate_content(
                        replaced if branch == "choice" else other,
                        other if branch == "choice" else replaced,
                    )
                    self.write_source(SLIDE_XML.replace(replaced, alternate))
                    result = self.run_helper()
                    self.assert_rejected(result, "unsupported alternate representation")
                    self.assertIn(name, result.stderr)

    def test_selected_group_with_alternate_content_in_descendants_is_rejected(self):
        for field in ("title_names", "detail_names"):
            with self.subTest(field=field):
                self.output = self.directory / field
                self.plan["title_names"] = ["Title"]
                self.plan["detail_names"] = ["Detail"]
                self.plan[field] = ["Annotations"]
                # The wrapper is below a nested child group, not a direct child.
                self.write_source(SLIDE_XML.replace(
                    text_shape(8, "Caption B"), alternate_content(INK, INK_FALLBACK)
                ))
                result = self.run_helper()
                self.assert_rejected(result, "unsupported alternate representation")
                self.assertIn("Annotations", result.stderr)

    def test_unselected_alternate_content_preserves_support_for_plain_shapes(self):
        alternate = alternate_content(INK, INK_FALLBACK)
        ink_slide = SLIDE_XML.replace("</p:spTree>", alternate + "</p:spTree>")
        for case, selected_xml, other_xml in (
            ("same-slide", ink_slide, SLIDE_XML),
            ("sibling-in-group", SLIDE_XML.replace(ANNOTATIONS, alternate), SLIDE_XML),
            ("other-slide", SLIDE_XML, ink_slide),
        ):
            with self.subTest(case=case):
                self.output = self.directory / case
                self.plan["detail_names"] = ["Detail"]
                self.write_source(selected_xml, other_xml)
                result = self.run_helper()
                self.assertEqual(result.returncode, 0, result.stderr)
                for filename, expected_xml in (
                    ("title-hidden.pptx", selected_xml.replace(TITLE, "")),
                    ("detail-hidden.pptx", selected_xml.replace(TITLE, "").replace(DETAIL, "")),
                ):
                    with ZipFile(self.source) as source, ZipFile(self.output / filename) as copy:
                        self.assertEqual(copy.namelist(), source.namelist())
                        for name in source.namelist():
                            if name != SELECTED_PART:
                                self.assertEqual(copy.read(name), source.read(name), name)
                        self.assertEqual(
                            ET.canonicalize(copy.read(SELECTED_PART).decode("utf-8"), with_comments=True),
                            ET.canonicalize(expected_xml, with_comments=True),
                        )


if __name__ == "__main__":
    unittest.main()
