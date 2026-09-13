# autotool — 条件匹配试配对

状态：**实际生成，待审阅；未入库、未推送**。

来源：[AutoTool: Efficient Tool Selection for Large Language Model Agents](https://ojs.aaai.org/index.php/AAAI/article/view/40389)，AAAI 2026。匹配参考：react。

![生成草图](figure.png)

[完整实际提交 prompt](prompt.txt) · [版本与校验记录](case.json)

Prompt：28,941 字符；24,434 非空白字符；参考下限 20,426；工具上限 32,000 字符。

源图检查：Official PDF method text and Figure 2 caption inspected via web; original figure raster inspection remains pending because local PDF download failed and the web screenshot tool returned a citation without a model-visible image.

检查内容：

- Both-checks-pass and any-check-fails routes converge before shared execution.
- LLM output and argument completeness no longer bypass execution to reach observation.
- Parameter source value a is preserved through the example.
- Candidate and argument information now reaches the enclosing decision region through a continuous gutter connector.

仍需审阅：

- The history-to-graph maintenance line is continuous, but an extra arrowhead near Add to history makes its direction ambiguous and still needs correction.
- Original source figure visual assessment is still pending.

图片和分子/几何示例是生成的概念插图，不是实验结果，也不是人类金标准。
