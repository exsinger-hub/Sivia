import argparse
import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = {
    "self-rag": "agents-reasoning",
    "visprog": "agents-reasoning",
    "pdformer": "structured-robotics",
    "diffdock": "three-d-reconstruction",
    "dust3r": "three-d-reconstruction",
    "anywhere": "generative-control",
    "unisim": "structured-robotics",
    "depth-anything": "detection-segmentation",
    "dc2": "detection-segmentation",
    "ibot": "multimodal-foundation",
    "cutie": "detection-segmentation",
    "glass": "generative-control",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


parser = argparse.ArgumentParser(description="Import a reviewed paper-knowledge v2 snapshot.")
parser.add_argument("--source", type=Path, required=True, help="Directory containing knowledge-manifest.json and dataset.jsonl")
args = parser.parse_args()
SOURCE = args.source.resolve()
manifest = json.loads((SOURCE / "knowledge-manifest.json").read_text(encoding="utf-8"))
rows = {x["id"]: x for x in map(json.loads, (SOURCE / "dataset.jsonl").read_text(encoding="utf-8").splitlines())}
out = []
for group in manifest["groups"]:
    case_id = group["case_id"]
    row = rows[case_id]
    src_dir = SOURCE / "cases" / case_id
    dst_dir = ROOT / "knowledge-base" / "cases" / case_id
    dst_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE / group["prompt"], dst_dir / "prompt.txt")
    shutil.copyfile(SOURCE / group["image"], dst_dir / "figure.png")
    shutil.copyfile(SOURCE / group["quality_history"], dst_dir / "quality-history.json")
    source = row["source"]
    source_meta = {
        "paper_title": source["paper_title"],
        "venue": source["venue"],
        "year": source["year"],
        "topic": source["topic"],
        "official_url": source["official_acceptance_url"],
        "pdf_url": source["pdf_url"],
        "source_family": source["source_family"],
        "learning_only": True,
        "exclude_from_sealed_evaluation": True,
        "conceptual_asset": True,
    }
    (dst_dir / "source.json").write_text(json.dumps(source_meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    readme = f"""# {source['paper_title']}

![实际生成图](figure.png)

- **类别**：`{CATEGORIES[case_id]}`
- **来源论文**：[{source['paper_title']}]({source['official_acceptance_url']})
- **会议 / 年份**：{source['venue']} {source['year']}
- **用途**：论文启发的学习 / 开发概念图；不是论文原图或实验结果
- **完整 prompt**：[prompt.txt](prompt.txt)
- **历史质量记录**：[quality-history.json](quality-history.json)

此目录只纳入最终选定的 prompt–PNG 配对。来源家族及其衍生物须排除在未来封闭评测之外；图中关系仍应按目标论文逐项核验。
"""
    (dst_dir / "README.md").write_text(readme, encoding="utf-8", newline="\n")
    out.append({
        "id": case_id,
        "category": CATEGORIES[case_id],
        "paper_title": source["paper_title"],
        "venue": source["venue"],
        "year": source["year"],
        "source": source["official_acceptance_url"],
        "selected_source_version": group["version"],
        "prompt": f"cases/{case_id}/prompt.txt",
        "image": f"cases/{case_id}/figure.png",
        "readme": f"cases/{case_id}/README.md",
        "quality_history": f"cases/{case_id}/quality-history.json",
        "prompt_sha256": sha(dst_dir / "prompt.txt"),
        "image_sha256": sha(dst_dir / "figure.png"),
        "admission_basis": "explicit_user_instruction_after_historical_review",
    })

(ROOT / "knowledge-base" / "paper-wave-prior-12.json").write_text(
    json.dumps({"schema_version": "sivia.paper_knowledge.wave.v1", "count": len(out), "records": out}, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
    newline="\n",
)
print(json.dumps({"imported": len(out)}, ensure_ascii=False))
