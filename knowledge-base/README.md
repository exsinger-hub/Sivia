# Sivia 科研绘图知识库

本知识库现有 **42 对实际生成 PNG + 完整生产 prompt**：6 对早期整理案例、12 对先前论文来源案例，以及本轮新增的 24 对。36 对论文来源案例覆盖 ICLR、CVPR、ICCV、NeurIPS、ICML、AAAI、CoRL 与 RSS 等会议。

## 纳入门槛

所有 42 对均通过同一低空白率数值筛查：32×20 内容网格占用率不低于 78%，且最大连续空区不高于画布的 10%。数值筛查只用于发现空白布局问题；论文来源案例还经过实际 PNG 目视检查。完整指标见 [`audit/`](audit/)，机器可读总索引见 [`index.json`](index.json)。

每个案例必须同时包含 `figure.png` 与生成它的完整 `prompt.txt`。论文来源图是重新设计并生成的概念示意，不是论文原图、实验结果或人工 gold。

## 按大类浏览

<a id="multimodal-foundation"></a>

### 多模态与基础表征

Multimodal and foundation representations。共 7 对。

| 案例 | 来源层级 | 实际成图 | 完整 prompt |
| --- | --- | --- | --- |
| [BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models](cases/blip2/README.md) | 论文来源·新增 24 | [PNG](cases/blip2/figure.png) | [TXT](cases/blip2/prompt.txt) |
| [Flamingo: a Visual Language Model for Few-Shot Learning](cases/flamingo/README.md) | 论文来源·新增 24 | [PNG](cases/flamingo/figure.png) | [TXT](cases/flamingo/prompt.txt) |
| [Image BERT Pre-training with Online Tokenizer](cases/ibot/README.md) | 论文来源·先前批次 | [PNG](cases/ibot/figure.png) | [TXT](cases/ibot/prompt.txt) |
| [InstructBLIP: Towards General-purpose Vision-Language Models with Instruction Tuning](cases/instructblip/README.md) | 论文来源·新增 24 | [PNG](cases/instructblip/figure.png) | [TXT](cases/instructblip/prompt.txt) |
| [Visual Instruction Tuning](cases/llava/README.md) | 论文来源·新增 24 | [PNG](cases/llava/figure.png) | [TXT](cases/llava/prompt.txt) |
| [TRACE](cases/trace/README.md) | 早期整理 | [PNG](cases/trace/figure.png) | [TXT](cases/trace/prompt.txt) |
| [Visio Memory Routing](cases/visio-memory-routing/README.md) | 早期整理 | [PNG](cases/visio-memory-routing/figure.png) | [TXT](cases/visio-memory-routing/prompt.txt) |

<a id="generative-control"></a>

### 生成建模与可控编辑

Generative modeling and control。共 6 对。

| 案例 | 来源层级 | 实际成图 | 完整 prompt |
| --- | --- | --- | --- |
| [Anywhere: A Multi-Agent Framework for User-Guided, Reliable, and Diverse Foreground-Conditioned Image Generation](cases/anywhere/README.md) | 论文来源·先前批次 | [PNG](cases/anywhere/figure.png) | [TXT](cases/anywhere/prompt.txt) |
| [Adding Conditional Control to Text-to-Image Diffusion Models](cases/controlnet/README.md) | 论文来源·新增 24 | [PNG](cases/controlnet/figure.png) | [TXT](cases/controlnet/prompt.txt) |
| [Scalable Diffusion Models with Transformers](cases/dit/README.md) | 论文来源·新增 24 | [PNG](cases/dit/figure.png) | [TXT](cases/dit/prompt.txt) |
| [DreamBooth: Fine Tuning Text-to-Image Diffusion Models for Subject-Driven Generation](cases/dreambooth/README.md) | 论文来源·新增 24 | [PNG](cases/dreambooth/figure.png) | [TXT](cases/dreambooth/prompt.txt) |
| [Leveraging RGB-D Data with Cross-Modal Context Mining for Glass Surface Detection](cases/glass/README.md) | 论文来源·先前批次 | [PNG](cases/glass/figure.png) | [TXT](cases/glass/prompt.txt) |
| [High-Resolution Image Synthesis with Latent Diffusion Models](cases/latent-diffusion/README.md) | 论文来源·新增 24 | [PNG](cases/latent-diffusion/figure.png) | [TXT](cases/latent-diffusion/prompt.txt) |

<a id="detection-segmentation"></a>

### 检测、分割与密集预测

Detection, segmentation and dense prediction。共 7 对。

