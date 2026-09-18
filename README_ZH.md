<div align="center">

# Sivia

### 从论文到科研视觉稿，从确认稿到可编辑图件。

[![版本](https://img.shields.io/badge/version-1.1.3-blue)](.codex-plugin/plugin.json)
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

## 快速开始

### 1. 从论文生成 Overview

上传论文即可开始。项目代码、真实实验素材、目标版面宽度与风格参考有助于提高准确性，但不要求你先自行寻找模板。

```text
使用 Sivia，根据我上传的论文设计并生成科研方法总览图。
以正文、公式及我提供的项目实现为科学依据，先简述核心图意和分区安排。
选择表达任务相近的知识库成图及其完整 prompt，编写逐区域完整 ImageGen prompt，
并按所选模板核验实际提交文本的长度。生成后检查方法关系、标签和最终尺寸可读性。
交付实际图片、完整 prompt 和简短设计说明；询问修改意见及是否需要可编辑 PPT，
然后暂停等待回复。本阶段不连接 PowerPoint/WPS，不创建演示文稿。
```

这是**用户需求示例**，不是直接提交给 ImageGen 的生产 prompt。Sivia 会展开具体对象、位置、比例、连接、标签和视觉规范；实际提交文本按非空白字符计，不得短于所绑定模板。制作说明可以详细，图内标签仍应简洁。

### 2. 只修改你指出的部分

```text
使用 Sivia，根据我附带的审阅意见局部修订当前视觉稿。
保留未涉及的画布比例、分区、配色和阅读路径；把修改整合进完整 prompt 并检查长度，
再生成并检查修订图片，保留上一版供比较。展示结果后等待我确认，暂不制作 PPT。
```

请附上具体意见或标注图。“这张图可以”仅表示图片获得认可，不等于授权制作 PPT。

### 3. 将确认稿复刻为可编辑图件

```text
使用 Sivia，将我明确确认的这张视觉稿忠实复刻为可编辑 PPTX。
保留布局、文字和可见连接关系；新建独立文件，不修改其他已打开文档。
文字、几何结构、图解和箭头使用原生对象；仅把不可进一步拆分的插画保留为独立图片。
后台执行；后端失败时，在上述范围内使用可用的独立原生文件路径继续推进。
检查实际保存的 PPTX 及其渲染预览，交付 PPTX、预览和简短的字体、素材、可编辑性说明，
明确标注尚未完成的目标软件显示核验。
```

需要 **WPS 演示**、**Microsoft PowerPoint**、**draw.io** 或指定文档的实时编辑时，请明确说明，不会静默改用其他软件。真实数据替换属于内容适配，需单独提出；忠实复刻保留确认稿可见内容，并将示意数值继续标识为示意。

## 为什么使用 Sivia？

- **先讲清研究，再决定布局。** 依据正文、公式与项目实现梳理图意，区分主图内容与正文细节。
- **参考成图，也参考完整 prompt。** 借鉴构图与图形语言，不借用其他方法的科学结论。
- **由你的确认控制下一阶段。** 生成、审阅、局部修订；明确要求后才进入可编辑复刻。
- **让关键结构真正可编辑。** 文字、模块、运算符、箭头和可重建图表使用原生对象，复杂插画独立保留。
- **失败后改变有效操作。** 面对低清裁图、假透明、无效属性设置或后端阻塞，在授权范围内寻找替代路径。
- **交付结论对应实际证据。** 分开说明文件有效、对象可编辑、实际文件预览、目标软件显示与最终尺寸可读性。

## 安装

### Codex

在终端执行：

```bash
codex plugin marketplace add exsinger-hub/Sivia --ref main
codex plugin add sivia@sivia
```

第一条注册仓库中的插件市场，第二条安装 Sivia。安装后新开任务使用。市场机制见 [OpenAI 官方插件说明](https://developers.openai.com/plugins/build/plugins)，本机命令可用 `codex plugin add --help` 核对。若安装过其他名称的旧版，请停用重复插件，避免同一组 skills 同时加载。

### Claude Code

在 Claude Code 对话内执行：

```text
/plugin marketplace add exsinger-hub/Sivia
/plugin install sivia@sivia
```

### 自愿 Star 邀请

助手协助你**首次安装成功时**，可以在安装完成消息中询问一次，是否愿意给 [exsinger-hub/Sivia](https://github.com/exsinger-hub/Sivia) 点 Star；仅在你同意后执行。升级、重装、启动和日常使用都不询问，跳过不影响任何功能。

安装助手须遵循[首次安装规则](skills/support-sivia/SKILL.md)，通过本地标记避免重复询问；设置 `SIVIA_STAR_INVITE=0` 可跳过。直接使用客户端原生插件管理器安装时，不弹出 Sivia 的 Star 询问，也不会留到第一次使用时补问。你仍可随时主动要求**“给 Sivia 点 Star”**。

### 运行条件

| 阶段 | 需要的能力 |
| --- | --- |
| 阅读论文、编写 prompt | 客户端能够读取 PDF/手稿；Python 3 用于 prompt 长度检查。 |
| 生成或修订图片 | 当前会话有可调用的生图工具。Sivia 不内置模型、API 密钥或付费生图服务；Claude Code 需连接相应工具或 MCP。 |
| 检查或遮罩处理插画 | Python 3＋Pillow。仅在本地处理获授权且适合该素材时使用遮罩。 |
| 可编辑复刻 | Node.js 运行 MCP 服务，并具备所选绘图后端。文件式 PPTX 需要 Python 与 python-pptx；预览渲染是独立能力。 |

后端能力以实际检测为准：Windows PowerPoint COM、已连接的 macOS PowerPoint Office.js、原生 OOXML 工作副本及 draw.io 适配器并不完全相同。安装了软件，不代表文档已连接或渲染已验证。仅图片阶段不打开演示软件。

## 哪些内容可以编辑？

| 内容 | 表示方式 |
| --- | --- |
| 标签、框线、网格、序列单元、简单图标 | 原生文字、形状或语义清晰的可编辑组合。 |
| 自定义线条图形与连线 | 后端支持的原生路径或基本图形；区分附着连接线与需手动调整端点的自由曲线。 |
| 定量曲线与图表 | 从原始测量值重绘为原生图表或具有准确数值和坐标的可编辑几何。 |
| 医学影像、预测和特征图 | 从真实来源分别导出，标签与标注单独可编辑。 |
| 复杂机器人、带纹理插画 | 优先合适的原始素材；获许可时独立生成，作为不带标签的单独图片。 |

PPT 没有现成图标时，可以用原生线条构建，或使用适合的独立素材。裁切本身不损失保留像素，放大低像素裁图才会暴露采样不足。SVG 可无损缩放，但不自动等于内部对象原生可编辑。

使用内置只读工具检查保留像素和真实透明通道：

```bash
python skills/design-scientific-figure/scripts/inspect_raster_asset.py --image robot.png --width-mm 30 --require-transparent
```

在插件根目录运行；加 `--crop-px LEFT TOP RIGHT BOTTOM` 可估算裁图。[素材生产规则](skills/design-scientific-figure/references/asset-production.md)包含像素规划和获授权后的轮廓遮罩后备方案。

## 开发与测试

在仓库根目录运行，需要 Node.js、Python 3/Pillow 与 PowerShell 7：

```bash
node scripts/sync-plugin-metadata.mjs --check
node --test tests/*.test.mjs
python -m unittest discover -s tests -p "test_*.py"
```

测试覆盖打包、焦点策略、操作参数、箭头映射、prompt、素材检查与审阅副本生成，不代替真实软件显示和视觉审阅。见 [v1.1.3 更新](CHANGELOG.md)。

## 致谢

Sivia 基于 [Scientific Illustrator](https://github.com/icebird1998/scientific-illustrator) 改造与扩展。感谢原作者 **一个地质博士（icebird1998）** 提供的可编辑绘图后端，以及设计、绘制、审阅、修正的协作流程。Sivia 增加了论文理解、模板化 ImageGen 视觉稿和确认后的忠实复刻流程，保留原项目的 [MIT 许可证与版权声明](LICENSE)。

双语 README 的语言导航与产品介绍结构参考 [CC Switch](https://github.com/farion1231/cc-switch)，未复用其产品声明与推广文案。

---

感谢使用 [Sivia](https://github.com/exsinger-hub/Sivia) 插件，制作者：**gatina**。
