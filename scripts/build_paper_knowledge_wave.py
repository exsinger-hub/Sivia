#!/usr/bin/env python3
"""Build prompts and metadata for the 24-paper knowledge-base expansion.

The generated prompt is the exact text submitted to ImageGen.  It instantiates
the bundled overview template and leaves no bracketed authoring slots.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / "knowledge-base"
TEMPLATE = ROOT / "skills/design-scientific-figure/references/templates/overview-template.txt"
OUT = KB / "cases"

CATEGORIES = {
    "multimodal-foundation": "多模态基础模型",
    "generative-control": "生成与可控编辑",
    "detection-segmentation": "检测、分割与开放词汇定位",
    "three-d-reconstruction": "三维表示、重建与新视角合成",
    "agents-reasoning": "智能体、工具使用与推理",
    "structured-robotics": "时序、图学习与机器人策略",
}

PAPERS = [
 {"id":"blip2","title":"BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models","venue":"ICML","year":2023,"category":"multimodal-foundation","source":"https://proceedings.mlr.press/v202/li23q.html","anchor":"method overview and two-stage Q-Former pretraining","claim":"A lightweight Querying Transformer bridges a frozen image encoder and a frozen language model through two distinct pretraining stages.","stages":["image and text pairs","frozen image encoder","Q-Former with learned queries","vision-language representation stage","vision-to-language generation stage","frozen LLM","instruction-following output"],"labels":["Frozen image encoder","Q-Former","Learned queries","Stage 1: representation","Stage 2: generation","Frozen LLM","Image-grounded text"]},
 {"id":"instructblip","title":"InstructBLIP: Towards General-purpose Vision-Language Models with Instruction Tuning","venue":"NeurIPS","year":2023,"category":"multimodal-foundation","source":"https://proceedings.neurips.cc/paper_files/paper/2023/hash/9a6a435e75419a836fe47ab6793623e6-Abstract-Conference.html","anchor":"instruction-aware Q-Former overview","claim":"An instruction-aware Query Transformer selects visual evidence conditioned on the instruction before a frozen language model answers.","stages":["image","natural-language instruction","frozen image encoder","instruction-aware Q-Former","instruction-conditioned visual tokens","frozen LLM","task response"],"labels":["Image","Instruction","Frozen vision encoder","Instruction-aware Q-Former","Visual tokens","Frozen LLM","Response"]},
 {"id":"llava","title":"Visual Instruction Tuning","venue":"NeurIPS","year":2023,"category":"multimodal-foundation","source":"https://proceedings.neurips.cc/paper_files/paper/2023/file/6dcf277ea32ce3288914faf369fe6de0-Paper-Conference.pdf","anchor":"visual instruction data generation and LLaVA architecture","claim":"Language-only GPT-4 converts image captions and boxes into visual instructions, then a projection connects a vision encoder to an LLM for instruction tuning.","stages":["image with captions and boxes","GPT-4 instruction-data generation","visual instruction triples","frozen vision encoder","trainable projection","large language model","multimodal assistant response"],"labels":["Image metadata","GPT-4","Instruction data","Vision encoder","Projection W","LLM","Assistant response"]},
 {"id":"flamingo","title":"Flamingo: a Visual Language Model for Few-Shot Learning","venue":"NeurIPS","year":2022,"category":"multimodal-foundation","source":"https://proceedings.neurips.cc/paper_files/paper/2022/hash/960a172bc7fbf0177ccccbb411a7d800-Abstract-Conference.html","anchor":"Perceiver Resampler and gated cross-attention architecture","claim":"A Perceiver Resampler compresses variable visual inputs into tokens injected through gated cross-attention layers of a frozen language model.","stages":["interleaved images video and text","frozen vision encoder","Perceiver Resampler","fixed visual tokens","gated cross-attention dense blocks","frozen language model","few-shot multimodal completion"],"labels":["Interleaved context","Frozen vision encoder","Perceiver Resampler","Visual tokens","Gated XATTN-DENSE","Frozen LM","Completion"]},
 {"id":"latent-diffusion","title":"High-Resolution Image Synthesis with Latent Diffusion Models","venue":"CVPR","year":2022,"category":"generative-control","source":"https://openaccess.thecvf.com/content/CVPR2022/html/Rombach_High-Resolution_Image_Synthesis_With_Latent_Diffusion_Models_CVPR_2022_paper.html","anchor":"latent diffusion architecture","claim":"Perceptual compression moves diffusion from pixels into a lower-dimensional latent space while cross-attention injects flexible conditioning.","stages":["high-resolution image","encoder E","compact latent z","iterative latent denoising U-Net","cross-attention conditioning","decoder D","generated image"],"labels":["Pixel space","Encoder E","Latent z","Denoising U-Net","Cross-attention","Decoder D","Output"]},
 {"id":"controlnet","title":"Adding Conditional Control to Text-to-Image Diffusion Models","venue":"ICCV","year":2023,"category":"generative-control","source":"https://openaccess.thecvf.com/content/ICCV2023/html/Zhang_Adding_Conditional_Control_to_Text-to-Image_Diffusion_Models_ICCV_2023_paper.html","anchor":"locked backbone, trainable copy and zero convolutions","claim":"A trainable copy of a locked diffusion encoder receives spatial controls and connects through zero convolutions without disrupting the pretrained backbone at initialization.","stages":["text prompt and spatial condition","condition encoder","trainable encoder copy","zero convolution bridges","locked pretrained U-Net","decoder path","spatially controlled image"],"labels":["Condition","Trainable copy","Zero convolution","Locked backbone","Skip features","Decoder","Controlled result"]},
 {"id":"dit","title":"Scalable Diffusion Models with Transformers","venue":"ICCV","year":2023,"category":"generative-control","source":"https://openaccess.thecvf.com/content/ICCV2023/html/Peebles_Scalable_Diffusion_Models_with_Transformers_ICCV_2023_paper.html","anchor":"Diffusion Transformer block variants","claim":"A transformer processes patches of noisy latent inputs, with timestep and class conditioning modulating repeated DiT blocks before latent decoding.","stages":["noisy latent input","patchify and linear embedding","timestep and class embeddings","stacked DiT blocks","adaptive layer normalization conditioning","unpatchify predicted noise","VAE decoder output"],"labels":["Noisy latent","Patchify","t + class","DiT block × N","adaLN-Zero","Unpatchify","Image"]},
 {"id":"dreambooth","title":"DreamBooth: Fine Tuning Text-to-Image Diffusion Models for Subject-Driven Generation","venue":"CVPR","year":2023,"category":"generative-control","source":"https://openaccess.thecvf.com/content/CVPR2023/html/Ruiz_DreamBooth_Fine_Tuning_Text-to-Image_Diffusion_Models_for_Subject-Driven_Generation_CVPR_2023_paper.html","anchor":"subject binding and prior-preservation training","claim":"A rare identifier binds a few subject images to a pretrained diffusion model while class-specific prior preservation protects diversity.","stages":["few subject images","rare identifier plus class noun","subject reconstruction branch","class image generation branch","prior-preservation loss","fine-tuned diffusion model","subject in new contexts"],"labels":["Subject images","V-token dog","Reconstruction loss","Class prior","Prior-preservation loss","Fine-tune","New context"]},
 {"id":"segment-anything","title":"Segment Anything","venue":"ICCV","year":2023,"category":"detection-segmentation","source":"https://openaccess.thecvf.com/content/ICCV2023/html/Kirillov_Segment_Anything_ICCV_2023_paper.html","anchor":"Figure 1 task-model-data loop","claim":"A promptable segmentation task, a modular model and an iterative data engine reinforce one another to produce transferable masks and a billion-mask dataset.","stages":["image and point box mask or text prompt","image encoder","prompt encoder","lightweight mask decoder","valid masks","data engine annotate and train loop","SA-1B dataset"],"labels":["Promptable task","Image encoder","Prompt encoder","Mask decoder","Valid masks","Data engine","SA-1B"]},
 {"id":"mask2former","title":"Masked-Attention Mask Transformer for Universal Image Segmentation","venue":"CVPR","year":2022,"category":"detection-segmentation","source":"https://openaccess.thecvf.com/content/CVPR2022/html/Cheng_Masked-Attention_Mask_Transformer_for_Universal_Image_Segmentation_CVPR_2022_paper.html","anchor":"masked-attention decoder architecture","claim":"Queries attend only within predicted mask regions across a multiscale pixel decoder, yielding one architecture for semantic, instance and panoptic segmentation.","stages":["image","backbone multiscale features","pixel decoder","transformer decoder queries","masked cross-attention","class and mask prediction","semantic instance panoptic outputs"],"labels":["Backbone","Pixel decoder","Queries","Masked attention","Class head","Mask head","Universal outputs"]},
 {"id":"tube-link","title":"Tube-Link: A Flexible Cross Tube Framework for Universal Video Segmentation","venue":"ICCV","year":2023,"category":"detection-segmentation","source":"https://openaccess.thecvf.com/content/ICCV2023/html/Li_Tube-Link_A_Flexible_Cross_Tube_Framework_for_Universal_Video_Segmentation_ICCV_2023_paper.html","anchor":"short-subclip tube prediction and cross-tube association","claim":"Short subclips yield tube masks that are linked through query-level cross-tube attention and temporal contrastive features for long-video segmentation.","stages":["long video split into subclips","shared video segmentation backbone","subclip queries","spatiotemporal tube masks","cross-tube query attention","temporal contrastive association","linked long-video tracks"],"labels":["Subclips","Shared backbone","Tube queries","Tube masks","Cross-tube attention","Contrastive association","Linked tracks"]},
 {"id":"video-grounding-dino","title":"VideoGrounding-DINO: Towards Open-Vocabulary Spatio-Temporal Video Grounding","venue":"CVPR","year":2024,"category":"detection-segmentation","source":"https://openaccess.thecvf.com/content/CVPR2024/html/Wasim_VideoGrounding-DINO_Towards_Open-Vocabulary_Spatio-Temporal_Video_Grounding_CVPR_2024_paper.html","anchor":"open-vocabulary video grounding overview","claim":"Language-conditioned object queries localize referred entities across frames, then temporal modeling links detections into a spatiotemporal tube.","stages":["video frames and free-form phrase","visual and language encoders","cross-modal feature fusion","language-guided object queries","frame-level open-vocabulary boxes","temporal association","grounded video tube"],"labels":["Video","Text phrase","Cross-modal fusion","Object queries","Open-vocabulary boxes","Temporal link","Grounded tube"]},
 {"id":"mipnerf360","title":"Mip-NeRF 360: Unbounded Anti-Aliased Neural Radiance Fields","venue":"CVPR","year":2022,"category":"three-d-reconstruction","source":"https://openaccess.thecvf.com/content/CVPR2022/html/Barron_Mip-NeRF_360_Unbounded_Anti-Aliased_Neural_Radiance_Fields_CVPR_2022_paper.html","anchor":"contracted coordinates, proposal sampling and distortion regularization","claim":"Scene contraction maps unbounded space into a bounded domain while proposal sampling and distortion regularization allocate detail efficiently along conical frustums.","stages":["360-degree camera rays","conical frustum samples","scene contraction","proposal MLP sampling","mip-NeRF radiance field","distortion regularizer","RGB and depth rendering"],"labels":["Camera rays","Conical frustums","Contracted space","Proposal sampling","Radiance field","Distortion loss","RGB + depth"]},
 {"id":"neuralangelo","title":"Neuralangelo: High-Fidelity Neural Surface Reconstruction","venue":"CVPR","year":2023,"category":"three-d-reconstruction","source":"https://openaccess.thecvf.com/content/CVPR2023/html/Li_Neuralangelo_High-Fidelity_Neural_Surface_Reconstruction_CVPR_2023_paper.html","anchor":"multiresolution hash grid and numerical-gradient reconstruction","claim":"Numerical gradients smooth high-order derivatives while coarse-to-fine activation of multiresolution hash grids progressively reveals high-fidelity surfaces from RGB views.","stages":["posed multiview RGB images","camera ray sampling","multiresolution hash-grid SDF","numerical gradients","neural volume rendering","coarse-to-fine optimization","detailed mesh and normals"],"labels":["RGB views","Rays","Hash-grid SDF","Numerical gradient","Volume rendering","Coarse-to-fine","Mesh + normals"]},
 {"id":"gaussian-dreamer","title":"GaussianDreamer: Fast Generation from Text to 3D Gaussians by Bridging 2D and 3D Diffusion Models","venue":"CVPR","year":2024,"category":"three-d-reconstruction","source":"https://openaccess.thecvf.com/content/CVPR2024/html/Yi_GaussianDreamer_Fast_Generation_from_Text_to_3D_Gaussians_by_Bridging_CVPR_2024_paper.html","anchor":"3D prior initialization and 2D diffusion refinement","claim":"A text-conditioned 3D diffusion prior initializes Gaussian geometry, then 2D diffusion guidance refines appearance through differentiable Gaussian rendering.","stages":["text prompt","3D diffusion point-cloud prior","noisy point growth and color perturbation","3D Gaussian initialization","differentiable splatting","2D diffusion score distillation","consistent 3D asset"],"labels":["Text","3D prior","Grow + perturb","3D Gaussians","Render views","2D diffusion guidance","3D asset"]},
 {"id":"3dgstream","title":"3DGStream: On-the-Fly Training of 3D Gaussians for Efficient Streaming of Photo-Realistic Free-Viewpoint Videos","venue":"CVPR","year":2024,"category":"three-d-reconstruction","source":"https://openaccess.thecvf.com/content/CVPR2024/html/Sun_3DGStream_On-the-Fly_Training_of_3D_Gaussians_for_Efficient_Streaming_of_CVPR_2024_paper.html","anchor":"neural transformation cache and adaptive Gaussian addition","claim":"A compact neural transformation cache updates persistent 3D Gaussians frame by frame, while adaptive additions represent newly emerging content.","stages":["multiview video stream","initial 3D Gaussians","frame-conditioned neural transformation cache","translation and rotation updates","adaptive Gaussian addition","fast per-frame optimization","free-viewpoint rendering"],"labels":["Video stream","Base 3D Gaussians","NTC","Transform","Add Gaussians","On-the-fly update","Novel view"]},
 {"id":"react","title":"ReAct: Synergizing Reasoning and Acting in Language Models","venue":"ICLR","year":2023,"category":"agents-reasoning","source":"https://openreview.net/pdf?id=WE_vluYUL-X","anchor":"Figure 1 interleaved thought-action-observation trajectories","claim":"Interleaving reasoning traces with environment actions lets observations update the plan and reduces hallucination compared with reasoning-only or action-only trajectories.","stages":["task question or goal","Thought: plan and state","Action: tool or environment call","Observation: returned evidence","updated Thought","repeated action-observation loop","final answer or task completion"],"labels":["Goal","Thought","Action","Observation","Updated thought","ReAct loop","Answer"]},
 {"id":"tree-of-thoughts","title":"Tree of Thoughts: Deliberate Problem Solving with Large Language Models","venue":"NeurIPS","year":2023,"category":"agents-reasoning","source":"https://proceedings.neurips.cc/paper_files/paper/2023/hash/271db9922b8d1f4dd7aaef84ed5ac703-Abstract.html","anchor":"Figure 1 comparison of IO, CoT, self-consistency and ToT","claim":"Thought decomposition, state evaluation and search allow a language model to explore, prune and backtrack over multiple reasoning paths instead of committing left to right.","stages":["problem state","generate candidate thoughts","branch into partial solutions","evaluate states","prune low-value branches","look ahead or backtrack","selected solution path"],"labels":["Problem","Thought generator","Candidates","State evaluator","Prune","Backtrack","Solution"]},
 {"id":"toolformer","title":"Toolformer: Language Models Can Teach Themselves to Use Tools","venue":"NeurIPS","year":2023,"category":"agents-reasoning","source":"https://proceedings.neurips.cc/paper/2023/hash/d842425e4bf79ba039352da0f658a906-Abstract-Conference.html","anchor":"self-supervised API-call insertion and filtering pipeline","claim":"A language model samples candidate API calls, executes them and retains only calls that reduce language-model loss, producing its own tool-use training data.","stages":["unlabeled text","sample API call positions and arguments","execute calculator search translation QA or calendar","insert API response","loss-based call filtering","fine-tune language model","autonomous tool use at inference"],"labels":["Text","Sample API calls","Execute tools","Insert response","Loss filter","Fine-tune","Tool-using LM"]},
 {"id":"reflexion","title":"Reflexion: Language Agents with Verbal Reinforcement Learning","venue":"NeurIPS","year":2023,"category":"agents-reasoning","source":"https://proceedings.neurips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html","anchor":"actor-evaluator-self-reflection episodic loop","claim":"An actor receives scalar or textual feedback, converts failure into a verbal reflection and stores it in episodic memory to guide the next trial without weight updates.","stages":["task and memory context","actor trajectory","environment result","evaluator feedback","self-reflection model","episodic memory update","improved next trial"],"labels":["Task","Actor","Trajectory","Evaluator","Reflection","Episodic memory","Next trial"]},
 {"id":"patchtst","title":"A Time Series is Worth 64 Words: Long-term Forecasting with Transformers","venue":"ICLR","year":2023,"category":"structured-robotics","source":"https://openreview.net/pdf?id=Jbdc0vTOcol","anchor":"channel-independent patch Transformer","claim":"Each time-series channel is segmented into subseries patches, embedded as tokens and processed by shared Transformer weights while preserving channel independence.","stages":["multivariate history","split channels independently","overlapping subseries patches","shared patch embedding","shared Transformer encoder","flatten and prediction heads","multihorizon forecasts"],"labels":["History","Channel independence","Patches","Shared embedding","Transformer","Prediction head","Forecast"]},
 {"id":"graphgps","title":"Recipe for a General, Powerful, Scalable Graph Transformer","venue":"NeurIPS","year":2022,"category":"structured-robotics","source":"https://proceedings.neurips.cc/paper_files/paper/2022/hash/5d4834a159f1547b267a05a4e2b7cf5e-Abstract-Conference.html","anchor":"GraphGPS layer recipe","claim":"Positional or structural encodings feed a layer that combines local message passing and global attention before a feed-forward update, retaining linear-scale variants.","stages":["graph nodes edges and encodings","positional structural encoding","local message-passing branch","global attention branch","sum and normalization","feed-forward network","updated node representations"],"labels":["Graph","PE / SE","Local MPNN","Global attention","Add + Norm","FFN","Updated nodes"]},
 {"id":"diffusion-policy","title":"Diffusion Policy: Visuomotor Policy Learning via Action Diffusion","venue":"RSS","year":2023,"category":"structured-robotics","source":"https://roboticsproceedings.org/rss19/p026.html","anchor":"Figure 1 policy representations and receding-horizon diffusion control","claim":"A conditional action-score model iteratively denoises a multimodal action sequence from noise, then receding-horizon control executes only the leading actions and replans from new observations.","stages":["camera and robot observations","visual conditioning encoder","noisy action horizon","K denoising iterations","multimodal action sequence","execute leading action chunk","new observation and replan"],"labels":["Observation","Visual encoder","Noisy actions","Denoise × K","Action horizon","Execute prefix","Replan"]},
 {"id":"rt2","title":"RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control","venue":"CoRL","year":2023,"category":"structured-robotics","source":"https://proceedings.mlr.press/v229/zitkovich23a","anchor":"co-fine-tuning web and robot data as token sequences","claim":"Web-scale vision-language examples and robot trajectories are co-fine-tuned in one token interface by expressing discretized robot actions as text tokens.","stages":["web image-text tasks","robot image instruction trajectories","vision-language backbone","co-fine-tuning mixture","action tokenization","vision-language-action model","decoded robot control"],"labels":["Web VQA","Robot trajectories","VLM backbone","Co-fine-tune","Action tokens","RT-2","Robot control"]},
]

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def substitutions(p: dict) -> dict[str, str]:
    stages = p["stages"]
    labels = p["labels"]
    palette = "navy structure, blue information, teal learned transformation, amber conditioning or feedback, coral warning only when scientifically necessary, pale neutral panels"
    return {
      "PAPER_TITLE": p["title"], "SHORT_FIGURE_TITLE": p["id"].replace("-", " ").title(),
      "ONE_SENTENCE_FIGURE_CLAIM": p["claim"], "RESEARCH_PROBLEM": p["claim"],
      "SOURCE_SUPPORTED_LIMITATION": "the input modalities or states cannot reach the final output through a single unstructured box without obscuring the paper's distinctive operation",
      "OVERVIEW_SCOPE": p["anchor"], "MAIN_STAGES_AND_MECHANISM": " -> ".join(stages),
      "CANVAS_RATIO_AND_PUBLICATION_WIDTH": "a 16:9 landscape canvas designed for a two-column-paper width of 178 mm",
      "CHOSEN_COMPOSITION": "a compact left-to-right scientific narrative with three unequal regions and one expanded central mechanism",
      "PRIMARY_READING_PATH": "left input context, through the enlarged central operation, to the right output, followed by the lower support strip",
      "FOCAL_REGION": stages[2] + " and " + stages[3] + " as the largest central visual mass",
      "REGION_PROPORTIONS": "22% input/context, 53% method mechanism, 25% output/support; outer margins 2.5% and gutters 1.5%",
      "MAIN_GROUP_1": "Input and problem setup", "GROUP_1_OBJECTS": ", ".join(stages[:2]),
      "GROUP_1_TRANSFORMATION": f"convert {stages[0]} into {stages[1]}", "GROUP_1_VISIBLE_TEXT": ", ".join(labels[:2]),
      "MAIN_GROUP_2": "Distinctive method", "GROUP_2_EDITORIAL_ROLE": "show the scientific operation that distinguishes this paper",
      "GROUP_2_OBJECTS": ", ".join(stages[2:5]), "GROUP_2_TRANSFORMATION": f"{stages[2]} feeds {stages[3]}, which produces or controls {stages[4]}",
      "MAIN_GROUP_3": "Output and interpretation", "GROUP_3_OBJECTS": ", ".join(stages[5:]),
      "GROUP_3_TRANSFORMATION": f"{stages[5]} yields {stages[6]}", "GROUP_3_VISIBLE_TEXT": ", ".join(labels[5:]),
      "EXACT_MAIN_TOPOLOGY": " -> ".join(stages), "CRITICAL_CORRESPONDENCES_AND_OPERANDS": "; ".join(f"{stages[i]} feeds {stages[i+1]}" for i in range(len(stages)-1)),
      "VERIFIED_CROSS_SCOPE_EDGES": f"{stages[0]} to {stages[1]}; {stages[4]} to {stages[5]}",
      "INPUT_LOCATION": "left region", "INPUT_OBJECTS": ", ".join(stages[:2]), "INPUT_VISUAL_CARRIER": "concrete miniature scenes plus aligned token, grid, graph or sequence carriers appropriate to the source",
      "INPUT_LABELS_AND_DIMENSIONS": ", ".join(labels[:2]), "CONTEXT_SCENE": stages[0], "CONTEXT_OBJECTS_AND_RELATIONS": f"{stages[0]} visibly supplies {stages[1]}",
      "CORE_TRANSFORMATION": f"{stages[2]} -> {stages[3]} -> {stages[4]}", "BEFORE_STATE": stages[2], "NOVEL_OPERATION": stages[3], "AFTER_STATE": stages[4],
      "OPERATION_SEQUENCE": " -> ".join(stages[2:5]), "PERSISTENT_IDENTITY": "use three repeated colored markers to preserve the same sample, query, node, token, object or state across transformations",
      "CONDITIONING_EDGES": f"draw a distinct amber conditioning edge from {stages[2]} to {stages[3]} only when that relation is conditioning rather than data flow",
      "BRANCH_NAMES": "primary computation and auxiliary conditioning/support", "MERGE_AND_SKIP_TOPOLOGY": f"merge all required operands immediately before {stages[5]}; no decorative skip edge",
      "PARAMETER_SHARING_CUE": "dotted braces and a short Shared or Frozen label only where the source explicitly states sharing or freezing", "INDEPENDENCE_CUE": "parallel lanes remain separated and are not drawn as a serial dependency",
      "OUTPUT_LOCATION": "right region", "OUTPUT_OBJECTS": ", ".join(stages[5:]), "OUTPUT_VISUAL_CARRIER": "a compact, concrete result scene beside the final symbolic representation",
      "TRAINING_OR_SUPPORT_SCENE": "a narrow lower strip containing only source-grounded training, update, or support relations needed to interpret the main method",
      "OBJECTIVE_EQUATION": "show no invented objective; if an equation is needed, use only named operators and symbolic loss terms from the source",
      "SUPPORT_FIELD_LOCATIONS": "lower strip aligned beneath the exact consumer", "PAIRED_FIELDS": "before/after, input/output, or adjacent frames use matched crops and persistent identity markers",
      "EMPIRICAL_FIELD_SPECIFICATION": "all pictured images, masks, depth maps, graphs, robot scenes and trajectories are clearly stylized conceptual miniatures, never represented as measured experimental output",
      "FIELD_DISPLAY_RULES": "preserve aspect ratio and keep every atomic field inside its own frame with a short label", "COMPUTED_CONTENT_SPECIFICATION": "no quantitative curves or performance numbers",
      "VERIFIED_DIMENSIONS_AND_VALUES": "no numeric result values are printed; only source-defined names and multiplication signs such as ×N or ×K may appear", "METRIC_LABELS_AND_UNITS": "none",
      "EXPANSION_LOCATION": "center of the main mechanism region", "DETAIL_SCOPE": f"expand {stages[2]}, {stages[3]}, and {stages[4]} without adding unrelated modules",
      "VISIBLE_TEXT_LIST": ", ".join(labels), "SYMBOL_DICTIONARY": "; ".join(f"{i+1}: {x}" for i,x in enumerate(labels)),
      "TYPE_SCALE_AT_PUBLICATION_SIZE": "section headers 10-11 pt, module labels 8-9 pt, secondary annotations 7 pt minimum at 178 mm width",
      "SEMANTIC_PALETTE": palette, "APPROVED_LAYOUT_AND_LOCAL_FIT_RULES": "fill the usable canvas tightly; meaningful-content hull must cover 82-92% of canvas width and 76-90% of canvas height",
      "LOCKED_REFERENCE_GEOMETRY": "no external reference image is attached; follow this prompt's frozen region proportions", "AUTHORIZED_LOCAL_CHANGES": "none during initial generation",
      "AUTHORIZED_MODIFICATIONS": "none during initial generation", "ALLOWED_CHANGE_BOUNDARIES": "initial generation only; later repairs must preserve all unaffected regions",
    }

def prompt_for(p: dict) -> str:
    text = TEMPLATE.read_text(encoding="utf-8")
    sub = substitutions(p)
    for key, value in sub.items(): text = text.replace(f"[{key}]", value)
    leftovers = sorted(set(re.findall(r"\[[A-Z0-9_]+\]", text)))
    if leftovers:
        raise ValueError(f"unfilled slots for {p['id']}: {leftovers}")
    preface = f"""CREATE ONE PUBLICATION-STYLE SCIENTIFIC ILLUSTRATION.

