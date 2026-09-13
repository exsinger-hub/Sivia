# d4rt — 条件匹配试配对

状态：**实际生成，待审阅；未入库、未推送**。

来源：[Efficiently Reconstructing Dynamic Scenes One D4RT at a Time](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_Efficiently_Reconstructing_Dynamic_Scenes_One_D4RT_at_a_Time_CVPR_2026_paper.html)，CVPR 2026。匹配参考：neuralangelo。

![生成草图](figure.png)

[完整实际提交 prompt](prompt.txt) · [版本与校验记录](case.json)

Prompt：29,741 字符；24,979 非空白字符；参考下限 20,509；工具上限 32,000 字符。

源图检查：assistant inspected original PDF p2 Figure 2 at rendered resolution

检查内容：

- Independent query calls remain separate and reuse F.
- Five embedding summands; source patch is not a sixth summand.
- Both coordinate clouds feed Umeyama, whose output is relative camera pose.

仍需审阅：

- Small labels require full-size viewing; schematic geometry is not a measured output.

图片和分子/几何示例是生成的概念插图，不是实验结果，也不是人类金标准。
