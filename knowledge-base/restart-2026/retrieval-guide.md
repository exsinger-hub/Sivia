# 从已有知识库做条件匹配

数据库只检索用户认可的 Neuralangelo、ReAct、DiffDock。24 篇近期论文是候选记录，3 张新图是审阅草稿；两者都不能反过来充当已认可参考。

## 新绘图需求查询

在仓库根目录运行：

```bash
python scripts/restart_conditional_kb.py --category agents-retrieval --objects tool,graph,text --topology feedback,conditional_branch --composition flow_loop,local_detail
```

该例返回 ReAct 及其原始图、完整 prompt 路径，逐项说明命中标签、可以借鉴的视觉形式和禁止迁移的科学内容。查询只读，不创建候选、生成图片或改变入库状态。

已有论文候选可以直接查询：

```bash
python scripts/restart_conditional_kb.py --query d4rt
```

不带参数用于重建派生索引和 SQLite 数据库，不能当只读查询使用。

## 条件词表

类别见 [taxonomy.json](taxonomy.json)。对象、拓扑、构图标签来自人工阅读后的标注；新需求可使用以下词表，同义词应先归一化。

| 条件 | 当前参考中的标签 |
| --- | --- |
| 领域 | `geometry-4d`、`agents-retrieval`、`molecular-science` |
| 科学对象 | `image`、`video`、`camera`、`point_cloud`、`surface`、`coordinate_frame`；`tool`、`ui`、`text`、`graph`、`document`、`robot`；`molecule`、`protein` |
| 机制拓扑 | `encode_decode`、`correspondence`、`geometric_transform`、`iteration`；`feedback`、`conditional_branch`、`retrieval`、`search`、`hierarchy`；`diffusion`、`conditioning`、`sampling` |
| 构图形式 | `dense_3d`、`object_sequence`、`local_detail`、`concrete_scenario`、`flow_loop` |

四轴权重依次为 0.30、0.30、0.25、0.15。领域采用完全相等判断；其余各轴为“命中参考的查询标签数 ÷ 查询标签数”。未提供的轴贡献 0，不重新分配权重。最高值低于 0.5 返回 `no_eligible_match`；同分按参考 id 排序。这些参数尚未经过实证调优。

匹配值 1.0 只表示给定的人工标签全部被覆盖，不表示参考与新论文相同，也不表示图片质量满分。标签查询不验证论文的新近性、主会身份或科学主张；这些仍由来源审阅完成。

## 如何增广

1. 从新论文的方法与源图提炼图意，核验会议版本、输入输出、必需关系和公式。
2. 输入对象、拓扑与构图条件，读取命中参考的完整 prompt 和图片。
3. 迁移构图比例、科学实体表现方式和局部展开方法。新论文的机制、标签和参数必须重写并绑定来源。
4. 保存实际提交的完整 prompt，检查参考长度下限和工具 32,000 字符上限，再执行真实图片生成。
5. 检查无效空白、科学连线、局部几何和字号。浅色底板不能充当内容；大面积留白必须有明确阅读功能。
6. 把新配对放入审阅区，保留修订与失败记录。只有达到质量要求且获得用户认可的条目才能进入活动参考池。

弱匹配时采用新论文支持的构图，并补充候选参考；不能为了凑满类别把不适合的历史模板硬套上去。任何已查看的论文家族和衍生图都继续排除未来封闭评测。