| 案例 | 来源层级 | 实际成图 | 完整 prompt |
| --- | --- | --- | --- |
| [Putting the Object Back into Video Object Segmentation](cases/cutie/README.md) | 论文来源·先前批次 | [PNG](cases/cutie/figure.png) | [TXT](cases/cutie/prompt.txt) |
| [Divide, Conquer and Combine: A Training-Free Framework for High-Resolution Image Perception in Multimodal Large Language Models](cases/dc2/README.md) | 论文来源·先前批次 | [PNG](cases/dc2/figure.png) | [TXT](cases/dc2/prompt.txt) |
| [Depth Anything: Unleashing the Power of Large-Scale Unlabeled Data](cases/depth-anything/README.md) | 论文来源·先前批次 | [PNG](cases/depth-anything/figure.png) | [TXT](cases/depth-anything/prompt.txt) |
| [Masked-Attention Mask Transformer for Universal Image Segmentation](cases/mask2former/README.md) | 论文来源·新增 24 | [PNG](cases/mask2former/figure.png) | [TXT](cases/mask2former/prompt.txt) |
| [Segment Anything](cases/segment-anything/README.md) | 论文来源·新增 24 | [PNG](cases/segment-anything/figure.png) | [TXT](cases/segment-anything/prompt.txt) |
| [Tube-Link: A Flexible Cross Tube Framework for Universal Video Segmentation](cases/tube-link/README.md) | 论文来源·新增 24 | [PNG](cases/tube-link/figure.png) | [TXT](cases/tube-link/prompt.txt) |
| [VideoGrounding-DINO: Towards Open-Vocabulary Spatio-Temporal Video Grounding](cases/video-grounding-dino/README.md) | 论文来源·新增 24 | [PNG](cases/video-grounding-dino/figure.png) | [TXT](cases/video-grounding-dino/prompt.txt) |

<a id="three-d-reconstruction"></a>

### 三维表示、重建与分子空间

3D representation, reconstruction and molecular space。共 6 对。

| 案例 | 来源层级 | 实际成图 | 完整 prompt |
| --- | --- | --- | --- |
| [3DGStream: On-the-Fly Training of 3D Gaussians for Efficient Streaming of Photo-Realistic Free-Viewpoint Videos](cases/3dgstream/README.md) | 论文来源·新增 24 | [PNG](cases/3dgstream/figure.png) | [TXT](cases/3dgstream/prompt.txt) |
| [DiffDock: Diffusion Steps, Twists, and Turns for Molecular Docking](cases/diffdock/README.md) | 论文来源·先前批次 | [PNG](cases/diffdock/figure.png) | [TXT](cases/diffdock/prompt.txt) |
| [DUSt3R: Geometric 3D Vision Made Easy](cases/dust3r/README.md) | 论文来源·先前批次 | [PNG](cases/dust3r/figure.png) | [TXT](cases/dust3r/prompt.txt) |
| [GaussianDreamer: Fast Generation from Text to 3D Gaussians by Bridging 2D and 3D Diffusion Models](cases/gaussian-dreamer/README.md) | 论文来源·新增 24 | [PNG](cases/gaussian-dreamer/figure.png) | [TXT](cases/gaussian-dreamer/prompt.txt) |
| [Mip-NeRF 360: Unbounded Anti-Aliased Neural Radiance Fields](cases/mipnerf360/README.md) | 论文来源·新增 24 | [PNG](cases/mipnerf360/figure.png) | [TXT](cases/mipnerf360/prompt.txt) |
| [Neuralangelo: High-Fidelity Neural Surface Reconstruction](cases/neuralangelo/README.md) | 论文来源·新增 24 | [PNG](cases/neuralangelo/figure.png) | [TXT](cases/neuralangelo/prompt.txt) |

<a id="agents-reasoning"></a>

### 智能体、工具使用与推理

Agents, tool use and reasoning。共 9 对。

