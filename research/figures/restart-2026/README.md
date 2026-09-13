# 2026-09-13 条件匹配重启记录

用户要求：最近一年顶会主会论文；保留 Neuralangelo、ReAct、DiffDock 为已认可历史参照，重做其他增广；只接纳低无效空白的图；完整 prompt、丰富内容、分类整理；确认后再推送。随后明确可以从现有知识库进行条件匹配增广。

当前是首个本地审阅里程碑：3 个已认可参考、39 个历史排除项、6 大类 24 篇候选、3 个实际生成试配对，0 个新入库。**24 对完整新数据尚未完成**。其余 21 篇候选还需要方法/源图审阅、完整 prompt 和实际生成。

## 已执行

- 读取官方来源；本地取得 22 份论文 PDF，另外 2 篇 AAAI 通过 web 工具读取正文。AAAI 原始 PDF 的本地下载及浏览器打开失败，不能称为已完成原图目视检查。
- 原论文渲染检查：D4RT PDF p2 Fig.2；SigmaDock PDF p3 Fig.1、p6 Fig.3；三篇方法与关键公式逐项检查。
- 编写可重建的 SQLite 条件匹配库；按领域、对象、拓扑、构图四轴检索。支持已有候选 id 和新需求的条件查询；低于阈值返回未匹配，缺省轴不重新分配权重。旧参考的类别已映射到新六类体系，DiffDock 归入分子建模。
- 实际执行 13 次成功图片生成/修订，保留 3 对当前草图；另有 2 次失败调用。一次 HTTP 400 明确返回 32,000 字符上限，失败调用不计作生成图片。模型名称、随机种子、费用未由工具提供。
- 完整 prompt 的非空白字符数达到对应已认可案例全文下限，总字符数不超过工具上限。最终工具实参已逐字与保存文件比较，3/3 相同。
- 独立保留源忠实度、低无效空白、标签与端点检查、用户认可状态。所有新图均未入库。
- 更新中英文根 README、知识库 README、活动索引、候选分类、历史排除清单和封闭评测排除清单。
- 根据后续反馈，将三个 README 改为按类别逐条配图；活动参考和已生成草图各选当前版本一张，共 6 张，并标注认可状态、原图、完整 prompt 和详情入口。展示清单保存为 `knowledge-base/restart-2026/readme-showcase.json`；未生成候选不使用占位图。

## 质量口径修正

旧报告把浅色底板当作内容占用，且把数值筛查通过写成了入库认可。本轮撤销这种解释。对比度网格可帮助定位空白，但边框、文字和纹理也会贡献边缘，不能自动证明科学密度。原始白像素比例也不能区分白色背景与无效空白。必须检查真实科学对象、局部细节、可追踪关系和标签。

三张新图均为生成概念插图。D4RT 的查询与 F 路径、AutoTool 的执行分支和决策输入连线、SigmaDock 的距离约束端点经历实际修订。AutoTool 的原图视觉检查尚未完成：web 能读官方 PDF 正文，但 screenshot 只返回引用文本，没有可见图片；当前历史维护线还有一个多余箭头，方向仍需精修。SigmaDock 的局部角标仍有轻微多余笔画，分子图形未经过化学合法性验证。完整出版级认可仍待审阅。

## 可复查产物

- [知识库审阅页](../../../knowledge-base/restart-2026/gallery.html)
- [数据索引](../../../knowledge-base/index.json)
- [完整配对与版本记录](../../../knowledge-base/restart-2026/pairs.json)
- [条件计划与分类](conditional_plan.json)
- [按新需求查询的使用说明](../../../knowledge-base/restart-2026/retrieval-guide.md)
- [官方论文候选与抓取证据](candidates.json)
- [本地 PDF 校验记录](pdf-inspection.json)

原始 PDF、网页和用于查看的渲染缓存通过 .gitignore 排除，不随发布包重新分发。只保存来源链接、已取得的散列和审阅记录。源论文家族及全部历史衍生图即使被拒绝，仍属于已暴露材料，排除未来封闭评测。

## 验证与下一步

```bash
python scripts/restart_conditional_kb.py
python research/figures/restart-2026/package_review.py
python scripts/validate_knowledge_base.py
python research/figures/restart-2026/validate_review.py
```

只更新 README 的逐条图片展示，无需重新生成或重算图片诊断：

```bash
python research/figures/restart-2026/package_review.py --readmes-only
```

构建审阅包依赖 numpy、Pillow、BeautifulSoup；索引构建和数据校验使用 Python 标准库。验证报告区分结构正确与视觉认可。自动浏览器打开 file:// 审阅页被 URL 安全策略阻止；未使用代理服务器或替代浏览器绕过，未声称浏览器渲染测试通过。

[验证摘要](validation-summary.json)：179 项结构与来源校验、11 项检索检查、7 项 prompt 长度测试、40 项仓库测试通过。32 个 PNG / prompt 文件与 Git 暂存对象逐字节相等，避免 Windows 换行转换影响实际提交文本。这些检查不能替代视觉或科学内容认可。

`prepare_*`、`repair_*`、`last_local_repairs.py` 和 `fit_production_prompts.py` 是已执行修订的作者工作记录，不属于重建命令；再次运行可能产生新的未提交 prompt。实际各版本对应文本由每个配对的 `case.json` 精确绑定。

下一步是审阅这三个条件匹配方向，修正剩余源图/角标问题，继续完成其余 21 个配对，筛除不符合科学与低空白标准的条目。用户确认最终包后才允许推送。当前没有运行付费模型实验，也没有更新正式实验快照或论文附录。
