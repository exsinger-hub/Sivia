<div align="center">

# Sivia

### 从论文到科研视觉稿，从确认稿到可编辑图件。

[![版本](https://img.shields.io/badge/version-1.1.1-blue)](.codex-plugin/plugin.json)
[![客户端](https://img.shields.io/badge/clients-Codex%20%7C%20Claude%20Code-orange)](#安装)
[![许可证](https://img.shields.io/badge/license-MIT-green)](LICENSE)

[English](README.md) | 简体中文

[快速开始](#快速开始) · [知识库](knowledge-base/README.md) · [更新日志](CHANGELOG.md)

</div>

Sivia 是面向 **Codex 与 Claude Code** 的科研绘图插件。它先理解论文，从“成图＋完整 prompt”知识库中选择合适参考，再围绕方法的真实贡献编写精细 ImageGen prompt。你先审阅图片；是否继续制作可编辑 PowerPoint、WPS 或 draw.io 图件，由你明确决定。

**默认第一轮交付图片、完整 prompt 和简短设计说明，不直接制作演示文稿。**

## 科研绘图知识库

当前有效参考池包含 **10 对用户认可的图像—prompt 配对**：Neuralangelo、ReAct、DiffDock 3 对历史参考，以及本次从 12 张审阅稿中选定的 7 对近期顶会 overview 扩充条目。其余 5 张仍留在审阅候选区。

请查看[分类知识库](knowledge-base/README.md)、[近期选定条目清单](knowledge-base/overview-hot-domains-2025-26/selected-ledger.json)和[机器索引](knowledge-base/index.json)。每个条目都包含对应图片、完整 prompt 与案例说明；所有来源论文家族及其衍生物继续排除在未来封闭评测之外。

### 近期选定 overview 图片

#### 3D 几何与神经渲染

<table>
<tr>
<td width="50%" valign="top" align="center">
<strong>VGGT: Visual Geometry Grounded Transformer</strong><br>
<sub>已确认纳入</sub><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-vggt/figure.png"><img src="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-vggt/figure.png" alt="VGGT: Visual Geometry Grounded Transformer" width="440"></a><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-vggt/figure.png">查看原图</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-vggt/prompt.txt">完整 prompt</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-vggt/README.md">案例详情</a>
</td>
<td width="50%" valign="top" align="center">
<strong>MegaSaM: Accurate, Fast, and Robust Structure and Motion from Casual Dynamic Videos</strong><br>
<sub>已确认纳入</sub><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-megasam/figure.png"><img src="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-megasam/figure.png" alt="MegaSaM: Accurate, Fast, and Robust Structure and Motion from Casual Dynamic Videos" width="440"></a><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-megasam/figure.png">查看原图</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-megasam/prompt.txt">完整 prompt</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-megasam/README.md">案例详情</a>
</td>
</tr>
</table>

#### 世界模型与具身感知

<table>
<tr>
<td width="50%" valign="top" align="center">
<strong>Learning View-invariant World Models for Visual Robotic Manipulation</strong><br>
<sub>已确认纳入</sub><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/iclr25-reviwo/figure.png"><img src="knowledge-base/overview-hot-domains-2025-26/pairs/iclr25-reviwo/figure.png" alt="Learning View-invariant World Models for Visual Robotic Manipulation" width="440"></a><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/iclr25-reviwo/figure.png">查看原图</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/iclr25-reviwo/prompt.txt">完整 prompt</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/iclr25-reviwo/README.md">案例详情</a>
</td>
<td width="50%" valign="top" align="center">
<strong>RoboSpatial: Teaching Spatial Understanding to 2D and 3D Vision-Language Models for Robotics</strong><br>
<sub>已确认纳入</sub><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-robospatial/figure.png"><img src="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-robospatial/figure.png" alt="RoboSpatial: Teaching Spatial Understanding to 2D and 3D Vision-Language Models for Robotics" width="440"></a><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-robospatial/figure.png">查看原图</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-robospatial/prompt.txt">完整 prompt</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-robospatial/README.md">案例详情</a>
</td>
</tr>
<tr>
<td width="50%" valign="top" align="center">
<strong>Reconstructing People, Places, and Cameras</strong><br>
<sub>已确认纳入</sub><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-people-places-cameras/figure.png"><img src="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-people-places-cameras/figure.png" alt="Reconstructing People, Places, and Cameras" width="440"></a><br>
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
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-motion-aware-video-mllm/figure.png"><img src="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-motion-aware-video-mllm/figure.png" alt="Efficient Motion-Aware Video MLLM" width="440"></a><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-motion-aware-video-mllm/figure.png">查看原图</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-motion-aware-video-mllm/prompt.txt">完整 prompt</a> · <a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-motion-aware-video-mllm/README.md">案例详情</a>
</td>
<td width="50%" valign="top" align="center">
<strong>Dense-SfM: Structure from Motion with Dense Consistent Matching</strong><br>
<sub>已确认纳入</sub><br>
<a href="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-dense-sfm/figure.png"><img src="knowledge-base/overview-hot-domains-2025-26/pairs/cvpr25-dense-sfm/figure.png" alt="Dense-SfM: Structure from Motion with Dense Consistent Matching" width="440"></a><br>
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

## Limitations

- 生图与原生渲染依赖当前会话的实际工具。没有 ImageGen 时可交付完整 prompt 并说明缺少的能力，不跳过确认直接制作 PPT。
- 可编辑复刻以布局和语义对应为目标，不保证手写字体、纹理或重新生成的角色逐像素一致。原始低清素材仍有分辨率上限。
- 生成插画不是实验结果，不能通过生成看似合理的热图、曲线补齐缺失测量。
- PPTX 有效或替代渲染器预览通过，不等于 PowerPoint/WPS 已验证。缺少目标软件渲染时保留待核验状态；高密度原图缩入更小版面可能需要另行同意的布局调整。
- 字体可能需要安装；编辑说明会区分字体近似、原生/位图边界和未附着的自由曲线。

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
