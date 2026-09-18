<div align="center">

# Sivia

### From research papers to visual drafts. From approved drafts to editable figures.

[![Version](https://img.shields.io/badge/version-1.1.3-blue)](.codex-plugin/plugin.json)
[![Clients](https://img.shields.io/badge/clients-Codex%20%7C%20Claude%20Code-orange)](#installation)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

English | [简体中文](README_ZH.md)

[Quick start](#quick-start) · [Workflow](docs/workflow.md) · [Knowledge base](knowledge-base/README.md) · [Changelog](CHANGELOG.md)

</div>

Sivia is a scientific-figure plugin for **Codex and Claude Code**. The core workflow is direct: **paper in, overview out**. It reads your manuscript, finds relevant image-and-prompt examples, and develops a detailed ImageGen prompt around the method's actual contribution.

**The default first delivery is an image, its complete prompt and a short design explanation—not a presentation.**

## Usage: paper in → overview out

1. **Input a paper**: provide a PDF, manuscript text, or a complete method description, with the contribution, modules, and scientific objects you want emphasized.
2. **Parse the method**: Sivia extracts inputs, modules, data flow, training/inference stages, intermediate representations, and outputs, then matches them to high-quality overview examples in the knowledge base.
3. **Generate the overview**: receive a compact, information-dense scientific overview figure suitable for a paper appendix or method overview, together with the reusable full prompt and design notes.
4. **Edit further (optional)**: after approving the overview, explicitly request an editable PowerPoint, WPS, or draw.io reconstruction.

The pipeline is: `paper.pdf / method text → structured overview image + complete prompt`.

## Knowledge base

The active reference pool contains **10 user-approved image–prompt pairs**: three historical anchors and seven recent top-conference overview additions. Each entry is displayed as its own image card with the full prompt and case details.

The D4RT, AutoTool and SigmaDock calibration drafts remain visibly marked as review-only and are outside the active reference pool.

Browse the [classified knowledge base](knowledge-base/README.md), the [selected recent-overview ledger](knowledge-base/overview-hot-domains-2025-26/selected-ledger.json), or the [active index](knowledge-base/index.json).

### Knowledge-base image gallery

#### 3D reconstruction and dynamic geometry

<table>
<tr>
<td width="50%" valign="top" align="center">
<strong>Neuralangelo: High-Fidelity Neural Surface Reconstruction</strong><br>
<sub>User-selected / active</sub><br>
<a href="knowledge-base/cases/neuralangelo/figure.png"><img src="knowledge-base/cases/neuralangelo/figure.png" alt="Neuralangelo: High-Fidelity Neural Surface Reconstruction — User-selected / active" width="440"></a><br>
<a href="knowledge-base/cases/neuralangelo/figure.png">Full-size image</a> · <a href="knowledge-base/cases/neuralangelo/prompt.txt">Full prompt</a> · <a href="knowledge-base/cases/neuralangelo/README.md">Case details</a>
</td>
<td width="50%" valign="top" align="center">
<strong>VGGT: Visual Geometry Grounded Transformer</strong><br>
<sub>User-selected / active</sub><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-vggt/figure.png"><img src="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-vggt/figure.png" alt="VGGT: Visual Geometry Grounded Transformer — User-selected / active" width="440"></a><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-vggt/figure.png">Full-size image</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-vggt/prompt.txt">Full prompt</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-vggt/README.md">Case details</a>
</td>
</tr>
<tr>
<td width="50%" valign="top" align="center">
<strong>MegaSaM: Accurate, Fast, and Robust Structure and Motion from Casual Dynamic Videos</strong><br>
<sub>User-selected / active</sub><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-megasam/figure.png"><img src="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-megasam/figure.png" alt="MegaSaM: Accurate, Fast, and Robust Structure and Motion from Casual Dynamic Videos — User-selected / active" width="440"></a><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-megasam/figure.png">Full-size image</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-megasam/prompt.txt">Full prompt</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-megasam/README.md">Case details</a>
</td>
<td width="50%" valign="top" align="center">
<strong>D4RT</strong><br>
<sub>Review draft · not admitted</sub><br>
<a href="knowledge-base/restart-2026/pairs/d4rt/figure.png"><img src="knowledge-base/restart-2026/pairs/d4rt/figure.png" alt="D4RT — Review draft · not admitted" width="440"></a><br>
<a href="knowledge-base/restart-2026/pairs/d4rt/figure.png">Full-size image</a> · <a href="knowledge-base/restart-2026/pairs/d4rt/prompt.txt">Full prompt</a> · <a href="knowledge-base/restart-2026/pairs/d4rt/README.md">Case details</a>
</td>
</tr>
</table>

#### Agents, tools and retrieval

<table>
<tr>
<td width="50%" valign="top" align="center">
<strong>ReAct: Synergizing Reasoning and Acting in Language Models</strong><br>
<sub>User-selected / active</sub><br>
<a href="knowledge-base/cases/react/figure.png"><img src="knowledge-base/cases/react/figure.png" alt="ReAct: Synergizing Reasoning and Acting in Language Models — User-selected / active" width="440"></a><br>
<a href="knowledge-base/cases/react/figure.png">Full-size image</a> · <a href="knowledge-base/cases/react/prompt.txt">Full prompt</a> · <a href="knowledge-base/cases/react/README.md">Case details</a>
</td>
<td width="50%" valign="top" align="center">
<strong>AutoTool</strong><br>
<sub>Review draft · not admitted</sub><br>
<a href="knowledge-base/restart-2026/pairs/autotool/figure.png"><img src="knowledge-base/restart-2026/pairs/autotool/figure.png" alt="AutoTool — Review draft · not admitted" width="440"></a><br>
<a href="knowledge-base/restart-2026/pairs/autotool/figure.png">Full-size image</a> · <a href="knowledge-base/restart-2026/pairs/autotool/prompt.txt">Full prompt</a> · <a href="knowledge-base/restart-2026/pairs/autotool/README.md">Case details</a>
</td>
</tr>
</table>

#### Molecular modeling and AI for Science

<table>
<tr>
<td width="50%" valign="top" align="center">
<strong>DiffDock: Diffusion Steps, Twists, and Turns for Molecular Docking</strong><br>
<sub>User-selected / active</sub><br>
<a href="knowledge-base/cases/diffdock/figure.png"><img src="knowledge-base/cases/diffdock/figure.png" alt="DiffDock: Diffusion Steps, Twists, and Turns for Molecular Docking — User-selected / active" width="440"></a><br>
<a href="knowledge-base/cases/diffdock/figure.png">Full-size image</a> · <a href="knowledge-base/cases/diffdock/prompt.txt">Full prompt</a> · <a href="knowledge-base/cases/diffdock/README.md">Case details</a>
</td>
<td width="50%" valign="top" align="center">
<strong>SigmaDock</strong><br>
<sub>Review draft · not admitted</sub><br>
<a href="knowledge-base/restart-2026/pairs/sigmadock/figure.png"><img src="knowledge-base/restart-2026/pairs/sigmadock/figure.png" alt="SigmaDock — Review draft · not admitted" width="440"></a><br>
<a href="knowledge-base/restart-2026/pairs/sigmadock/figure.png">Full-size image</a> · <a href="knowledge-base/restart-2026/pairs/sigmadock/prompt.txt">Full prompt</a> · <a href="knowledge-base/restart-2026/pairs/sigmadock/README.md">Case details</a>
</td>
</tr>
</table>

#### World models and embodied perception

<table>
<tr>
<td width="50%" valign="top" align="center">
<strong>Learning View-invariant World Models for Visual Robotic Manipulation</strong><br>
<sub>User-selected / active</sub><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/iclr25-reviwo/figure.png"><img src="knowledge-base/overview-hot-domains-2025-26/pairs/iclr25-reviwo/figure.png" alt="Learning View-invariant World Models for Visual Robotic Manipulation — User-selected / active" width="440"></a><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/iclr25-reviwo/figure.png">Full-size image</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/iclr25-reviwo/prompt.txt">Full prompt</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/iclr25-reviwo/README.md">Case details</a>
</td>
<td width="50%" valign="top" align="center">
<strong>RoboSpatial: Teaching Spatial Understanding to 2D and 3D Vision-Language Models for Robotics</strong><br>
<sub>User-selected / active</sub><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-robospatial/figure.png"><img src="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-robospatial/figure.png" alt="RoboSpatial: Teaching Spatial Understanding to 2D and 3D Vision-Language Models for Robotics — User-selected / active" width="440"></a><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-robospatial/figure.png">Full-size image</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-robospatial/prompt.txt">Full prompt</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-robospatial/README.md">Case details</a>
</td>
</tr>
<tr>
<td width="50%" valign="top" align="center">
<strong>Reconstructing People, Places, and Cameras</strong><br>
<sub>User-selected / active</sub><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-people-places-cameras/figure.png"><img src="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-people-places-cameras/figure.png" alt="Reconstructing People, Places, and Cameras — User-selected / active" width="440"></a><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-people-places-cameras/figure.png">Full-size image</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-people-places-cameras/prompt.txt">Full prompt</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-people-places-cameras/README.md">Case details</a>
</td>
<td width="50%" valign="top" align="center"></td>
</tr>
</table>

#### Multimodal and motion-aware learning

<table>
<tr>
<td width="50%" valign="top" align="center">
<strong>Efficient Motion-Aware Video MLLM</strong><br>
<sub>User-selected / active</sub><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-motion-aware-video-mllm/figure.png"><img src="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-motion-aware-video-mllm/figure.png" alt="Efficient Motion-Aware Video MLLM — User-selected / active" width="440"></a><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-motion-aware-video-mllm/figure.png">Full-size image</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-motion-aware-video-mllm/prompt.txt">Full prompt</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-motion-aware-video-mllm/README.md">Case details</a>
</td>
<td width="50%" valign="top" align="center">
<strong>Dense-SfM: Structure from Motion with Dense Consistent Matching</strong><br>
<sub>User-selected / active</sub><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-dense-sfm/figure.png"><img src="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-dense-sfm/figure.png" alt="Dense-SfM: Structure from Motion with Dense Consistent Matching — User-selected / active" width="440"></a><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-dense-sfm/figure.png">Full-size image</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-dense-sfm/prompt.txt">Full prompt</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-dense-sfm/README.md">Case details</a>
</td>
</tr>
</table>

## Quick start

### 1. Make a paper overview

Attach the paper. Code, real experiment assets, target figure width and style references are useful when available, not mandatory template-selection homework.

```text
Use Sivia to design and generate a scientific method overview from my attached paper.
Ground the content in the manuscript, equations and supplied implementation. Explain the main
message and proposed regions first. Select a relevant knowledge-base image and its complete
prompt, then write and validate the full region-specific ImageGen prompt against that template.
Generate and inspect the image. Deliver the actual image, full prompt and short design notes.
Ask for my revisions and whether I want an editable PPT, then stop. Do not open PowerPoint/WPS.
```

Sivia expands this **user request** into the actual production prompt. Before generation, the exact submitted prompt must contain at least as many non-whitespace characters as its bound template. Detailed production instructions do not mean verbose labels inside the figure.

### 2. Revise only what you name

```text
Use Sivia to revise the current visual draft according to my attached comments.
Keep the approved ratio, regions, palette and reading path outside the affected objects.
Integrate the changes into the complete prompt, validate its length, generate and inspect
the revised image, and retain the previous version. Show me the result and wait; no PPT yet.
```

Add your actual comments or annotated image. “This image looks good” approves the image; it does not authorize a deck.

### 3. Reconstruct the approved image

```text
Use Sivia to faithfully reconstruct this explicitly approved visual draft as an editable PPTX.
Preserve its layout, wording and visible connections. Create a separate file; do not modify
other open documents. Rebuild text, geometry, diagrams and arrows as native objects; retain
only irreducible artwork as independent pictures. Keep work in the background.
If a backend fails, recover within this scope using an available isolated native-file route.
Inspect the actual saved PPTX and its rendered preview. Deliver the PPTX, preview and concise
notes about fonts, assets, editability and any pending target-application verification.
```

Specify **WPS**, **Microsoft PowerPoint**, **draw.io**, or a required live document when that choice matters. A constrained backend is not silently replaced. Real-data substitution is a separate adaptation request: a faithful-copy request preserves the approved visible content and identifies schematic values as schematic.

## Why Sivia?

- **A scientific story before a layout.** Ground the figure in the manuscript, equations and supplied implementation; identify what belongs in the overview and what belongs in the paper.
- **Templates with their actual outputs.** Learn composition and graphic language from paired images and complete prompts, without importing another method's scientific claims.
- **Your approval controls the next stage.** Generate → review → revise. Start editable reconstruction only when you ask for it.
- **Edit the structure that matters.** Text, modules, operators, arrows and reconstructable charts stay native; complex illustrations remain independent assets.
- **Failures lead to a changed action.** Recover from inadequate crops, false transparency, ineffective setters and stalled backends within the authorized scope.
- **Evidence-backed delivery.** Distinguish file validity, editability, exact-file preview, target-application rendering and final-size readability.

## Installation

### Codex

Run in a terminal:

```bash
codex plugin marketplace add exsinger-hub/Sivia --ref main
codex plugin add sivia@sivia
```

The first command registers the repository marketplace; the second installs Sivia. Start a new task after installation. See [OpenAI's plugin packaging documentation](https://developers.openai.com/plugins/build/plugins); use `codex plugin add --help` to check your local CLI. Disable an older differently named copy if both expose the same skills.

### Claude Code

Run inside Claude Code:

```text
/plugin marketplace add exsinger-hub/Sivia
/plugin install sivia@sivia
```

## What stays editable?

| Content | Representation |
| --- | --- |
| Labels, boxes, grids, token strips, simple icons | Native text/shapes or meaningful editable groups. |
| Custom line art and connectors | Native paths/primitives where supported; distinguish attached connectors from manually adjustable curves. |
| Quantitative plots | Original measurements → native charts or editable geometry with exact values and scales. |
| Medical images, predictions and feature maps | Individual exports from the real source; separate editable overlays. |
| Detailed robots and textured illustrations | Suitable source artwork, or separately generated assets when permitted; independent pictures with no baked-in labels. |

No stock PPT icon? Build the geometry or choose an appropriate independent asset. Cropping alone does not blur pixels; enlarging a small crop exposes its limited sampling. SVG can scale cleanly without offering native subobject editing.

Inspect retained pixels and real alpha with the bundled read-only helper:

```bash
python skills/design-scientific-figure/scripts/inspect_raster_asset.py --image robot.png --width-mm 30 --require-transparent
```

Run from the plugin root. Add `--crop-px LEFT TOP RIGHT BOTTOM` to evaluate a crop. See [asset production](skills/design-scientific-figure/references/asset-production.md) for source-resolution planning and authorized contour-mask recovery.

## Development

From the repository root, with Node.js, Python 3/Pillow and PowerShell 7 available:

```bash
node scripts/sync-plugin-metadata.mjs --check
node --test tests/*.test.mjs
python -m unittest discover -s tests -p "test_*.py"
```

These tests exercise packaging, focus policy, payload behavior, arrow mapping, prompts, raster inspection and review-copy preparation. They do not replace live-application or visual tests. See [v1.1.3 changes](CHANGELOG.md).

## Acknowledgments

Built on [Scientific Illustrator](https://github.com/icebird1998/scientific-illustrator) by **icebird1998（一个地质博士）**, retaining its [MIT license and copyright](LICENSE). Sivia extends its editable drawing backends and Designer–Drawer–Reviewer–Corrector process with manuscript understanding, template-led ImageGen drafts and approval-locked reconstruction.

The bilingual README navigation and product-oriented organization take inspiration from [CC Switch](https://github.com/farion1231/cc-switch); its product claims and promotional content are not reused.

---

Thank you for using [Sivia](https://github.com/exsinger-hub/Sivia). Created by **gatina**.
