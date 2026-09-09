#!/usr/bin/env python3
"""Prepare full native PPTX copies for review of one selected slide.

Usage: python scripts/prepare-overview-review.py source.pptx plan.json output-directory
Plan: {"slide": 1, "title_names": ["Title"], "detail_names": ["Caption"],
       "publication_width_mm": 170}

Names are exact, case-sensitive PowerPoint shape names on the selected slide;
slide is one-based in presentation order. A named group includes its children.
Manifest removed_names/count include group objects and descendants, each once.
Both name lists must be nonempty, and details must remove something additional.
Dangling connector endpoints are rejected before output writes.
Selections inside or containing mc:AlternateContent are unsupported and rejected
before output writes; unrelated alternate content is preserved.

Only the selected slide XML changes; all other package parts (including all
slides and relationship files) are copied byte-for-byte. No relationship cleanup
is performed. The source is read-only. Publication width is review metadata, not
a slide resize. Copy preparation is not renderer evidence: open/render the named
slide in each copy separately; renderer_status remains pending.
"""

import argparse
import json
import math
from pathlib import Path
import posixpath
from defusedxml import minidom
from pyexpat import ExpatError
from zipfile import BadZipFile, ZipFile


P = "http://schemas.openxmlformats.org/presentationml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
REL = "http://schemas.openxmlformats.org/package/2006/relationships"
MC = "http://schemas.openxmlformats.org/markup-compatibility/2006"
SHAPES = {"sp", "grpSp", "pic", "cxnSp", "graphicFrame", "contentPart"}
DELIVERABLES = ("title-hidden.pptx", "detail-hidden.pptx", "review-manifest.json")


def read_plan(path):
    plan = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(plan, dict):
        raise ValueError("plan must be a JSON object")
    slide = plan.get("slide")
    if type(slide) is not int or slide < 1:
        raise ValueError("slide must be a positive one-based integer")
    for field in ("title_names", "detail_names"):
        names = plan.get(field)
        if (not isinstance(names, list) or not names
                or any(not isinstance(name, str) or not name.strip() for name in names)):
            raise ValueError(f"{field} must be a nonempty list of exact shape names")
    width = plan.get("publication_width_mm")
    if type(width) not in (int, float) or not math.isfinite(width) or width <= 0:
        raise ValueError("publication_width_mm must be a finite positive number")
    return plan


def slide_part(archive, slide):
    """Resolve the slide through presentation relationships, not slideN.xml."""
    with minidom.parseString(archive.read("ppt/presentation.xml")) as presentation:
        slides = presentation.getElementsByTagNameNS(P, "sldId")
        if slide > len(slides):
            raise ValueError(f"slide {slide} is out of range; presentation has {len(slides)} slides")
        relationship_id = slides[slide - 1].getAttributeNS(R, "id")
    with minidom.parseString(archive.read("ppt/_rels/presentation.xml.rels")) as relationships:
        matches = [
            rel for rel in relationships.getElementsByTagNameNS(REL, "Relationship")
            if rel.getAttribute("Id") == relationship_id
        ]
        if len(matches) != 1:
            raise ValueError(f"slide {slide} has a missing or ambiguous presentation relationship")
        relationship = matches[0]
        target = relationship.getAttribute("Target")
        if (not target or relationship.getAttribute("TargetMode") == "External"
                or relationship.getAttribute("Type") != R + "/slide"):
            raise ValueError(f"slide {slide} must reference an internal slide part")
        return posixpath.normpath(posixpath.join("ppt", target)).lstrip("/")


