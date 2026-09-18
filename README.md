<div align="center">

# Sivia

### From research papers to visual drafts. From approved drafts to editable figures.

[![Version](https://img.shields.io/badge/version-1.1.1-blue)](.codex-plugin/plugin.json)
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

## Installation

### Codex

```bash
codex plugin marketplace add exsinger-hub/Sivia --ref main
codex plugin add sivia@sivia
```

### Claude Code

```text
/plugin marketplace add exsinger-hub/Sivia
/plugin install sivia@sivia
```

## Development

From the repository root, with Node.js, Python 3/Pillow and PowerShell 7 available:

```bash
node scripts/sync-plugin-metadata.mjs --check
node --test tests/*.test.mjs
python -m unittest discover -s tests -p "test_*.py"
```

These tests exercise packaging, focus policy, payload behavior, arrow mapping, prompts, raster inspection and review-copy preparation. They do not replace live-application or visual tests. See [v1.1.1 changes](CHANGELOG.md).

## Acknowledgments

Built on [Scientific Illustrator](https://github.com/icebird1998/scientific-illustrator) by **icebird1998（一个地质博士）**, retaining its [MIT license and copyright](LICENSE). Sivia extends its editable drawing backends and Designer–Drawer–Reviewer–Corrector process with manuscript understanding, template-led ImageGen drafts and approval-locked reconstruction.

The bilingual README navigation and product-oriented organization take inspiration from [CC Switch](https://github.com/farion1231/cc-switch); its product claims and promotional content are not reused.

---

Thank you for using [Sivia](https://github.com/exsinger-hub/Sivia). Created by **gatina**.
