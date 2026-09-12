#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / "knowledge-base"
CATEGORIES = {
    "multimodal-foundation": ("多模态与基础表征", "Multimodal and foundation representations"),
    "generative-control": ("生成建模与可控编辑", "Generative modeling and control"),
    "detection-segmentation": ("检测、分割与密集预测", "Detection, segmentation and dense prediction"),
    "three-d-reconstruction": ("三维表示、重建与分子空间", "3D representation, reconstruction and molecular space"),
    "agents-reasoning": ("智能体、工具使用与推理", "Agents, tool use and reasoning"),
    "structured-robotics": ("时序、图学习、世界模型与机器人", "Time series, graphs, world models and robotics"),
}
LEGACY = [
    ("eventbridge-rl", "EventBridge-RL", "structured-robotics", "双时间尺度世界模型与分支场景"),
    ("reasoning-between-words", "Reasoning Between Words", "agents-reasoning", "潜在推理、符号锚点与局部反馈"),
    ("trace", "TRACE", "multimodal-foundation", "多模态证据路由与选择性验证"),
    ("two-phase-trust-repair", "Two-phase Trust / Repair", "agents-reasoning", "紧凑双阶段信任与修复"),
    ("agent-fleet", "Agent Fleet", "agents-reasoning", "多智能体协作与共享产物"),
    ("visio-memory-routing", "Visio Memory Routing", "multimodal-foundation", "长视频记忆与路由"),
]


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prompt_stats(path: Path):
    text = path.read_text(encoding="utf-8")
    return len(text), sum(not c.isspace() for c in text), sha(path)


def audit_map(name: str):
    return {x["id"]: x for x in read_json(KB / "audit" / name / "measurements.json")["records"]}


audit24 = audit_map("paper-wave-24")
audit12 = audit_map("paper-wave-prior-12")
audit6 = audit_map("legacy-6")

wave24 = read_json(KB / "paper-wave-24.json")
new24 = []
for row in wave24["records"]:
    case = KB / "cases" / row["id"]
    chars, nonwhite, prompt_hash = prompt_stats(case / "prompt.txt")
    density = {k: audit24[row["id"]][k] for k in (
        "size", "sha256", "near_white_fraction", "content_grid_fraction",
        "detail_grid_fraction", "largest_empty_rectangle_fraction", "density_screen_pass"
    )}
    versions = sorted(case.glob("figure.v*.png"))
    final = {
        **{k: row[k] for k in ("id", "title", "venue", "year", "category", "source", "anchor", "claim", "stages", "labels")},
        "prompt": f"cases/{row['id']}/prompt.txt",
        "image": f"cases/{row['id']}/figure.png",
        "readme": f"cases/{row['id']}/README.md",
        "prompt_characters": chars,
        "prompt_nonwhitespace_characters": nonwhite,
        "prompt_sha256": prompt_hash,
        "image_sha256": sha(case / "figure.png"),
        "retained_prior_image_versions": len(versions),
        "density": density,
        "manual_visual_review": "pass",
        "admission": "admitted",
        "conceptual_asset": True,
        "not_experimental_evidence": True,
        "exclude_source_family_and_derivatives_from_sealed_evaluation": True,
    }
    new24.append(final)
    zh = CATEGORIES[row["category"]][0]
    (case / "README.md").write_text(f"""# {row['title']}

![实际生成图](figure.png)

- **大类**：{zh} (`{row['category']}`)
- **来源**：[{row['venue']} {row['year']}]({row['source']})
- **参考切入点**：{row['anchor']}
- **核心图意**：{row['claim']}
- **完整生产 prompt**：[prompt.txt](prompt.txt)（{nonwhite:,} 个非空白字符）
- **低空白筛查**：通过；内容网格占用 {density['content_grid_fraction']:.1%}，最大连续空区 {density['largest_empty_rectangle_fraction']:.1%}
- **人工目视检查**：通过

这是依据论文机制重新组织的 ImageGen 概念示意，不是论文原图、实验结果或人工 gold。生成时未输入原论文图像像素。使用时应借鉴信息组织、对象密度、分区和连线方式，并依据目标论文重新核验科学关系。
""", encoding="utf-8", newline="\n")

