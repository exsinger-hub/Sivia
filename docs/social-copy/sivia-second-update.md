# Sivia 第二弹更新｜把顶会论文的 Overview 结构，变成可复用科研绘图 Prompt

## 抖音 / 视频号主文案

论文内容很清楚，为什么一到 AI 作图就变成：大面积空白、几个漂浮卡片、箭头没有起点终点？

Sivia 第二弹，专门补上这块。

我们从近期 CVPR、ICLR 等顶会论文中整理了 12 张高质量 Overview 审阅稿，最终精选 7 对正式加入知识库。每一对都不是只放一张图，而是完整绑定：

- 一张对应的科研 Overview 图片
- 一条可直接复用的完整 Prompt
- 官方论文来源
- 方法结构与分类标签
- 图像哈希和 Prompt 长度校验

这次新增三类高频科研场景：

1. **3D 几何与神经渲染**
   VGGT、MegaSaM：多视角几何、动态视频、相机轨迹、深度和三维重建。
2. **世界模型与具身感知**
   ReViWo、RoboSpatial、People–Places–Cameras：视角不变表示、世界模型、2D/3D 空间关系和人物—场景—相机联合重建。
3. **多模态与运动感知学习**
   Motion-Aware Video MLLM、Dense-SfM：RGB 与运动向量融合、视频 token、稠密匹配和几何一致性优化。

Sivia 的目标很简单：让 AI 先把论文的方法关系画明白，再考虑风格；让图片、Prompt 和论文来源始终对应起来。

开源地址：https://github.com/exsinger-hub/Sivia

#科研工具 #开源项目 #AI科研绘图 #科研知识库 #三维重建 #世界模型 #具身智能 #多模态学习 #学术可视化 #ClaudeCode插件

## 小红书标题与正文

### 标题备选

1. 顶会论文 Overview 怎么画？Sivia 把 7 组完整 Prompt 直接整理好了
2. 告别科研图大空白：Sivia 第二弹知识库更新
3. 从论文方法到科研配图，7 组顶会 Overview 进入 Sivia

### 正文

科研图最难的地方，往往不是“画得好看”，而是把输入、表示、变换、输出和监督关系画准确。

Sivia 第二弹更新，精选 7 组近期顶会论文 Overview，全部配套图片、完整 Prompt、来源链接和方法结构说明。

新增内容覆盖：

- 多视角几何、动态 SLAM、神经渲染
- 世界模型、机器人空间理解、人物与场景重建
- 视频运动感知、视觉语言模型、稠密 SfM

每个条目都能直接点开查看对应图片和 Prompt。剩余 5 张审阅稿继续保留在候选区，不混入正式知识库。

知识库入口：
https://github.com/exsinger-hub/Sivia/tree/codex/knowledge-base-restart-2026/knowledge-base

## 公众号 / GitHub Release 长文案

**Sivia 第二弹更新：近期顶会科研 Overview 知识库扩容**

科研绘图中最常见的问题，不是缺少颜色，而是缺少结构：方法模块之间的关系没有被画出来，箭头缺少明确端点，动态过程被压成静态卡片，最终留下大面积空白和泛化式 AI 流程框。

本次更新围绕“论文方法结构可复用”扩容知识库。我们从 12 张近期顶会 Overview 审阅稿中选定 7 对，正式发布三类科研绘图范式：

- **3D 几何与神经渲染**：VGGT、MegaSaM
- **世界模型与具身感知**：ReViWo、RoboSpatial、Reconstructing People, Places, and Cameras
- **多模态与运动感知学习**：Efficient Motion-Aware Video MLLM、Dense-SfM

每组条目包含实际生成图片、完整提交 Prompt、官方论文来源、分类标签、方法结构说明以及文件校验信息。Prompt 对空白比例、虚构指标、无依据模块、卡片化布局和泛化式流程框进行了明确约束。

这些图片是来源于论文方法结构的概念性科研插图，不是实验结果或人类金标准；相关论文家族及其衍生物继续排除在未来封闭评测之外。

开源地址：
https://github.com/exsinger-hub/Sivia

知识库目录：
https://github.com/exsinger-hub/Sivia/tree/codex/knowledge-base-restart-2026/knowledge-base
