<div align="center">

# Sivia

### From research papers to visual drafts. From approved drafts to editable figures.

[![Version](https://img.shields.io/badge/version-1.1.1-blue)](.codex-plugin/plugin.json)
[![Clients](https://img.shields.io/badge/clients-Codex%20%7C%20Claude%20Code-orange)](#installation)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

English | [简体中文](README_ZH.md)

[Quick start](#quick-start) · [Workflow](docs/workflow.md) · [Knowledge base](knowledge-base/README.md) · [Changelog](CHANGELOG.md)

</div>

Sivia is a scientific-figure plugin for **Codex and Claude Code**. It reads your manuscript, finds relevant image-and-prompt examples, and develops a detailed ImageGen prompt around the method's actual contribution. You review the image first; editable PowerPoint, WPS or draw.io reconstruction is a separate, explicit choice.

**The default first delivery is an image, its complete prompt and a short design explanation—not a presentation.**

## Knowledge base

The active reference pool now contains **10 user-approved image–prompt pairs**: the historical Neuralangelo, ReAct and DiffDock anchors plus **7 recent top-conference overview additions** selected from the 12-image review round. The remaining five review drafts stay outside the active pool.

Browse the [classified knowledge base](knowledge-base/README.md), the [selected recent-overview ledger](knowledge-base/overview-hot-domains-2025-26/selected-ledger.json), or the [machine-readable active index](knowledge-base/index.json). Every selected entry includes its own image, exact prompt and case notes. All source families and derivatives remain excluded from future sealed evaluation.

### Selected recent overview gallery

#### 3D geometry and neural rendering

<table>
<tr>
<td width="50%" valign="top" align="center">
<strong>VGGT: Visual Geometry Grounded Transformer</strong><br>
<sub>User-selected and published</sub><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-vggt/figure.png"><img src="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-vggt/figure.png" alt="VGGT: Visual Geometry Grounded Transformer" width="440"></a><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-vggt/figure.png">Full-size image</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-vggt/prompt.txt">Full prompt</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-vggt/README.md">Case details</a>
</td>
<td width="50%" valign="top" align="center">
<strong>MegaSaM: Accurate, Fast, and Robust Structure and Motion from Casual Dynamic Videos</strong><br>
<sub>User-selected and published</sub><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-megasam/figure.png"><img src="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-megasam/figure.png" alt="MegaSaM: Accurate, Fast, and Robust Structure and Motion from Casual Dynamic Videos" width="440"></a><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-megasam/figure.png">Full-size image</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-megasam/prompt.txt">Full prompt</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-megasam/README.md">Case details</a>
</td>
</tr>
</table>

#### World models and embodied perception

<table>
<tr>
<td width="50%" valign="top" align="center">
<strong>Learning View-invariant World Models for Visual Robotic Manipulation</strong><br>
<sub>User-selected and published</sub><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/iclr25-reviwo/figure.png"><img src="knowledge-base/overview-hot-domains-2025-26/pairs/iclr25-reviwo/figure.png" alt="Learning View-invariant World Models for Visual Robotic Manipulation" width="440"></a><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/iclr25-reviwo/figure.png">Full-size image</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/iclr25-reviwo/prompt.txt">Full prompt</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/iclr25-reviwo/README.md">Case details</a>
</td>
<td width="50%" valign="top" align="center">
<strong>RoboSpatial: Teaching Spatial Understanding to 2D and 3D Vision-Language Models for Robotics</strong><br>
<sub>User-selected and published</sub><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-robospatial/figure.png"><img src="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-robospatial/figure.png" alt="RoboSpatial: Teaching Spatial Understanding to 2D and 3D Vision-Language Models for Robotics" width="440"></a><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-robospatial/figure.png">Full-size image</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-robospatial/prompt.txt">Full prompt</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-robospatial/README.md">Case details</a>
</td>
</tr>
<tr>
<td width="50%" valign="top" align="center">
<strong>Reconstructing People, Places, and Cameras</strong><br>
<sub>User-selected and published</sub><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-people-places-cameras/figure.png"><img src="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-people-places-cameras/figure.png" alt="Reconstructing People, Places, and Cameras" width="440"></a><br>
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
<sub>User-selected and published</sub><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-motion-aware-video-mllm/figure.png"><img src="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-motion-aware-video-mllm/figure.png" alt="Efficient Motion-Aware Video MLLM" width="440"></a><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-motion-aware-video-mllm/figure.png">Full-size image</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-motion-aware-video-mllm/prompt.txt">Full prompt</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-motion-aware-video-mllm/README.md">Case details</a>
</td>
<td width="50%" valign="top" align="center">
<strong>Dense-SfM: Structure from Motion with Dense Consistent Matching</strong><br>
<sub>User-selected and published</sub><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-dense-sfm/figure.png"><img src="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-dense-sfm/figure.png" alt="Dense-SfM: Structure from Motion with Dense Consistent Matching" width="440"></a><br>
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

## Limitations

- Image generation and native rendering depend on tools actually available in your session. Without ImageGen, Sivia can deliver a full prompt and explain what is missing; it will not skip approval and create a PPT instead.
- Faithful editable reconstruction preserves composition and semantics; it does not guarantee pixel-identical handwriting, textures or regenerated character designs. Low-resolution source art remains low-resolution.
- Generated illustrations are not experimental evidence. Missing measurements cannot be repaired by inventing plausible heatmaps or curves.
- A valid PPTX or an alternate-renderer preview is not PowerPoint/WPS verification. Unavailable target rendering stays pending, and dense source figures may need a separately approved layout change for smaller publication widths.
- Fonts may require installation. Editing notes identify approximations, native/raster boundaries and any non-attached routes.

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
