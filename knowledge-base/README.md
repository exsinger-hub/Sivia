# 科研绘图知识库

当前有效参考池包含 **10 对用户认可的图像—prompt 配对**：3 对历史参考和 7 对近期顶会 overview 扩充条目。每个条目都直接展示对应图片、完整 prompt 和案例详情。

未入库的 D4RT、AutoTool、SigmaDock 仍作为审阅草稿保留，状态单独标记，不进入正式参考池。

## 使用方法：paper 输入 → overview 输出

知识库服务于一条明确的科研绘图链路：输入论文 PDF、正文或方法描述，Sivia 先提取输入、模块、数据流和输出，再匹配下方案例，生成一张信息密度高、适合论文 overview 或附录展示的图片，并同步返回完整 prompt。确认图片后，可继续要求生成可编辑的 PowerPoint、WPS 或 draw.io 图件。

`paper.pdf / method text → overview image + complete prompt`

[机器索引](index.json) · [近期选定清单](overview-hot-domains-2025-26/selected-ledger.json) · [审阅候选](restart-2026/candidates.json) · [条件匹配数据库](restart-2026/conditional.sqlite) · [机器可读展示清单](showcase/index.json) · [贡献图文配对](CONTRIBUTING.md)

## 知识库图片总览

#### 三维重建与动态几何

<table>
<tr>
<td width="50%" valign="top" align="center">
<strong>Neuralangelo: High-Fidelity Neural Surface Reconstruction</strong><br>
<sub>已确认纳入</sub><br>
<a href="cases/neuralangelo/figure.png"><img src="cases/neuralangelo/figure.png" alt="Neuralangelo: High-Fidelity Neural Surface Reconstruction — 已确认纳入" width="440"></a><br>
<a href="cases/neuralangelo/figure.png">查看原图</a> · <a href="cases/neuralangelo/prompt.txt">完整 prompt</a> · <a href="cases/neuralangelo/README.md">案例详情</a>
</td>
<td width="50%" valign="top" align="center">
<strong>VGGT: Visual Geometry Grounded Transformer</strong><br>
<sub>已确认纳入</sub><br>
<a href="overview-hot-domains-2025-26/pairs/cvpr25-vggt/figure.png"><img src="overview-hot-domains-2025-26/pairs/cvpr25-vggt/figure.png" alt="VGGT: Visual Geometry Grounded Transformer — 已确认纳入" width="440"></a><br>
<a href="overview-hot-domains-2025-26/pairs/cvpr25-vggt/figure.png">查看原图</a> · <a href="overview-hot-domains-2025-26/pairs/cvpr25-vggt/prompt.txt">完整 prompt</a> · <a href="overview-hot-domains-2025-26/pairs/cvpr25-vggt/README.md">案例详情</a>
</td>
</tr>
<tr>
<td width="50%" valign="top" align="center">
<strong>MegaSaM: Accurate, Fast, and Robust Structure and Motion from Casual Dynamic Videos</strong><br>
<sub>已确认纳入</sub><br>
<a href="overview-hot-domains-2025-26/pairs/cvpr25-megasam/figure.png"><img src="overview-hot-domains-2025-26/pairs/cvpr25-megasam/figure.png" alt="MegaSaM: Accurate, Fast, and Robust Structure and Motion from Casual Dynamic Videos — 已确认纳入" width="440"></a><br>
<a href="overview-hot-domains-2025-26/pairs/cvpr25-megasam/figure.png">查看原图</a> · <a href="overview-hot-domains-2025-26/pairs/cvpr25-megasam/prompt.txt">完整 prompt</a> · <a href="overview-hot-domains-2025-26/pairs/cvpr25-megasam/README.md">案例详情</a>
</td>
<td width="50%" valign="top" align="center">
<strong>D4RT</strong><br>
<sub>审阅草稿 · 未入库</sub><br>
<a href="restart-2026/pairs/d4rt/figure.png"><img src="restart-2026/pairs/d4rt/figure.png" alt="D4RT — 审阅草稿 · 未入库" width="440"></a><br>
<a href="restart-2026/pairs/d4rt/figure.png">查看原图</a> · <a href="restart-2026/pairs/d4rt/prompt.txt">完整 prompt</a> · <a href="restart-2026/pairs/d4rt/README.md">案例详情</a>
</td>
</tr>
</table>