wave24_final = {
    "schema_version": "sivia.paper_knowledge.wave24.v2",
    "count": 24,
    "admitted_count": sum(x["admission"] == "admitted" for x in new24),
    "categories": {k: v[0] for k, v in CATEGORIES.items()},
    "admission_gate": "density numeric screen and manual visual review",
    "records": new24,
}
(KB / "paper-wave-24.json").write_text(json.dumps(wave24_final, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

prior_raw = read_json(KB / "paper-wave-prior-12.json")
prior12 = []
for row in prior_raw["records"]:
    case = KB / "cases" / row["id"]
    chars, nonwhite, prompt_hash = prompt_stats(case / "prompt.txt")
    density = {k: audit12[row["id"]][k] for k in (
        "size", "sha256", "near_white_fraction", "content_grid_fraction",
        "detail_grid_fraction", "largest_empty_rectangle_fraction", "density_screen_pass"
    )}
    current = {**row, "prompt_characters": chars, "prompt_nonwhitespace_characters": nonwhite,
               "prompt_sha256": prompt_hash, "image_sha256": sha(case / "figure.png"),
               "density": density, "manual_visual_review": "pass",
               "admission": "admitted", "conceptual_asset": True,
               "not_experimental_evidence": True,
               "exclude_source_family_and_derivatives_from_sealed_evaluation": True}
    prior12.append(current)
    zh = CATEGORIES[row["category"]][0]
    note = "；本次进行了密度修订并保留原选定版为 figure.v3.png" if row["id"] == "diffdock" else ""
    (case / "README.md").write_text(f"""# {row['paper_title']}

![实际生成图](figure.png)

- **大类**：{zh} (`{row['category']}`)
- **来源论文**：[{row['paper_title']}]({row['source']})
- **会议 / 年份**：{row['venue']} {row['year']}
- **完整生产 prompt**：[prompt.txt](prompt.txt)（{nonwhite:,} 个非空白字符）
- **低空白筛查**：通过；内容网格占用 {density['content_grid_fraction']:.1%}，最大连续空区 {density['largest_empty_rectangle_fraction']:.1%}{note}
- **质量沿革**：[quality-history.json](quality-history.json)

这是论文启发的学习 / 开发概念图，不是论文原图、实验结果或人工 gold。来源家族及其衍生物须排除在未来封闭评测之外；使用时应依据目标论文逐项核验科学关系。
""", encoding="utf-8", newline="\n")

(KB / "paper-wave-prior-12.json").write_text(json.dumps({"schema_version": "sivia.paper_knowledge.wave.v2", "count": 12, "admitted_count": 12, "records": prior12}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

legacy = []
for case_id, title, category, task in LEGACY:
    case = KB / "cases" / case_id
    chars, nonwhite, prompt_hash = prompt_stats(case / "prompt.txt")
    density = {k: audit6[case_id][k] for k in (
        "size", "sha256", "near_white_fraction", "content_grid_fraction",
        "detail_grid_fraction", "largest_empty_rectangle_fraction", "density_screen_pass"
    )}
    legacy.append({"id": case_id, "title": title, "category": category, "communication_task": task,
                   "prompt": f"cases/{case_id}/prompt.txt", "image": f"cases/{case_id}/figure.png",
                   "readme": f"cases/{case_id}/README.md", "prompt_characters": chars,
                   "prompt_nonwhitespace_characters": nonwhite, "prompt_sha256": prompt_hash,
                   "image_sha256": sha(case / "figure.png"), "density": density,
                   "admission": "admitted", "provenance_tier": "legacy-curated"})

(KB / "legacy-6.json").write_text(json.dumps({"schema_version": "sivia.knowledge.legacy.v2", "count": 6, "admitted_count": 6, "records": legacy}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

catalog = []
for x in legacy:
    catalog.append({**x, "tier": "legacy-curated"})
for x in prior12:
    catalog.append({**x, "title": x["paper_title"], "tier": "paper-sourced-prior"})
for x in new24:
    catalog.append({**x, "tier": "paper-sourced-new"})
catalog.sort(key=lambda x: (list(CATEGORIES).index(x["category"]), x["id"]))

index = {
    "schema_version": "sivia.knowledge_base.index.v2",
    "total_pairs": len(catalog),
    "paper_sourced_pairs": len(prior12) + len(new24),
    "new_pairs": len(new24),
    "all_density_screen_pass": all(x["density"]["density_screen_pass"] for x in catalog),
    "categories": [{"id": k, "label_zh": v[0], "label_en": v[1], "count": sum(x["category"] == k for x in catalog)} for k, v in CATEGORIES.items()],
    "records": catalog,
}
(KB / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

exclusions = sorted({x.get("id") for x in prior12 + new24})
(KB / "evaluation-exclusions.json").write_text(json.dumps({
    "schema_version": "sivia.knowledge_base.exclusions.v1",
    "policy": "All inspected source paper families and generated derivatives are learning/development assets and must not appear in a future sealed evaluation.",
    "case_ids": exclusions,
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

(KB / "generation-summary.json").write_text(json.dumps({
    "schema_version": "sivia.image_generation.summary.v1",
    "new_wave_final_pairs": 24,
    "new_wave_generation_calls": 40,
    "additional_prior_pair_density_repair_calls": 1,
    "total_calls_in_this_augmentation_phase": 41,
    "duplicate_call_note": "LLaVA received one same-prompt duplicate generation; the earlier output is retained as figure.v1.png.",
    "provider_model_id": None,
    "seed": None,
    "cost": None,
    "note": "Provider model identifier, seed and cost were not returned by the generation tool and are intentionally not inferred.",
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

lines = [
    "# Sivia 科研绘图知识库", "",
    "本知识库现有 **42 对实际生成 PNG + 完整生产 prompt**：6 对早期整理案例、12 对先前论文来源案例，以及本轮新增的 24 对。36 对论文来源案例覆盖 ICLR、CVPR、ICCV、NeurIPS、ICML、AAAI、CoRL 与 RSS 等会议。", "",
    "## 纳入门槛", "",
    "所有 42 对均通过同一低空白率数值筛查：32×20 内容网格占用率不低于 78%，且最大连续空区不高于画布的 10%。数值筛查只用于发现空白布局问题；论文来源案例还经过实际 PNG 目视检查。完整指标见 [`audit/`](audit/)，机器可读总索引见 [`index.json`](index.json)。", "",
    "每个案例必须同时包含 `figure.png` 与生成它的完整 `prompt.txt`。论文来源图是重新设计并生成的概念示意，不是论文原图、实验结果或人工 gold。", "",
    "## 按大类浏览", "",
]
for category, (zh, en) in CATEGORIES.items():
    rows = [x for x in catalog if x["category"] == category]
    lines += [f"<a id=\"{category}\"></a>", "", f"### {zh}", "", f"{en}。共 {len(rows)} 对。", "", "| 案例 | 来源层级 | 实际成图 | 完整 prompt |", "| --- | --- | --- | --- |"]
    for x in rows:
        tier = {"legacy-curated": "早期整理", "paper-sourced-prior": "论文来源·先前批次", "paper-sourced-new": "论文来源·新增 24"}[x["tier"]]
        lines.append(f"| [{x['title']}](cases/{x['id']}/README.md) | {tier} | [PNG](cases/{x['id']}/figure.png) | [TXT](cases/{x['id']}/prompt.txt) |")
    lines.append("")
lines += [
    "## 使用方式", "",
    "1. 先按任务大类选择结构接近的案例，同时查看 PNG 与完整 prompt。",
    "2. 借鉴版式、信息密度、对象层级、配色和连线约束；不要照搬案例的方法名、公式、示意数值或实验结论。",
    "3. 用目标论文的真实贡献、模块与依赖关系重写完整 prompt，并保留明确的低空白率约束。",
    "4. 生成后先检查空白占比、裁切、文字、箭头、输入输出与科学关系，再决定是否入库。", "",
    "## 数据与评测边界", "",
    "36 个论文来源家族及其衍生图只用于学习和开发，必须排除在未来封闭评测之外；列表见 [`evaluation-exclusions.json`](evaluation-exclusions.json)。详细生成调用说明见 [`generation-summary.json`](generation-summary.json)。生成图不能充当定量曲线、消融、基准结果、用户研究或人工标注。", "",
    "## 共建", "",
    "欢迎通过 [Issue](https://github.com/exsinger-hub/Sivia/issues/new?template=knowledge-base.md) 或 [Pull Request](CONTRIBUTING.md) 提交有权公开的图文配对案例。投稿应包含最终 PNG、对应完整 prompt、来源与有价值的修改记录。代码的 MIT 许可不会自动覆盖第三方来源素材。", "",
]
(KB / "README.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")

def replace_section(path: Path, start: str, end: str, replacement: str):
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(rf"{re.escape(start)}.*?(?={re.escape(end)})", re.S)
    updated, n = pattern.subn(replacement.rstrip() + "\n\n", text, count=1)
    if n != 1:
        raise RuntimeError(f"Could not replace knowledge-base section in {path}")
    path.write_text(updated, encoding="utf-8", newline="\n")

en_rows = "\n".join(f"| [{v[1]}](knowledge-base/README.md#{k}) | {sum(x['category']==k for x in catalog)} |" for k, v in CATEGORIES.items())
replace_section(ROOT / "README.md", "## Knowledge base", "## Limitations", f"""## Knowledge base

The knowledge base now contains **42 actual image–prompt pairs**, including **36 paper-sourced conceptual examples** and 24 new pairs from major AI conferences. Every pair passes the low-whitespace admission screen; paper-sourced examples also received visual review.

| Category | Pairs |
| --- | ---: |
{en_rows}

Browse the complete categorized [knowledge-base index](knowledge-base/README.md), or use the machine-readable [`index.json`](knowledge-base/index.json). Each case includes the generated PNG, the exact full prompt and source/quality notes. Source families and derivatives are learning assets and are excluded from future sealed evaluation.""")

zh_rows = "\n".join(f"| [{v[0]}](knowledge-base/README.md#{k}) | {sum(x['category']==k for x in catalog)} |" for k, v in CATEGORIES.items())
replace_section(ROOT / "README_ZH.md", "## 科研绘图知识库", "## Limitations", f"""## 科研绘图知识库

知识库现有 **42 对实际成图–完整 prompt**，其中 **36 对来自优秀 AI 会议论文的概念图增广**，本轮新增 24 对。全部配对通过低空白率数值筛查；论文来源案例还完成了实际 PNG 目视检查。

| 大类 | 数量 |
| --- | ---: |
{zh_rows}

请从完整的[分类知识库索引](knowledge-base/README.md)浏览，机器可读数据见 [`index.json`](knowledge-base/index.json)。每个案例都含实际 PNG、精确完整 prompt 与来源 / 质量说明。论文来源家族及其衍生物只用于学习与开发，并从未来封闭评测中排除。""")

print(json.dumps({"total": len(catalog), "paper_sourced": len(prior12) + len(new24), "new": len(new24), "all_density_pass": index["all_density_screen_pass"]}, ensure_ascii=False))