| 案例 | 来源层级 | 实际成图 | 完整 prompt |
| --- | --- | --- | --- |
| [Agent Fleet](cases/agent-fleet/README.md) | 早期整理 | [PNG](cases/agent-fleet/figure.png) | [TXT](cases/agent-fleet/prompt.txt) |
| [ReAct: Synergizing Reasoning and Acting in Language Models](cases/react/README.md) | 论文来源·新增 24 | [PNG](cases/react/figure.png) | [TXT](cases/react/prompt.txt) |
| [Reasoning Between Words](cases/reasoning-between-words/README.md) | 早期整理 | [PNG](cases/reasoning-between-words/figure.png) | [TXT](cases/reasoning-between-words/prompt.txt) |
| [Reflexion: Language Agents with Verbal Reinforcement Learning](cases/reflexion/README.md) | 论文来源·新增 24 | [PNG](cases/reflexion/figure.png) | [TXT](cases/reflexion/prompt.txt) |
| [Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection](cases/self-rag/README.md) | 论文来源·先前批次 | [PNG](cases/self-rag/figure.png) | [TXT](cases/self-rag/prompt.txt) |
| [Toolformer: Language Models Can Teach Themselves to Use Tools](cases/toolformer/README.md) | 论文来源·新增 24 | [PNG](cases/toolformer/figure.png) | [TXT](cases/toolformer/prompt.txt) |
| [Tree of Thoughts: Deliberate Problem Solving with Large Language Models](cases/tree-of-thoughts/README.md) | 论文来源·新增 24 | [PNG](cases/tree-of-thoughts/figure.png) | [TXT](cases/tree-of-thoughts/prompt.txt) |
| [Two-phase Trust / Repair](cases/two-phase-trust-repair/README.md) | 早期整理 | [PNG](cases/two-phase-trust-repair/figure.png) | [TXT](cases/two-phase-trust-repair/prompt.txt) |
| [Visual Programming: Compositional Visual Reasoning Without Training](cases/visprog/README.md) | 论文来源·先前批次 | [PNG](cases/visprog/figure.png) | [TXT](cases/visprog/prompt.txt) |

<a id="structured-robotics"></a>

### 时序、图学习、世界模型与机器人

Time series, graphs, world models and robotics。共 7 对。

| 案例 | 来源层级 | 实际成图 | 完整 prompt |
| --- | --- | --- | --- |
| [Diffusion Policy: Visuomotor Policy Learning via Action Diffusion](cases/diffusion-policy/README.md) | 论文来源·新增 24 | [PNG](cases/diffusion-policy/figure.png) | [TXT](cases/diffusion-policy/prompt.txt) |
| [EventBridge-RL](cases/eventbridge-rl/README.md) | 早期整理 | [PNG](cases/eventbridge-rl/figure.png) | [TXT](cases/eventbridge-rl/prompt.txt) |
| [Recipe for a General, Powerful, Scalable Graph Transformer](cases/graphgps/README.md) | 论文来源·新增 24 | [PNG](cases/graphgps/figure.png) | [TXT](cases/graphgps/prompt.txt) |
| [A Time Series is Worth 64 Words: Long-term Forecasting with Transformers](cases/patchtst/README.md) | 论文来源·新增 24 | [PNG](cases/patchtst/figure.png) | [TXT](cases/patchtst/prompt.txt) |
| [PDFormer: Propagation Delay-Aware Dynamic Long-Range Transformer for Traffic Flow Prediction](cases/pdformer/README.md) | 论文来源·先前批次 | [PNG](cases/pdformer/figure.png) | [TXT](cases/pdformer/prompt.txt) |
| [RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control](cases/rt2/README.md) | 论文来源·新增 24 | [PNG](cases/rt2/figure.png) | [TXT](cases/rt2/prompt.txt) |
| [Learning Interactive Real-World Simulators](cases/unisim/README.md) | 论文来源·先前批次 | [PNG](cases/unisim/figure.png) | [TXT](cases/unisim/prompt.txt) |

## 使用方式

1. 先按任务大类选择结构接近的案例，同时查看 PNG 与完整 prompt。
2. 借鉴版式、信息密度、对象层级、配色和连线约束；不要照搬案例的方法名、公式、示意数值或实验结论。
3. 用目标论文的真实贡献、模块与依赖关系重写完整 prompt，并保留明确的低空白率约束。
4. 生成后先检查空白占比、裁切、文字、箭头、输入输出与科学关系，再决定是否入库。

## 数据与评测边界

36 个论文来源家族及其衍生图只用于学习和开发，必须排除在未来封闭评测之外；列表见 [`evaluation-exclusions.json`](evaluation-exclusions.json)。详细生成调用说明见 [`generation-summary.json`](generation-summary.json)。生成图不能充当定量曲线、消融、基准结果、用户研究或人工标注。

## 共建

欢迎通过 [Issue](https://github.com/exsinger-hub/Sivia/issues/new?template=knowledge-base.md) 或 [Pull Request](CONTRIBUTING.md) 提交有权公开的图文配对案例。投稿应包含最终 PNG、对应完整 prompt、来源与有价值的修改记录。代码的 MIT 许可不会自动覆盖第三方来源素材。