#### 代理、工具与检索

<table>
<tr>
<td width="50%" valign="top" align="center">
<strong>ReAct: Synergizing Reasoning and Acting in Language Models</strong><br>
<sub>已确认纳入</sub><br>
<a href="cases/react/figure.png"><img src="cases/react/figure.png" alt="ReAct: Synergizing Reasoning and Acting in Language Models — 已确认纳入" width="440"></a><br>
<a href="cases/react/figure.png">查看原图</a> · <a href="cases/react/prompt.txt">完整 prompt</a> · <a href="cases/react/README.md">案例详情</a>
</td>
<td width="50%" valign="top" align="center">
<strong>AutoTool</strong><br>
<sub>审阅草稿 · 未入库</sub><br>
<a href="restart-2026/pairs/autotool/figure.png"><img src="restart-2026/pairs/autotool/figure.png" alt="AutoTool — 审阅草稿 · 未入库" width="440"></a><br>
<a href="restart-2026/pairs/autotool/figure.png">查看原图</a> · <a href="restart-2026/pairs/autotool/prompt.txt">完整 prompt</a> · <a href="restart-2026/pairs/autotool/README.md">案例详情</a>
</td>
</tr>
</table>

#### 分子建模与科学人工智能

<table>
<tr>
<td width="50%" valign="top" align="center">
<strong>DiffDock: Diffusion Steps, Twists, and Turns for Molecular Docking</strong><br>
<sub>已确认纳入</sub><br>
<a href="cases/diffdock/figure.png"><img src="cases/diffdock/figure.png" alt="DiffDock: Diffusion Steps, Twists, and Turns for Molecular Docking — 已确认纳入" width="440"></a><br>
<a href="cases/diffdock/figure.png">查看原图</a> · <a href="cases/diffdock/prompt.txt">完整 prompt</a> · <a href="cases/diffdock/README.md">案例详情</a>
</td>
<td width="50%" valign="top" align="center">
<strong>SigmaDock</strong><br>
<sub>审阅草稿 · 未入库</sub><br>
<a href="restart-2026/pairs/sigmadock/figure.png"><img src="restart-2026/pairs/sigmadock/figure.png" alt="SigmaDock — 审阅草稿 · 未入库" width="440"></a><br>
<a href="restart-2026/pairs/sigmadock/figure.png">查看原图</a> · <a href="restart-2026/pairs/sigmadock/prompt.txt">完整 prompt</a> · <a href="restart-2026/pairs/sigmadock/README.md">案例详情</a>
</td>
</tr>
</table>

#### 世界模型与具身感知

