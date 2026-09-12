# ReAct: Synergizing Reasoning and Acting in Language Models

![实际生成图](figure.png)

- **大类**：智能体、工具使用与推理 (`agents-reasoning`)
- **来源**：[ICLR 2023](https://openreview.net/pdf?id=WE_vluYUL-X)
- **参考切入点**：Figure 1 interleaved thought-action-observation trajectories
- **核心图意**：Interleaving reasoning traces with environment actions lets observations update the plan and reduces hallucination compared with reasoning-only or action-only trajectories.
- **完整生产 prompt**：[prompt.txt](prompt.txt)（20,426 个非空白字符）
- **低空白筛查**：通过；内容网格占用 93.4%，最大连续空区 2.0%
- **人工目视检查**：通过

这是依据论文机制重新组织的 ImageGen 概念示意，不是论文原图、实验结果或人工 gold。生成时未输入原论文图像像素。使用时应借鉴信息组织、对象密度、分区和连线方式，并依据目标论文重新核验科学关系。
