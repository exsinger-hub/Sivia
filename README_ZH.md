<div align="center">

# Sivia

### 从论文到科研视觉稿，从确认稿到可编辑图件。

[![版本](https://img.shields.io/badge/version-1.1.1-blue)](.codex-plugin/plugin.json)
[![客户端](https://img.shields.io/badge/clients-Codex%20%7C%20Claude%20Code-orange)](#安装)
[![许可证](https://img.shields.io/badge/license-MIT-green)](LICENSE)

[English](README.md) | 简体中文

[快速开始](#快速开始) · [知识库](knowledge-base/README.md) · [更新日志](CHANGELOG.md)

</div>

Sivia 是面向 **Codex 与 Claude Code** 的科研绘图插件。核心链路很直接：**输入论文，输出 overview**。它先理解论文，从“成图＋完整 prompt”知识库中选择合适参考，再围绕方法的真实贡献编写精细 ImageGen prompt。

**默认第一轮交付图片、完整 prompt 和简短设计说明，不直接制作演示文稿。**

## 使用方法：paper 输入 → overview 输出

1. **输入 paper**：提供论文 PDF、正文，或方法部分的完整描述；同时说明希望突出的方法贡献、模块关系和实验对象。
2. **解析方法**：Sivia 提取输入、核心模块、数据流、训练/推理阶段、关键中间表示和输出，将其与知识库中的高质量 overview 案例匹配。
3. **生成 overview**：返回一张紧凑、信息密度高、可用于论文附录或方法概览的科研插图，并同时给出可复用的完整 prompt 与设计说明。
4. **继续编辑（可选）**：确认 overview 后，再明确要求制作可编辑的 PowerPoint、WPS 或 draw.io 图件。

可以把它理解为：`paper.pdf / method text → structured overview image + complete prompt`。

## 科研绘图知识库

当前有效参考池包含 **10 对用户认可的图像—prompt 配对**：3 对历史参考和 7 对近期顶会 overview 扩充条目。每个条目都以独立图片卡片展示，并提供完整 Prompt 与案例详情。

D4RT、AutoTool、SigmaDock 三个校准草稿仍保留为“审阅草稿 · 未入库”，不会混入正式参考池。

请查看[分类知识库](knowledge-base/README.md)、[近期选定清单](knowledge-base/overview-hot-domains-2025-26/selected-ledger.json)和[机器索引](knowledge-base/index.json)。

### 知识库图片总览

#### 三维重建与动态几何

<table>
<tr>
<td width="50%" valign="top" align="center">
<strong>Neuralangelo: High-Fidelity Neural Surface Reconstruction</strong><br>
<sub>已确认纳入</sub><br>
<a href="knowledge-base/cases/neuralangelo/figure.png"><img src="knowledge-base/cases/neuralangelo/figure.png" alt="Neuralangelo: High-Fidelity Neural Surface Reconstruction — 已确认纳入" width="440"></a><br>
<a href="knowledge-base/cases/neuralangelo/figure.png">查看原图</a> · <a href="knowledge-base/cases/neuralangelo/prompt.txt">完整 prompt</a> · <a href="knowledge-base/cases/neuralangelo/README.md">案例详情</a>
</td>
<td width="50%" valign="top" align="center">
<strong>VGGT: Visual Geometry Grounded Transformer</strong><br>
<sub>已确认纳入</sub><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-vggt/figure.png"><img src="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-vggt/figure.png" alt="VGGT: Visual Geometry Grounded Transformer — 已确认纳入" width="440"></a><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-vggt/figure.png">查看原图</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-vggt/prompt.txt">完整 prompt</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-vggt/README.md">案例详情</a>
</td>
</tr>
<tr>
<td width="50%" valign="top" align="center">
<strong>MegaSaM: Accurate, Fast, and Robust Structure and Motion from Casual Dynamic Videos</strong><br>
<sub>已确认纳入</sub><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-megasam/figure.png"><img src="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-megasam/figure.png" alt="MegaSaM: Accurate, Fast, and Robust Structure and Motion from Casual Dynamic Videos — 已确认纳入" width="440"></a><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-megasam/figure.png">查看原图</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-megasam/prompt.txt">完整 prompt</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-megasam/README.md">案例详情</a>
</td>
<td width="50%" valign="top" align="center">
<strong>D4RT</strong><br>
<sub>审阅草稿 · 未入库</sub><br>
<a href="knowledge-base/restart-2026/pairs/d4rt/figure.png"><img src="knowledge-base/restart-2026/pairs/d4rt/figure.png" alt="D4RT — 审阅草稿 · 未入库" width="440"></a><br>
<a href="knowledge-base/restart-2026/pairs/d4rt/figure.png">查看原图</a> · <a href="knowledge-base/restart-2026/pairs/d4rt/prompt.txt">完整 prompt</a> · <a href="knowledge-base/restart-2026/pairs/d4rt/README.md">案例详情</a>
</td>
</tr>
</table>

#### 代理、工具与检索

<table>
<tr>
<td width="50%" valign="top" align="center">
<strong>ReAct: Synergizing Reasoning and Acting in Language Models</strong><br>
<sub>已确认纳入</sub><br>
<a href="knowledge-base/cases/react/figure.png"><img src="knowledge-base/cases/react/figure.png" alt="ReAct: Synergizing Reasoning and Acting in Language Models — 已确认纳入" width="440"></a><br>
<a href="knowledge-base/cases/react/figure.png">查看原图</a> · <a href="knowledge-base/cases/react/prompt.txt">完整 prompt</a> · <a href="knowledge-base/cases/react/README.md">案例详情</a>
</td>
<td width="50%" valign="top" align="center">
<strong>AutoTool</strong><br>
<sub>审阅草稿 · 未入库</sub><br>
<a href="knowledge-base/restart-2026/pairs/autotool/figure.png"><img src="knowledge-base/restart-2026/pairs/autotool/figure.png" alt="AutoTool — 审阅草稿 · 未入库" width="440"></a><br>
<a href="knowledge-base/restart-2026/pairs/autotool/figure.png">查看原图</a> · <a href="knowledge-base/restart-2026/pairs/autotool/prompt.txt">完整 prompt</a> · <a href="knowledge-base/restart-2026/pairs/autotool/README.md">案例详情</a>
</td>
</tr>
</table>

#### 分子建模与科学人工智能

<table>
<tr>
<td width="50%" valign="top" align="center">
<strong>DiffDock: Diffusion Steps, Twists, and Turns for Molecular Docking</strong><br>
<sub>已确认纳入</sub><br>
<a href="knowledge-base/cases/diffdock/figure.png"><img src="knowledge-base/cases/diffdock/figure.png" alt="DiffDock: Diffusion Steps, Twists, and Turns for Molecular Docking — 已确认纳入" width="440"></a><br>
<a href="knowledge-base/cases/diffdock/figure.png">查看原图</a> · <a href="knowledge-base/cases/diffdock/prompt.txt">完整 prompt</a> · <a href="knowledge-base/cases/diffdock/README.md">案例详情</a>
</td>
<td width="50%" valign="top" align="center">
<strong>SigmaDock</strong><br>
<sub>审阅草稿 · 未入库</sub><br>
<a href="knowledge-base/restart-2026/pairs/sigmadock/figure.png"><img src="knowledge-base/restart-2026/pairs/sigmadock/figure.png" alt="SigmaDock — 审阅草稿 · 未入库" width="440"></a><br>
<a href="knowledge-base/restart-2026/pairs/sigmadock/figure.png">查看原图</a> · <a href="knowledge-base/restart-2026/pairs/sigmadock/prompt.txt">完整 prompt</a> · <a href="knowledge-base/restart-2026/pairs/sigmadock/README.md">案例详情</a>
</td>
</tr>
</table>

#### 世界模型与具身感知

<table>
<tr>
<td width="50%" valign="top" align="center">
<strong>Learning View-invariant World Models for Visual Robotic Manipulation</strong><br>
<sub>已确认纳入</sub><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/iclr25-reviwo/figure.png"><img src="knowledge-base/overview-hot-domains-2025-26/pairs/iclr25-reviwo/figure.png" alt="Learning View-invariant World Models for Visual Robotic Manipulation — 已确认纳入" width="440"></a><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/iclr25-reviwo/figure.png">查看原图</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/iclr25-reviwo/prompt.txt">完整 prompt</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/iclr25-reviwo/README.md">案例详情</a>
</td>
<td width="50%" valign="top" align="center">
<strong>RoboSpatial: Teaching Spatial Understanding to 2D and 3D Vision-Language Models for Robotics</strong><br>
<sub>已确认纳入</sub><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-robospatial/figure.png"><img src="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-robospatial/figure.png" alt="RoboSpatial: Teaching Spatial Understanding to 2D and 3D Vision-Language Models for Robotics — 已确认纳入" width="440"></a><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-robospatial/figure.png">查看原图</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-robospatial/prompt.txt">完整 prompt</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-robospatial/README.md">案例详情</a>
</td>
</tr>
<tr>
<td width="50%" valign="top" align="center">
<strong>Reconstructing People, Places, and Cameras</strong><br>
<sub>已确认纳入</sub><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-people-places-cameras/figure.png"><img src="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-people-places-cameras/figure.png" alt="Reconstructing People, Places, and Cameras — 已确认纳入" width="440"></a><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-people-places-cameras/figure.png">查看原图</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-people-places-cameras/prompt.txt">完整 prompt</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-people-places-cameras/README.md">案例详情</a>
</td>
<td width="50%" valign="top" align="center"></td>
</tr>
</table>

#### 多模态与运动感知学习

<table>
<tr>
<td width="50%" valign="top" align="center">
<strong>Efficient Motion-Aware Video MLLM</strong><br>
<sub>已确认纳入</sub><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-motion-aware-video-mllm/figure.png"><img src="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-motion-aware-video-mllm/figure.png" alt="Efficient Motion-Aware Video MLLM — 已确认纳入" width="440"></a><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-motion-aware-video-mllm/figure.png">查看原图</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-motion-aware-video-mllm/prompt.txt">完整 prompt</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-motion-aware-video-mllm/README.md">案例详情</a>
</td>
<td width="50%" valign="top" align="center">
<strong>Dense-SfM: Structure from Motion with Dense Consistent Matching</strong><br>
<sub>已确认纳入</sub><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-dense-sfm/figure.png"><img src="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-dense-sfm/figure.png" alt="Dense-SfM: Structure from Motion with Dense Consistent Matching — 已确认纳入" width="440"></a><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-dense-sfm/figure.png">查看原图</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-dense-sfm/prompt.txt">完整 prompt</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-dense-sfm/README.md">案例详情</a>
</td>
</tr>
</table>

## 安装

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

## 开发与测试

在仓库根目录运行，需要 Node.js、Python 3/Pillow 与 PowerShell 7：

```bash
node scripts/sync-plugin-metadata.mjs --check
node --test tests/*.test.mjs
python -m unittest discover -s tests -p "test_*.py"
```

测试覆盖打包、焦点策略、操作参数、箭头映射、prompt、素材检查与审阅副本生成，不代替真实软件显示和视觉审阅。见 [v1.1.1 更新](CHANGELOG.md)。

## 致谢

Sivia 基于 [Scientific Illustrator](https://github.com/icebird1998/scientific-illustrator) 改造与扩展。感谢原作者 **一个地质博士（icebird1998）** 提供的可编辑绘图后端，以及设计、绘制、审阅、修正的协作流程。Sivia 增加了论文理解、模板化 ImageGen 视觉稿和确认后的忠实复刻流程，保留原项目的 [MIT 许可证与版权声明](LICENSE)。

双语 README 的语言导航与产品介绍结构参考 [CC Switch](https://github.com/farion1231/cc-switch)，未复用其产品声明与推广文案。

---

感谢使用 [Sivia](https://github.com/exsinger-hub/Sivia) 插件，制作者：**gatina**。
