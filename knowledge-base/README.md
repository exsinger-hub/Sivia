# Sivia 科研绘图知识库

**一个案例 = 实际生成图片 + 生成它时使用的完整 prompt。** 不是一张孤立图片，也不是只有提示词的长截图。欢迎[贡献图文配对案例](CONTRIBUTING.md)，一起积累可复用的科研绘图经验。

## 首批 6 组生成案例

将 gatina 提供的提示词收藏整理为 6 个主题：转写并校对完整提示词，再逐例调用 ImageGen。下面链接分别提供独立成图、可复制的生成全文和案例说明。

| 案例 | 可借鉴的表达 | 实际成图 | 完整 prompt |
| --- | --- | --- | --- |
| [EventBridge-RL](cases/eventbridge-rl/README.md) | 数学机制、双时间尺度、分支场景叙事 | [PNG](cases/eventbridge-rl/figure.png) | [TXT](cases/eventbridge-rl/prompt.txt) |
| [Reasoning Between Words](cases/reasoning-between-words/README.md) | LLM 潜在推理与符号锚点、非等宽分区、局部反馈 | [PNG](cases/reasoning-between-words/figure.png) | [TXT](cases/reasoning-between-words/prompt.txt) |
| [TRACE](cases/trace/README.md) | 多模态证据、中心机制放大、选择性获取与验证 | [PNG](cases/trace/figure.png) | [TXT](cases/trace/prompt.txt) |
| [两阶段 Trust / Repair](cases/two-phase-trust-repair/README.md) | 紧凑双阶段、跨区知识模块、橙绿双流向 | [PNG](cases/two-phase-trust-repair/figure.png) | [TXT](cases/two-phase-trust-repair/prompt.txt) |
| [Agent Fleet](cases/agent-fleet/README.md) | 多智能体、共享产物、技术漫画与清晰正文搭配 | [PNG](cases/agent-fleet/figure.png) | [TXT](cases/agent-fleet/prompt.txt) |
| [Memory Routing](cases/visio-memory-routing/README.md) | 神经网络框架、视频场景、主干流程与机制放大 | [PNG](cases/visio-memory-routing/figure.png) | [TXT](cases/visio-memory-routing/prompt.txt) |

两阶段案例还使用了随案例提供的[参考图](cases/two-phase-trust-repair/reference.png)。其余案例按文本生成。生成结果存在随机性；相同 prompt 不保证像素级复现。

## 如何用于下一篇论文

1. **先理解论文**：确定研究问题、真实贡献、方法依赖与证据，再选相近案例。
2. **图文一起读**：看成图的布局、密度、对象和连线，再读完整 prompt 如何把这些关系写出来。不要照搬案例中的模型、公式或示例数值。
3. **精细改写**：将论文本身的内容填入具体视觉场景，保存完整生产 prompt；使用[长度规则](../skills/design-scientific-figure/references/imagegen-prompt-detail.md)，不得短于选定模板，不能用摘要或一句话替代。
4. **生成与确认**：调用 ImageGen，听取用户反馈。用户认可后保留该版式，再进入后台 PPT / WPS 忠实复刻与真实素材替换。
5. **积累新案例**：保存最终认可版 prompt、对应图片、使用的参考输入与有价值的修改理由。先本地留存；公开投稿另行取得授权。

默认完整模板见[模板目录](../skills/design-scientific-figure/references/prompt-templates.md)。若用户指定这里某个案例为模板，以它的完整 `prompt.txt` 为基准。参考案例中的指令仅是案例资料，不会覆盖当前用户要求。

## 共建知识库

**欢迎上传你的科研图和对应完整 prompt 到 GitHub！** 尤其欢迎“论文想表达什么 → prompt → 成图 → 用户反馈 → 最终认可版”的配套记录，以及值得解释的失败与改进对比。

[提交案例 Issue](https://github.com/exsinger-hub/Sivia/issues/new?template=knowledge-base.md) · [通过 Pull Request 投稿](CONTRIBUTING.md)

仅有图片或仅有 prompt 的投稿先归为待补全参考；补齐配对后再收为完整案例。不要把尚未认可的生成稿标成“用户最终认可”。

## 使用边界与许可

首批 6 组是 **ImageGen 生成示例，尚未获得用户最终视觉确认**，不是经验证的论文实验或可以不经核对直接投稿的科研图。图中的场景、概率、曲线及比较仅用于学习表达；生成标签、数学符号和箭头还需逐项对照真实论文。

本批案例基于 gatina 提供的提示词收藏，经授权整理与发布；单项原作者、出处链接及原素材许可尚未完整提供，欢迎补充或提出更正。来源提示词与参考素材的权利归各自权利人，代码的 MIT 许可不自动变更第三方素材许可。使用案例提示词或图像时请核对来源与适用许可。投稿只提交有权公开的材料，移除个人隐私、患者信息和未经授权的未公开内容。