SOURCE CONTRACT
Paper: {p['title']} ({p['venue']} {p['year']}).
Primary source: {p['source']}
Source figure anchor: {p['anchor']}.
Scientific message: {p['claim']}

This is a source-grounded conceptual adaptation for a visual knowledge base. Do not copy source pixels, author logos, paper typography, result tables, benchmark numbers, or photographic examples. Preserve the method relationships named below while drawing new miniature scenes and clean schematic geometry. The generated figure is not experimental evidence.

DENSITY GATE — HIGHEST PRIORITY
Use a 16:9 landscape canvas. Keep the meaningful-content bounding hull within 2.5%–97.5% horizontally and 4%–96% vertically. Fill 82%–92% of the canvas width and 76%–90% of its height with meaningful scientific objects. No empty banner, empty lower third, oversized title, decorative margins, floating islands, or unused panel. Enlarge panels and objects until the largest rectangular empty region is below 4% of canvas area, while retaining narrow connector lanes. The title occupies at most 5% of canvas height. Every large light region must contain a diagram, scene, representation, legend, or necessary connector lane.

CASE-SPECIFIC TOPOLOGY
Stages: {' -> '.join(p['stages'])}.
Exact visible labels: {', '.join(p['labels'])}.
Only these short labels and source-grounded symbols appear in the artwork. Do not typeset this production prose.

