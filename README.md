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

![Agent Fleet — an ImageGen knowledge-base example](knowledge-base/cases/agent-fleet/figure.png)

<p align="center">Knowledge-base example, not a claim that every pixel is native-editable. <a href="knowledge-base/cases/agent-fleet/prompt.txt">Full prompt</a> · <a href="knowledge-base/cases/agent-fleet/README.md">Case notes</a></p>

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

### What you need

| Stage | Requirements |
| --- | --- |
| Read a paper and prepare a prompt | A client that can read your PDF/manuscript; Python 3 for prompt-length checks. |
| Generate or revise images | An image-generation tool available in the session. Sivia does not bundle a model, API key or paid image service. Claude Code needs an appropriate connected tool/MCP. |
| Inspect or mask artwork | Python 3 + Pillow. Local masking is used only when authorized and appropriate for the artwork. |
| Editable reconstruction | Node.js for the MCP servers, plus the selected drawing backend. File-backed PPTX requires Python and python-pptx; preview rendering is a separate capability. |

Backend availability is detected at runtime: Windows PowerPoint COM, connected macOS PowerPoint Office.js, native OOXML working copies, and the draw.io adapter have different capabilities. An installed application does not prove a connected document or successful rendering. Image-only work does not open presentation software.

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

## Knowledge base

The knowledge base now contains **42 actual image–prompt pairs**, including **36 paper-sourced conceptual examples** and 24 new pairs from major AI conferences. Every pair passes the low-whitespace admission screen; paper-sourced examples also received visual review.

| Category | Pairs |
| --- | ---: |
| [Multimodal and foundation representations](knowledge-base/README.md#multimodal-foundation) | 7 |
| [Generative modeling and control](knowledge-base/README.md#generative-control) | 6 |
| [Detection, segmentation and dense prediction](knowledge-base/README.md#detection-segmentation) | 7 |
| [3D representation, reconstruction and molecular space](knowledge-base/README.md#three-d-reconstruction) | 6 |
| [Agents, tool use and reasoning](knowledge-base/README.md#agents-reasoning) | 9 |
| [Time series, graphs, world models and robotics](knowledge-base/README.md#structured-robotics) | 7 |

Browse the complete categorized [knowledge-base index](knowledge-base/README.md), or use the machine-readable [`index.json`](knowledge-base/index.json). Each case includes the generated PNG, the exact full prompt and source/quality notes. Source families and derivatives are learning assets and are excluded from future sealed evaluation.

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
