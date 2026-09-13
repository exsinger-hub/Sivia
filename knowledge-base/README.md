# 科研绘图知识库 · 条件匹配重启版

本地审阅版，尚未推送。当前有效参考池是用户认可的 **Neuralangelo、ReAct、DiffDock 3 对**；其余 **39 对**保留为历史排除项。原先“42 对全部通过”的结论只代表旧数值筛查，不能代表用户认可或科学质量。

[打开图文审阅页](restart-2026/gallery.html) · [机器索引](index.json) · [SQLite 条件匹配数据库](restart-2026/conditional.sqlite) · [24 篇候选](restart-2026/candidates.json) · [历史排除项](archive/excluded-39.json)

本轮已完成 3 个实际生成试配对；其余 21 篇尚未生成。新入库为 0，全部等待审阅。

## 条件匹配

[按新需求的条件直接查询：命令、词表与增广流程](restart-2026/retrieval-guide.md)

按领域、科学对象、机制拓扑、构图形式四个维度匹配，仅检索用户认可的历史参考。默认权重 0.30 / 0.30 / 0.25 / 0.15；匹配值低于 0.5 时不自动选择参考。该值是可解释的检索启发式，不是视觉质量分数。

```bash
python scripts/restart_conditional_kb.py --query d4rt
python scripts/validate_knowledge_base.py
```

每条记录保留借鉴内容、禁止迁移的科学内容和弱匹配提示。现有三个参考覆盖有限；弱匹配的生成、机器人等候选仍需新论文图形支持，不能强行套版。

## 三个试配对