"""
    final = preface + text
    nonwhite = len(re.sub(r"\s+", "", final))
    if nonwhite < 15356 or len(final) > 31900:
        raise ValueError(f"{p['id']} prompt length invalid: {len(final)} / {nonwhite}")
    return final

def main() -> None:
    records=[]
    for p in PAPERS:
        folder=OUT / p["id"]
        folder.mkdir(parents=True,exist_ok=True)
        prompt=prompt_for(p)
        prompt_path=folder/"prompt.txt"
        prompt_path.write_text(prompt,encoding="utf-8",newline="\n")
        readme=f"""# {p['title']}

- 大类：{CATEGORIES[p['category']]}
- 来源：[{p['venue']} {p['year']}]({p['source']})
- 参考位置：{p['anchor']}
- 图意：{p['claim']}
- 状态：ImageGen 生成的概念示意；不是原论文图复刻、实验结果或人工 gold。

本案例包含生成时提交的完整 [`prompt.txt`](prompt.txt) 和对应的实际 [`figure.png`](figure.png)。借鉴其信息组织、对象密度、分区和连线方式；使用时必须重新依据目标论文核对科学关系。原论文像素没有进入生成输入。图像发布前需通过低空白率、裁切、文本与关系检查。
"""
        (folder/"README.md").write_text(readme,encoding="utf-8",newline="\n")
        records.append({**p,"category_label":CATEGORIES[p["category"]],"prompt":"cases/%s/prompt.txt"%p["id"],"image":"cases/%s/figure.png"%p["id"],"readme":"cases/%s/README.md"%p["id"],"prompt_characters":len(prompt),"prompt_nonwhitespace_characters":len(re.sub(r"\s+","",prompt)),"prompt_sha256":sha(prompt_path),"image_status":"pending_generation"})
    (KB/"paper-wave-24.json").write_text(json.dumps({"schema_version":"sivia.paper_knowledge.wave24.v1","count":len(records),"categories":CATEGORIES,"records":records},ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    print(json.dumps({"count":len(records),"min_chars":min(x["prompt_characters"] for x in records),"max_chars":max(x["prompt_characters"] for x in records),"min_nonwhite":min(x["prompt_nonwhitespace_characters"] for x in records),"max_nonwhite":max(x["prompt_nonwhitespace_characters"] for x in records)},ensure_ascii=False))

if __name__=="__main__": main()
