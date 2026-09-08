# Sivia

[**Sivia**](https://github.com/exsinger-hub/Sivia) 是面向 Codex 和 Claude Code 的科研绘图插件。输入 PDF 论文，先理解研究内容、参考知识库编写精细 prompt，再生成科研 Overview 图片供你审阅。**默认先交图片，不直接制作 PPT；是否修改图片、是否继续生成可编辑 PPT，由你决定。**

## 安装


### Claude Code

在 Claude Code 对话内依次执行：

```text
/plugin marketplace add exsinger-hub/Sivia
/plugin install sivia@sivia
```

安装后重新开启会话。上传 PDF，或提供 Claude Code 可访问的本地文件路径，按下文说明开始。也可用 `/sivia:design-scientific-figure` 显式调用绘图设计 skill。安装方式对应 [Claude Code 官方插件说明](https://code.claude.com/docs/en/plugin-marketplaces)。

### Codex

在终端依次执行：

```bash
codex plugin marketplace add exsinger-hub/Sivia --ref main
codex plugin add sivia@sivia
```

第一条注册仓库中的插件市场，第二条安装 Sivia。安装后新开任务使用。市场注册方式见 [OpenAI 官方插件说明](https://developers.openai.com/plugins/build/plugins)；安装命令可用本机 `codex plugin add --help` 核对。若之前安装了旧名插件，请在插件管理中停用旧版，避免同一组 skills 重复加载。

### 运行条件

- **理解论文与编写 prompt**：客户端能够读取 PDF；Python 3 用于检查 prompt 长度。
- **生成图片**：当前会话需要可调用的 ImageGen / 图像生成工具。Sivia 提供工作流、模板和知识库，不内置生图模型或 API 凭据；Claude Code 需另行连接图像生成工具或 MCP 服务。
- **制作可编辑 PPT（可选）**：Node.js，以及可用的 PowerPoint / WPS 后端；具体能力由插件检测。只做图片阶段不需要打开这些软件。

没有可用生图工具时，Sivia 会交付完整 prompt 并说明缺少的能力。你也可以将 prompt 用于 ImageGen，再把成图传回继续审阅；它不会擅自跳过图片确认，直接改用 PPT 绘制。

## 使用

### 1. 提供论文，先生成图片

必需材料是 **PDF 论文或完整手稿**。可选材料包括：偏好的参考图、知识库案例、项目代码和真实图片/数据、目标版面尺寸。没有指定模板时，由 Sivia 理解论文后选择合适的内置模板，不要求你自己写生产 prompt。

上传 PDF 后，可以直接这样说：

```text
使用 Sivia，为附件中的 PDF 论文绘制一张科研 Overview。

先读懂研究问题、现有方法的局限、核心创新，以及方法的输入、关键过程和输出。
突出这篇论文自己的科学逻辑，不要把模板中的模型、公式或实验数值照搬过来。

参考 Sivia 知识库中的图片与配套 prompt，选择适合本文的表达风格。
先写出完整、逐区域细化且不短于所选模板的生成 prompt，再调用 ImageGen。
图中采用简洁准确的英文标签，布局紧凑，突出核心机制；不要加入内部说明或待完成事项。

这一轮只需要 Overview 图片、完整 prompt，以及简短的设计说明。
生成后先给我查看，问我哪里需要调整、是否继续制作可编辑 PPT，然后停下来等我回复。
不要直接打开 PowerPoint/WPS，也不要自动生成 PPT。
```

这段是**用户需求示例**，不是直接发给 ImageGen 的完整 prompt。真正的生成 prompt 由 Sivia 根据论文和模板展开、保存，并检查长度。希望先审核文字时，额外说“先只给我完整 prompt，等我确认再生成图片”。

第一轮交付：生成图片、对应完整 prompt、简短的内容与布局说明。缺少项目真实素材不妨碍先讨论构图，但生成的示例不能冒充实验结果。

### 2. 看图后决定是否修改

可以按具体区域提出修改，例如：

```text
保留这张图的整体布局、配色和模块位置。
只放大中间的核心机制，减少右侧说明文字，并修正我标出的箭头。
先修改 prompt，再生成修改后的图片供我确认。这一轮仍然不做 PPT。
```

每次修改都保留对应的完整 prompt 和成图。已认可的部分不擅自重设计。回复“这张图可以”表示认可该图片，**不等于授权制作 PPT**；你也可以只保留图片，到此结束。

### 3. 确认图片后，按需制作 PPT

需要可编辑版本时，再明确下达：

```text
这张图片的视觉稿已确认，现在继续制作可编辑 PPT。
在后台忠实复刻这张图，不抢占焦点，不把 PowerPoint/WPS 切到前台。
保持画布比例、分区、配色、对象大小和连线路径，不重新设计。
文字、框、箭头、网格、token 和可重建图表使用原生可编辑对象，
不要把整张图片直接贴进 PPT 作为交付。

检查我提供的项目文件夹，选取同一样本、对应模型阶段的真实图片和计算数据，
替换合适的示例字段；保留用于解释顺序、坐标和机制的必要示意图。
没有真实来源的字段先告诉我，不要生成虚假的实验结果。
完成后提供 PPTX、预览图，以及素材替换说明。
```

后台复刻必须使用不抢焦点的可用后端；若当前后端做不到，先说明并等待选择，不自动切到前台。完成后检查可编辑对象和导出预览，再交付文件。

## 工作流

论文理解 → 图文知识库与模板参考 → 完整精细 prompt → ImageGen 图片 → **暂停，等待你的反馈**。

需要改图，就在原布局内修订 prompt、重新生成并再次确认；你明确要求 PPT 后，才进入 **后台忠实复刻 → 真实素材替换 → 检查与交付**。

用户最终认可的完整 prompt、对应图片与有价值的修改反馈会作为配对案例保存在当前项目中。公开上传 GitHub 另行征求同意。

[内置模板](skills/design-scientific-figure/references/prompt-templates.md) · [详细工作流](skills/design-scientific-figure/references/imagegen-first-workflow.md)

## 共建科研绘图知识库

知识库以 **实际生成图片 + 对应完整 prompt** 为一个案例，首批整理 6 个不同主题，覆盖 LLM 推理、多模态框架、强化学习与多智能体。点击图片下方链接即可取得生成提示词。

### 1. Agent Fleet · 多智能体协作

![Agent Fleet：多智能体协作技术漫画](knowledge-base/cases/agent-fleet/figure.png)

[完整 prompt](knowledge-base/cases/agent-fleet/prompt.txt) · [案例说明](knowledge-base/cases/agent-fleet/README.md)

### 2. Reasoning Between Words · LLM 潜在推理

![Reasoning Between Words：潜在推理与符号锚点](knowledge-base/cases/reasoning-between-words/figure.png)

[完整 prompt](knowledge-base/cases/reasoning-between-words/prompt.txt) · [案例说明](knowledge-base/cases/reasoning-between-words/README.md)

### 3. TRACE · 多模态证据路由

![TRACE：多模态证据路由](knowledge-base/cases/trace/figure.png)

[完整 prompt](knowledge-base/cases/trace/prompt.txt) · [案例说明](knowledge-base/cases/trace/README.md)

### 4. EventBridge-RL · 双时间尺度世界模型

![EventBridge-RL：双时间尺度世界模型](knowledge-base/cases/eventbridge-rl/figure.png)

[完整 prompt](knowledge-base/cases/eventbridge-rl/prompt.txt) · [案例说明](knowledge-base/cases/eventbridge-rl/README.md)

### 5. 两阶段 Trust / Repair · 紧凑多智能体框架

![两阶段 Trust / Repair：紧凑多智能体框架](knowledge-base/cases/two-phase-trust-repair/figure.png)

[完整 prompt](knowledge-base/cases/two-phase-trust-repair/prompt.txt) · [案例说明](knowledge-base/cases/two-phase-trust-repair/README.md)

### 6. Memory Routing · 长视频记忆框架

![Memory Routing：长视频记忆框架](knowledge-base/cases/visio-memory-routing/figure.png)

[完整 prompt](knowledge-base/cases/visio-memory-routing/prompt.txt) · [案例说明](knowledge-base/cases/visio-memory-routing/README.md)

以上为参考提示词的 ImageGen 生成示例；用户认可状态与观察记录见各案例说明。

**欢迎把你的优秀科研图、完整 prompt 和修改经验贡献到 Sivia！** 尤其欢迎“最终认可的 prompt + 对应成图 + 为什么这样改”的配套案例，让后续作图有更多可借鉴的真实经验。

[提交知识库案例](https://github.com/exsinger-hub/Sivia/issues/new?template=knowledge-base.md) · [贡献指南与 PR 方式](knowledge-base/CONTRIBUTING.md)

## 致谢

Sivia 基于 [Scientific Illustrator](https://github.com/icebird1998/scientific-illustrator) 改造与扩展。感谢原作者 **一个地质博士（icebird1998）** 提供的可编辑科研绘图基础、PowerPoint / WPS / draw.io 后端，以及设计、绘制、审阅、修正的协作流程。Sivia 在此基础上扩展了论文理解、模板化 ImageGen 设计和视觉稿忠实复刻工作流。保留原项目的 [MIT 许可证与版权声明](LICENSE)。

---

感谢使用 [Sivia](https://github.com/exsinger-hub/Sivia) 插件，制作者：gatina。
