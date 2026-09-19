<div align="center">

# Sivia

### 论文 → 科研 Overview → 可编辑 PPT

**把论文里的方法，变成能继续修改的 PPT。**

[![版本](https://img.shields.io/badge/version-1.1.3-blue)](.codex-plugin/plugin.json)
[![客户端](https://img.shields.io/badge/clients-Codex%20%7C%20Claude%20Code-orange)](#安装)
[![许可证](https://img.shields.io/badge/license-MIT-green)](LICENSE)

[English](README.md) | 简体中文

[知识库与效果展示](#科研绘图知识库) · [快速开始](#快速开始) · [RSI](#rsi) · [安装](#安装)

</div>

Sivia 是面向 **Codex 与 Claude Code** 的科研绘图插件，服务于论文插图、组会汇报与答辩中的方法展示。上传论文，Sivia 梳理方法与贡献，结合**外挂知识库**生成 Overview；确认设计并要求制作 PPT 后，交付可在 **PowerPoint / WPS** 中继续修改的 **PPTX**。

改标签、移动模块、调整箭头、替换实验图片，都可以在交付文件中继续完成。同一张方法图，也能按论文版面和汇报场景调整。

| 能力 | 对你的用途 |
| --- | --- |
| **可编辑 PPT 交付** | 文字、模块和箭头按原生对象重建，复杂插画与实验图片独立放置，方便后续修改与复用。 |
| **外挂知识库** | 按领域、科学对象、方法关系与构图需求选择参考，也可使用你提供的课题组案例和风格素材。 |
| **局部修改与经验积累** | 根据反馈修改指定区域，保留已确认的布局；把认可案例与修订经验留作后续参考。 |

**交付链路：Paper → Overview 预览 → 确认并生成 PPT → 可编辑 PPTX + 预览。**

也支持将已有科研图复刻为可编辑图件，以及按需输出 draw.io 源文件。Sivia 进一步以 [RSI](#rsi) 为研究方向，探索让作图技能及其改进方法持续演进。

## 科研绘图知识库

**给科研绘图接上可扩充的外挂知识库。** Sivia 自带精选的科研图案例，也可结合你提供的论文参考图、课题组风格和已认可作品。知识库为新任务提供构图、层级、空间关系与图形表达的参考，具体科学内容由当前论文决定。

当前收录 **10 个已认可案例**，覆盖下方五类方向；另有 **3 个审阅草稿**，在卡片中单独标记。以下展示 Overview 图片，制作记录与来源可以逐项查看。

[浏览分类知识库](knowledge-base/README.md) · [扩充自己的案例库](knowledge-base/CONTRIBUTING.md)

### 三维重建与动态几何

<table>
<tr>
<td width="50%" valign="top" align="center">
<strong>Neuralangelo: High-Fidelity Neural Surface Reconstruction</strong><br>
<sub>已确认纳入</sub><br>
<a href="knowledge-base/cases/neuralangelo/figure.png"><img src="knowledge-base/cases/neuralangelo/figure.png" alt="Neuralangelo: High-Fidelity Neural Surface Reconstruction — 已确认纳入" width="440"></a><br>
<a href="knowledge-base/cases/neuralangelo/figure.png">查看原图</a> · <a href="knowledge-base/cases/neuralangelo/prompt.txt">制作记录</a> · <a href="knowledge-base/cases/neuralangelo/README.md">案例详情</a>
</td>
<td width="50%" valign="top" align="center">
<strong>VGGT: Visual Geometry Grounded Transformer</strong><br>
<sub>已确认纳入</sub><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-vggt/figure.png"><img src="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-vggt/figure.png" alt="VGGT: Visual Geometry Grounded Transformer — 已确认纳入" width="440"></a><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-vggt/figure.png">查看原图</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-vggt/prompt.txt">制作记录</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-vggt/README.md">案例详情</a>
</td>
</tr>
<tr>
<td width="50%" valign="top" align="center">
<strong>MegaSaM: Accurate, Fast, and Robust Structure and Motion from Casual Dynamic Videos</strong><br>
<sub>已确认纳入</sub><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-megasam/figure.png"><img src="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-megasam/figure.png" alt="MegaSaM: Accurate, Fast, and Robust Structure and Motion from Casual Dynamic Videos — 已确认纳入" width="440"></a><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-megasam/figure.png">查看原图</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-megasam/prompt.txt">制作记录</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-megasam/README.md">案例详情</a>
</td>
<td width="50%" valign="top" align="center">
<strong>D4RT</strong><br>
<sub>审阅草稿 · 未入库</sub><br>
<a href="knowledge-base/restart-2026/pairs/d4rt/figure.png"><img src="knowledge-base/restart-2026/pairs/d4rt/figure.png" alt="D4RT — 审阅草稿 · 未入库" width="440"></a><br>
<a href="knowledge-base/restart-2026/pairs/d4rt/figure.png">查看原图</a> · <a href="knowledge-base/restart-2026/pairs/d4rt/prompt.txt">制作记录</a> · <a href="knowledge-base/restart-2026/pairs/d4rt/README.md">案例详情</a>
</td>
</tr>
</table>

### 代理、工具与检索

<table>
<tr>
<td width="50%" valign="top" align="center">
<strong>ReAct: Synergizing Reasoning and Acting in Language Models</strong><br>
<sub>已确认纳入</sub><br>
<a href="knowledge-base/cases/react/figure.png"><img src="knowledge-base/cases/react/figure.png" alt="ReAct: Synergizing Reasoning and Acting in Language Models — 已确认纳入" width="440"></a><br>
<a href="knowledge-base/cases/react/figure.png">查看原图</a> · <a href="knowledge-base/cases/react/prompt.txt">制作记录</a> · <a href="knowledge-base/cases/react/README.md">案例详情</a>
</td>
<td width="50%" valign="top" align="center">
<strong>AutoTool</strong><br>
<sub>审阅草稿 · 未入库</sub><br>
<a href="knowledge-base/restart-2026/pairs/autotool/figure.png"><img src="knowledge-base/restart-2026/pairs/autotool/figure.png" alt="AutoTool — 审阅草稿 · 未入库" width="440"></a><br>
<a href="knowledge-base/restart-2026/pairs/autotool/figure.png">查看原图</a> · <a href="knowledge-base/restart-2026/pairs/autotool/prompt.txt">制作记录</a> · <a href="knowledge-base/restart-2026/pairs/autotool/README.md">案例详情</a>
</td>
</tr>
</table>

### 分子建模与科学人工智能

<table>
<tr>
<td width="50%" valign="top" align="center">
<strong>DiffDock: Diffusion Steps, Twists, and Turns for Molecular Docking</strong><br>
<sub>已确认纳入</sub><br>
<a href="knowledge-base/cases/diffdock/figure.png"><img src="knowledge-base/cases/diffdock/figure.png" alt="DiffDock: Diffusion Steps, Twists, and Turns for Molecular Docking — 已确认纳入" width="440"></a><br>
<a href="knowledge-base/cases/diffdock/figure.png">查看原图</a> · <a href="knowledge-base/cases/diffdock/prompt.txt">制作记录</a> · <a href="knowledge-base/cases/diffdock/README.md">案例详情</a>
</td>
<td width="50%" valign="top" align="center">
<strong>SigmaDock</strong><br>
<sub>审阅草稿 · 未入库</sub><br>
<a href="knowledge-base/restart-2026/pairs/sigmadock/figure.png"><img src="knowledge-base/restart-2026/pairs/sigmadock/figure.png" alt="SigmaDock — 审阅草稿 · 未入库" width="440"></a><br>
<a href="knowledge-base/restart-2026/pairs/sigmadock/figure.png">查看原图</a> · <a href="knowledge-base/restart-2026/pairs/sigmadock/prompt.txt">制作记录</a> · <a href="knowledge-base/restart-2026/pairs/sigmadock/README.md">案例详情</a>
</td>
</tr>
</table>

### 世界模型与具身感知

<table>
<tr>
<td width="50%" valign="top" align="center">
<strong>Learning View-invariant World Models for Visual Robotic Manipulation</strong><br>
<sub>已确认纳入</sub><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/iclr25-reviwo/figure.png"><img src="knowledge-base/overview-hot-domains-2025-26/pairs/iclr25-reviwo/figure.png" alt="Learning View-invariant World Models for Visual Robotic Manipulation — 已确认纳入" width="440"></a><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/iclr25-reviwo/figure.png">查看原图</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/iclr25-reviwo/prompt.txt">制作记录</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/iclr25-reviwo/README.md">案例详情</a>
</td>
<td width="50%" valign="top" align="center">
<strong>RoboSpatial: Teaching Spatial Understanding to 2D and 3D Vision-Language Models for Robotics</strong><br>
<sub>已确认纳入</sub><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-robospatial/figure.png"><img src="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-robospatial/figure.png" alt="RoboSpatial: Teaching Spatial Understanding to 2D and 3D Vision-Language Models for Robotics — 已确认纳入" width="440"></a><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-robospatial/figure.png">查看原图</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-robospatial/prompt.txt">制作记录</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-robospatial/README.md">案例详情</a>
</td>
</tr>
<tr>
<td width="50%" valign="top" align="center">
<strong>Reconstructing People, Places, and Cameras</strong><br>
<sub>已确认纳入</sub><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-people-places-cameras/figure.png"><img src="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-people-places-cameras/figure.png" alt="Reconstructing People, Places, and Cameras — 已确认纳入" width="440"></a><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-people-places-cameras/figure.png">查看原图</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-people-places-cameras/prompt.txt">制作记录</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-people-places-cameras/README.md">案例详情</a>
</td>
<td width="50%" valign="top" align="center"></td>
</tr>
</table>

### 多模态与运动感知学习

<table>
<tr>
<td width="50%" valign="top" align="center">
<strong>Efficient Motion-Aware Video MLLM</strong><br>
<sub>已确认纳入</sub><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-motion-aware-video-mllm/figure.png"><img src="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-motion-aware-video-mllm/figure.png" alt="Efficient Motion-Aware Video MLLM — 已确认纳入" width="440"></a><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-motion-aware-video-mllm/figure.png">查看原图</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-motion-aware-video-mllm/prompt.txt">制作记录</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-motion-aware-video-mllm/README.md">案例详情</a>
</td>
<td width="50%" valign="top" align="center">
<strong>Dense-SfM: Structure from Motion with Dense Consistent Matching</strong><br>
<sub>已确认纳入</sub><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-dense-sfm/figure.png"><img src="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-dense-sfm/figure.png" alt="Dense-SfM: Structure from Motion with Dense Consistent Matching — 已确认纳入" width="440"></a><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-dense-sfm/figure.png">查看原图</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-dense-sfm/prompt.txt">制作记录</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-dense-sfm/README.md">案例详情</a>
</td>
</tr>
</table>

## 快速开始

安装后，在 Codex 或 Claude Code 中上传论文，直接说明你需要的图即可。

### 1. 上传 Paper，生成 Overview

```text
使用 Sivia，为这篇论文生成一张科研 Overview。
突出核心创新、关键模块和输入输出关系，构图紧凑，适合论文展示。
```

Sivia 负责理解论文、选择参考、设计构图并生成图片。你先看效果，再决定需要修改哪里。

### 2. 确认设计，生成可编辑 PPT

```text
这版 Overview 已确认。请用 Sivia 生成可编辑 PPTX，保留当前布局和内容。
文字、模块和箭头使用原生对象，插画与实验图片独立保留，方便我后续修改。
```

交付 **PPTX + 预览**。打开 PowerPoint 或 WPS 后，可以继续调整文字、模块位置与素材；已有满意的科研图，也可以直接从这一步开始。

### 3. 按反馈局部修改

```text
把右侧输出模块移到下方，调整对应箭头，增大图内标签。
保留其他区域的布局、内容与配色，更新可编辑 PPT 和预览。
```

**使用自己的外挂知识库：** 把参考图或案例目录一并提供，并告诉 Sivia：“优先参考这些案例的构图和配色，用当前论文的方法内容重新设计。”

## RSI

**Recursive Self-Improvement · 递归自我改进（研究方向）**

一次修订的价值，可以延续到下一次作图。Sivia 当前通过设计、绘制、审阅与修正流程改进图件，并将认可的作品、参考素材和有用反馈保存为本地案例；你可以在后续任务中继续使用这些经验。

RSI 的下一步是同时研究**作图技能**与**更新技能的方法**：从修订反馈中提出规则，在新任务上检验，再探索如何递归改进规则的更新策略。这是 Sivia 的演进路线；当前开源版提供可编辑绘图与案例积累，递归更新策略属于后续研究。

## 安装

### Codex

在终端执行，安装后新开任务：

```bash
codex plugin marketplace add exsinger-hub/Sivia --ref main
codex plugin add sivia@sivia
```

### Claude Code

在 Claude Code 中执行：

```text
/plugin marketplace add exsinger-hub/Sivia
/plugin install sivia@sivia
```

## 开发与文档

[完整工作流程](docs/workflow_ZH.md) · [更新日志](CHANGELOG.md) · [知识库贡献指南](knowledge-base/CONTRIBUTING.md)

在仓库根目录运行检查：

```bash
node scripts/sync-plugin-metadata.mjs --check
node --test tests/*.test.mjs
python -m unittest discover -s tests -p "test_*.py"
```

## 致谢

Sivia 基于 [Scientific Illustrator](https://github.com/icebird1998/scientific-illustrator) 改造与扩展。感谢原作者 **一个地质博士（icebird1998）** 提供的可编辑绘图后端，以及设计、绘制、审阅、修正的协作流程。Sivia 增加了论文理解、模板化 ImageGen 视觉稿和确认后的忠实复刻流程，保留原项目的 [MIT 许可证与版权声明](LICENSE)。

双语 README 的语言导航与产品介绍结构参考 [CC Switch](https://github.com/farion1231/cc-switch)，未复用其产品声明与推广文案。

---

感谢使用 [Sivia](https://github.com/exsinger-hub/Sivia) 插件，制作者：**gatina**。
