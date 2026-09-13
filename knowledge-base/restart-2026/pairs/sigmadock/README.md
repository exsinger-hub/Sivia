# sigmadock — 条件匹配试配对

状态：**实际生成，待审阅；未入库、未推送**。

来源：[SigmaDock: Untwisting Molecular Docking with Fragment-Based SE(3) Diffusion](https://proceedings.iclr.cc/paper_files/paper/2026/hash/4c1516dc8f1643c94d164a436ce8fe51-Abstract-Conference.html)，ICLR 2026。匹配参考：diffdock。

![生成草图](figure.png)

[完整实际提交 prompt](prompt.txt) · [版本与校验记录](case.json)

Prompt：29,697 字符；25,096 非空白字符；参考下限 23,963；工具上限 32,000 字符。

源图检查：assistant inspected original PDF p3 Figure 1 and p6 Figure 3; read sections 2.2.3–2.4 and appendix FR3D algorithm

检查内容：

- Protein pocket remains fixed; reverse direction is T to 0.
- Local geometry uses A–C and B–D distance associations with a B–C dihedral axis.
- Fragment score and reverse-step roles remain distinct; current-state dependence is labeled.

仍需审阅：

- Small angle-label artifacts remain in the lower construction; publication typography needs another precision pass.
- Generic molecular graphics were not validated as a chemical structure.

图片和分子/几何示例是生成的概念插图，不是实验结果，也不是人类金标准。
