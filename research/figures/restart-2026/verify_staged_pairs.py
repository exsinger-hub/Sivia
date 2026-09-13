"""Verify that Git preserves the exact PNG and production-prompt bytes."""
from pathlib import Path
import json, subprocess
ROOT=Path(__file__).resolve().parents[3];KB=ROOT/'knowledge-base';OUT=KB/'restart-2026'
files=set()
for r in json.loads((KB/'index.json').read_text(encoding='utf-8'))['records']:
    files.update(KB/r[key] for key in ['prompt','image'])
for r in json.loads((OUT/'pairs.json').read_text(encoding='utf-8'))['records']:
    directory=(OUT/r['prompt']).parent
    for version in r['versions']:
        files.update(directory/version[key] for key in ['prompt','image'])
for path in sorted(files):
    relative=path.relative_to(ROOT).as_posix()
    staged=subprocess.check_output(['git','show',':'+relative],cwd=ROOT)
    assert staged==path.read_bytes(),relative
print(json.dumps({'valid':True,'exact_prompt_image_files_preserved_in_git_index':len(files)},indent=2))