| 新论文 | 匹配参考 | 完整 prompt | 状态 |
| --- | --- | --- | --- |
| [d4rt](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_Efficiently_Reconstructing_Dynamic_Scenes_One_D4RT_at_a_Time_CVPR_2026_paper.html) · CVPR 2026 | neuralangelo | [全文](restart-2026/pairs/d4rt/prompt.txt) · 24,979 非空白字符 | 实际草图，未入库 |
| [autotool](https://ojs.aaai.org/index.php/AAAI/article/view/40389) · AAAI 2026 | react | [全文](restart-2026/pairs/autotool/prompt.txt) · 24,434 非空白字符 | 实际草图，未入库 |
| [sigmadock](https://proceedings.iclr.cc/paper_files/paper/2026/hash/4c1516dc8f1643c94d164a436ce8fe51-Abstract-Conference.html) · ICLR 2026 | diffdock | [全文](restart-2026/pairs/sigmadock/prompt.txt) · 25,096 非空白字符 | 实际草图，未入库 |

## 六大类候选

近期范围按会议论文集版本为 **2025-09-13—2026-09-13**。原始预印本首次公开日期尚未逐篇核对；历史参考不计入近期新增。下面是候选，不是已评定的优秀源图名单。

### 三维重建与动态几何

- [Efficiently Reconstructing Dynamic Scenes One D4RT at a Time](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_Efficiently_Reconstructing_Dynamic_Scenes_One_D4RT_at_a_Time_CVPR_2026_paper.html) — CVPR 2026；已生成试配对。
- [FUSER: Feed-Forward Multiview 3D Registration Transformer and SE(3)$^N$ Diffusion Refinement](https://openaccess.thecvf.com/content/CVPR2026/html/Jiang_FUSER_Feed-Forward_Multiview_3D_Registration_Transformer_and_SE3N_Diffusion_Refinement_CVPR_2026_paper.html) — CVPR 2026；待源图审阅与生成。
- [4D Primitive-Mache: Glueing Primitives for Persistent 4D Scene Reconstruction](https://openaccess.thecvf.com/content/CVPR2026/html/Mazur_4D_Primitive-Mache_Glueing_Primitives_for_Persistent_4D_Scene_Reconstruction_CVPR_2026_paper.html) — CVPR 2026；待源图审阅与生成。
- [Residual Primitive Fitting of 3D Shapes with SuperFrusta](https://openaccess.thecvf.com/content/CVPR2026/html/Ganeshan_Residual_Primitive_Fitting_of_3D_Shapes_with_SuperFrusta_CVPR_2026_paper.html) — CVPR 2026；待源图审阅与生成。

### 智能体、工具与检索

- [AutoTool: Efficient Tool Selection for Large Language Model Agents](https://ojs.aaai.org/index.php/AAAI/article/view/40389) — AAAI 2026；已生成试配对。
- [Mobile-Agent-RAG: Driving Smart Multi-Agent Coordination with Contextual Knowledge Empowerment for Long-Horizon Mobile Automation](https://ojs.aaai.org/index.php/AAAI/article/view/40241) — AAAI 2026；待源图审阅与生成。
- [AI-Researcher: Autonomous Scientific Innovation](https://proceedings.neurips.cc/paper_files/paper/2025/hash/0d904d300a105809a2114d727851e759-Abstract-Conference.html) — NeurIPS 2025；待源图审阅与生成。
- [AI Research Agents for Machine Learning: Search, Exploration, and Generalization in MLE-bench](https://proceedings.neurips.cc/paper_files/paper/2025/hash/328b81881da145412f2bc56c998dfb6a-Abstract-Conference.html) — NeurIPS 2025；待源图审阅与生成。

### 分子建模与 AI for Science

- [SigmaDock: Untwisting Molecular Docking with Fragment-Based SE(3) Diffusion](https://proceedings.iclr.cc/paper_files/paper/2026/hash/4c1516dc8f1643c94d164a436ce8fe51-Abstract-Conference.html) — ICLR 2026；已生成试配对。
- [Scalable Spatio-Temporal SE(3) Diffusion for Long-Horizon Protein Dynamics](https://proceedings.iclr.cc/paper_files/paper/2026/hash/f1f2ecd9db4c1faaa2ba9c716dc3e413-Abstract-Conference.html) — ICLR 2026；待源图审阅与生成。
- [Graph Diffusion Transformers are In-Context Molecular Designers](https://proceedings.iclr.cc/paper_files/paper/2026/hash/a6b41bed7b8c1abfcf34591d7ae13424-Abstract-Conference.html) — ICLR 2026；待源图审阅与生成。
- [DynaPhArM: Adaptive and Physics-Constrained Modeling for Target-Drug Complexes with Drug-Specific Adaptations](https://proceedings.neurips.cc/paper_files/paper/2025/hash/027af285dc29d3388002c2d223ab1772-Abstract-Conference.html) — NeurIPS 2025；待源图审阅与生成。

### 图像、视频生成与编辑

- [ThinkGen: Generalized Thinking for Visual Generation](https://openaccess.thecvf.com/content/CVPR2026/html/Jiao_ThinkGen_Generalized_Thinking_for_Visual_Generation_CVPR_2026_paper.html) — CVPR 2026；待源图审阅与生成。
- [Learning to Generate Highly Dynamic Videos using Synthetic Motion Data](https://openaccess.thecvf.com/content/CVPR2026/html/Jin_Learning_to_Generate_Highly_Dynamic_Videos_using_Synthetic_Motion_Data_CVPR_2026_paper.html) — CVPR 2026；待源图审阅与生成。
- [SeeU: Seeing the Unseen World via 4D Dynamics-aware Generation](https://openaccess.thecvf.com/content/CVPR2026/html/Yuan_SeeU_Seeing_the_Unseen_World_via_4D_Dynamics-aware_Generation_CVPR_2026_paper.html) — CVPR 2026；待源图审阅与生成。
- [AR-RAG: Autoregressive Retrieval Augmentation for Image Generation](https://proceedings.neurips.cc/paper_files/paper/2025/hash/294fe7aabe8f67e8aca8c0eab2bcfbc4-Abstract-Conference.html) — NeurIPS 2025；待源图审阅与生成。

### 具身控制与世界模型

- [Cosmos Policy: Fine-Tuning Video Models for Visuomotor Control and Planning](https://proceedings.iclr.cc/paper_files/paper/2026/hash/748becc400a57c0e31cfe6a2e7951467-Abstract-Conference.html) — ICLR 2026；待源图审阅与生成。
- [WorldGym: World Model as An Environment for Policy Evaluation](https://proceedings.iclr.cc/paper_files/paper/2026/hash/7f5e909ac0324db03506b380c695ffaf-Abstract-Conference.html) — ICLR 2026；待源图审阅与生成。
- [Scaling up Memory for Robotic Control via Experience Retrieval](https://proceedings.iclr.cc/paper_files/paper/2026/hash/9da515b1ad19d032a7398f00f5ff9b0c-Abstract-Conference.html) — ICLR 2026；待源图审阅与生成。
- [Policy Contrastive Decoding for Robotic Foundation Models](https://proceedings.iclr.cc/paper_files/paper/2026/hash/b6d67c380f8bde2adc4247d0036c0c73-Abstract-Conference.html) — ICLR 2026；待源图审阅与生成。

### 视觉理解、分割与空间定位

- [SegGraph: Leveraging Graphs of SAM Segments for Few-Shot 3D Part Segmentation](https://proceedings.neurips.cc/paper_files/paper/2025/hash/13388efc819c09564c66ab2dc8463809-Abstract-Conference.html) — NeurIPS 2025；待源图审阅与生成。
- [RoboRefer: Towards Spatial Referring with Reasoning in Vision-Language Models for Robotics](https://proceedings.neurips.cc/paper_files/paper/2025/hash/29416b66c2149872b9d1415a3fd2c5e0-Abstract-Conference.html) — NeurIPS 2025；待源图审阅与生成。
- [MS-Temba: Multi-Scale Temporal Mamba for Understanding Long Untrimmed Videos](https://openaccess.thecvf.com/content/CVPR2026/html/Sinha_MS-Temba_Multi-Scale_Temporal_Mamba_for_Understanding_Long_Untrimmed_Videos_CVPR_2026_paper.html) — CVPR 2026；待源图审阅与生成。
- [Guardians of the Hair: Rescuing Soft Boundaries in Depth, Stereo, and Novel Views](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_Guardians_of_the_Hair_Rescuing_Soft_Boundaries_in_Depth_Stereo_CVPR_2026_paper.html) — CVPR 2026；待源图审阅与生成。

## 入库与长度要求

- 科学对象、细节和必要连线应充分占据画面；浅色底板、空框、边框和大标题不能代替有效内容。
- 长度下限为匹配参考完整 prompt 的非空白 Unicode 字符数，接口上限为 32,000 总字符；提交前两项都检查，实际提交全文必须与保存文件一致。
- 自动对比度网格只辅助找空白，不能判定科学正确性、图形美学或用户认可。
- 标签、端点、对象身份及训练/推理范围需单独核对。所有草图保留修订历史和剩余问题。
- 用户确认后才允许新条目入库和推送；当前 publication_allowed=false。不启动模型实验。

源论文 PDF/网页的本地检查缓存不纳入发布包；保留官方链接和已取得的校验散列。所有已接触源论文家族和衍生物均排除未来封闭评测。生成概念图不能作为实测结果或人类金标准。