<table>
<tr>
<td width="50%" valign="top" align="center">
<strong>Learning View-invariant World Models for Visual Robotic Manipulation</strong><br>
<sub>已确认纳入</sub><br>
<a href="overview-hot-domains-2025-26/pairs/iclr25-reviwo/figure.png"><img src="overview-hot-domains-2025-26/pairs/iclr25-reviwo/figure.png" alt="Learning View-invariant World Models for Visual Robotic Manipulation — 已确认纳入" width="440"></a><br>
<a href="overview-hot-domains-2025-26/pairs/iclr25-reviwo/figure.png">查看原图</a> · <a href="overview-hot-domains-2025-26/pairs/iclr25-reviwo/prompt.txt">完整 prompt</a> · <a href="overview-hot-domains-2025-26/pairs/iclr25-reviwo/README.md">案例详情</a>
</td>
<td width="50%" valign="top" align="center">
<strong>RoboSpatial: Teaching Spatial Understanding to 2D and 3D Vision-Language Models for Robotics</strong><br>
<sub>已确认纳入</sub><br>
<a href="overview-hot-domains-2025-26/pairs/cvpr25-robospatial/figure.png"><img src="overview-hot-domains-2025-26/pairs/cvpr25-robospatial/figure.png" alt="RoboSpatial: Teaching Spatial Understanding to 2D and 3D Vision-Language Models for Robotics — 已确认纳入" width="440"></a><br>
<a href="overview-hot-domains-2025-26/pairs/cvpr25-robospatial/figure.png">查看原图</a> · <a href="overview-hot-domains-2025-26/pairs/cvpr25-robospatial/prompt.txt">完整 prompt</a> · <a href="overview-hot-domains-2025-26/pairs/cvpr25-robospatial/README.md">案例详情</a>
</td>
</tr>
<tr>
<td width="50%" valign="top" align="center">
<strong>Reconstructing People, Places, and Cameras</strong><br>
<sub>已确认纳入</sub><br>
<a href="overview-hot-domains-2025-26/pairs/cvpr25-people-places-cameras/figure.png"><img src="overview-hot-domains-2025-26/pairs/cvpr25-people-places-cameras/figure.png" alt="Reconstructing People, Places, and Cameras — 已确认纳入" width="440"></a><br>
<a href="overview-hot-domains-2025-26/pairs/cvpr25-people-places-cameras/figure.png">查看原图</a> · <a href="overview-hot-domains-2025-26/pairs/cvpr25-people-places-cameras/prompt.txt">完整 prompt</a> · <a href="overview-hot-domains-2025-26/pairs/cvpr25-people-places-cameras/README.md">案例详情</a>
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
<a href="overview-hot-domains-2025-26/pairs/cvpr25-motion-aware-video-mllm/figure.png"><img src="overview-hot-domains-2025-26/pairs/cvpr25-motion-aware-video-mllm/figure.png" alt="Efficient Motion-Aware Video MLLM — 已确认纳入" width="440"></a><br>
<a href="overview-hot-domains-2025-26/pairs/cvpr25-motion-aware-video-mllm/figure.png">查看原图</a> · <a href="overview-hot-domains-2025-26/pairs/cvpr25-motion-aware-video-mllm/prompt.txt">完整 prompt</a> · <a href="overview-hot-domains-2025-26/pairs/cvpr25-motion-aware-video-mllm/README.md">案例详情</a>
</td>
<td width="50%" valign="top" align="center">
<strong>Dense-SfM: Structure from Motion with Dense Consistent Matching</strong><br>
<sub>已确认纳入</sub><br>
<a href="overview-hot-domains-2025-26/pairs/cvpr25-dense-sfm/figure.png"><img src="overview-hot-domains-2025-26/pairs/cvpr25-dense-sfm/figure.png" alt="Dense-SfM: Structure from Motion with Dense Consistent Matching — 已确认纳入" width="440"></a><br>
<a href="overview-hot-domains-2025-26/pairs/cvpr25-dense-sfm/figure.png">查看原图</a> · <a href="overview-hot-domains-2025-26/pairs/cvpr25-dense-sfm/prompt.txt">完整 prompt</a> · <a href="overview-hot-domains-2025-26/pairs/cvpr25-dense-sfm/README.md">案例详情</a>
</td>
</tr>
</table>
## 近期顶会选定条目

近期 7 对正式条目按三类整理：3D 几何与神经渲染、世界模型与具身感知、多模态与运动感知学习。完整来源、Prompt 和校验记录见 `overview-hot-domains-2025-26/`。

## 条件匹配

按领域、科学对象、机制拓扑、构图形式四个维度匹配 3 对历史锚点与 7 对近期选定 overview 条目。默认权重 0.30 / 0.30 / 0.25 / 0.15；匹配值低于 0.5 时不自动选择参考。该值是可解释的检索启发式，不是视觉质量分数。

```bash
python scripts/restart_conditional_kb.py --query d4rt
python scripts/validate_knowledge_base.py
```

新增图像是论文方法结构的概念性科研插图，不是实验结果或人类金标准；来源论文家族及其衍生物排除在未来封闭评测之外。