def prepare_variant(slide_xml, names, filename):
    # minidom retains prefixes and namespace declarations, including declarations
    # used only in attribute values such as mc:Ignorable (unlike ElementTree).
    with minidom.parseString(slide_xml) as document:
        trees = document.getElementsByTagNameNS(P, "spTree")
        if len(trees) != 1:
            raise ValueError("selected slide must contain one native shape tree")
        # Alternate representations may use p14:cNvPr (native ink) as well as
        # p:cNvPr (fallback picture). Reject either represented name; removing
        # only the indexed fallback would leave the native object visible.
        alternate_names = {
            properties.getAttribute("name")
            for alternate in trees[0].getElementsByTagNameNS(MC, "AlternateContent")
            for properties in alternate.getElementsByTagNameNS("*", "cNvPr")
        }
        shapes = []
        by_name = {}
        for properties in trees[0].getElementsByTagNameNS(P, "cNvPr"):
            shape = properties.parentNode.parentNode
            # The shape tree's own cNvPr is not a removable shape.
            if shape.namespaceURI == P and shape.localName in SHAPES:
                shapes.append((shape, properties))
                by_name.setdefault(properties.getAttribute("name"), []).append(shape)
        selected = set()
        for name in names:
            matches = by_name.get(name, [])
            if name in alternate_names or any(
                shape.getElementsByTagNameNS(MC, "AlternateContent") for shape in matches
            ):
                raise ValueError(
                    f"{filename}: unsupported alternate representation for selected name "
                    f"{name!r}: object is inside or contains mc:AlternateContent. "
                    "No review files written."
                )
            if not matches:
                raise ValueError(f"{filename}: unknown shape name {name!r} on selected slide")
            if len(matches) != 1:
                raise ValueError(f"{filename}: ambiguous shape name {name!r} ({len(matches)} matches)")
            selected.add(matches[0])

        def removed(node):
            while node is not None:
                if node in selected:
                    return True
                node = node.parentNode
            return False

        actual = [(shape, properties) for shape, properties in shapes if removed(shape)]
        removed_ids = {properties.getAttribute("id") for _, properties in actual}
        removed_names = [properties.getAttribute("name") for _, properties in actual]
        # Compute roots before mutation so naming a group and its child is atomic.
        roots = [shape for shape in selected if not removed(shape.parentNode)]
        for shape in roots:
            shape.parentNode.removeChild(shape)
        for endpoint_type in ("stCxn", "endCxn"):
            for endpoint in document.getElementsByTagNameNS(A, endpoint_type):
                shape_id = endpoint.getAttribute("id")
                if shape_id in removed_ids:
                    raise ValueError(
                        f"{filename}: connector endpoint {endpoint_type} references removed "
                        f"shape id {shape_id}; choose annotation-only shapes without attached "
                        "connectors. No review files written."
                    )
        return document.toxml(encoding="utf-8"), {
            "requested_names": list(dict.fromkeys(names)),
            "removed_names": removed_names,
            "removed_count": len(removed_names),
        }


def prepare_review(source, plan_path, output_directory):
    source = source.resolve(strict=True)
    output_directory = output_directory.resolve()
    destinations = [output_directory / name for name in DELIVERABLES]
    if source in destinations:
        raise ValueError("output would overwrite the source; use a new directory")
    for destination in destinations:
        if destination.exists():
            raise ValueError(f"output deliverable already exists: {destination}; use a new directory")
    plan = read_plan(plan_path)
    with ZipFile(source, "r") as archive:
        part = slide_part(archive, plan["slide"])
        slide_xml = archive.read(part)
        variants = {}
        for filename, names in (
            ("title-hidden.pptx", plan["title_names"]),
            ("detail-hidden.pptx", plan["title_names"] + plan["detail_names"]),
        ):
            variants[filename] = prepare_variant(slide_xml, names, filename)
        if (variants["detail-hidden.pptx"][1]["removed_count"]
                <= variants["title-hidden.pptx"][1]["removed_count"]):
            raise ValueError("detail_names must remove additional shapes beyond title_names")
        manifest = {
            "source": str(source),
            "slide": plan["slide"],
            "slide_part": part,
            "publication_width_mm": plan["publication_width_mm"],
            "renderer_status": "pending",
            "variants": {filename: report for filename, (_, report) in variants.items()},
        }
        # Validate both variants and read every source member before output writes.
        # Retain all relationship files, even those now unused by removed shapes.
        members = [(info, archive.read(info)) for info in archive.infolist()]
        output_directory.mkdir(parents=True, exist_ok=True)
        for filename, (xml, _) in variants.items():
            with ZipFile(output_directory / filename, "x") as copy:
                copy.comment = archive.comment
                for info, data in members:
                    copy.writestr(info, xml if info.filename == part else data)
    manifest_path = output_directory / "review-manifest.json"
    with manifest_path.open("x", encoding="utf-8") as output:
        json.dump(manifest, output, indent=2, ensure_ascii=False, allow_nan=False)
        output.write("\n")
    return manifest_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("plan", type=Path)
    parser.add_argument("output_directory", type=Path)
    args = parser.parse_args()
    try:
        manifest_path = prepare_review(args.source, args.plan, args.output_directory)
    except (OSError, ValueError, KeyError, BadZipFile, ExpatError) as error:
        parser.exit(1, f"error: {error}\n")
    print(f"Prepared review copies: {manifest_path}\nRenderer status: pending (copy preparation only).")


if __name__ == "__main__":
    main()
