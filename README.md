# Sivia

[**Sivia**](https://github.com/exsinger-hub/You-Only-Figure-Once)科研绘图插件：从手稿提炼核心内容，先用ImageGen确定视觉稿，再忠实复刻为可编辑PPT，并结合项目真实图片与数据完成作图。

## SBF-Mamba作图示例

### Fig.1 · 方法总览

多尺度编码、序列化、空间对齐融合与辅助频谱训练，结合真实医学图像展示。

![SBF-Mamba Fig.1 方法总览](assets/examples/sbf-mamba-fig1.png)

### Fig.2 · 核心机制

有限网格序列化与坐标对齐的双向建模。

![SBF-Mamba Fig.2 核心机制](assets/examples/sbf-mamba-fig2.png)

## 工作流

1. **提炼内容与风格**：阅读手稿、项目代码和知识库，编写逐区域的详细prompt。
2. **生成并确认**：通过ImageGen生成视觉稿，确认构图、密度与科学表达。
3. **忠实复刻**：按认可版式重建原生PPT，文字、图形、网格和连线保持可编辑。
4. **真实素材替换**：使用对应图像和计算数据替换合适字段，检查后导出。

**每张图的完整prompt不得短于对应模板**，且必须写清对象、布局、连线、标签和素材要求。已认可的版式只做授权范围内的局部修改。

[详细工作流](skills/design-scientific-figure/references/imagegen-first-workflow.md) · [Prompt规则](skills/design-scientific-figure/references/imagegen-prompt-detail.md)

## 安装

需要Codex、Node.js及所选的PowerPoint、WPS或draw.io；ImageGen路线需要会话提供图像生成工具，prompt长度检查需要Python 3。

```bash
codex plugin marketplace add exsinger-hub/You-Only-Figure-Once --ref main
codex plugin add you-only-figure-once@you-only-figure-once
```

## 使用

向Codex说明：

```text
使用Sivia，根据手稿和参考模板绘制科研overview。
先写不短于模板的精细prompt，再调用ImageGen。
我确认视觉稿后，忠实复刻为可编辑PPT，
并使用项目真实图片和数据替换合适的示例字段。
保持已认可的布局，不擅自重设计。
```

---

感谢使用 [Sivia](https://github.com/exsinger-hub/You-Only-Figure-Once) 插件，制作者：gatina。
