"""Retain draft five and isolate its remaining dashed-maintenance junction repair."""
from pathlib import Path
import json, shutil
ROOT=Path(__file__).resolve().parents[3];PAIR=ROOT/'knowledge-base/restart-2026/pairs/autotool'
for name in ['prompt','figure']:
    suffix='txt' if name=='prompt' else 'png'
    old=PAIR/f'{name}.v4.{suffix}'
    if not old.exists(): shutil.copyfile(PAIR/f'{name}.{suffix}',old)
shutil.copyfile(PAIR/'prompt.next.txt',PAIR/'prompt.v5.txt')
shutil.copyfile(Path('C:/Users/admin/.codex/generated_images/01a094a3-03a2-7270-9111-16bea5aeaad3/exec-6027c6ee-5e2e-422e-8848-310a300c820c.png'),PAIR/'figure.v5.png')
body=(PAIR/'prompt.next.txt').read_text(encoding='utf-8').split('\n\n',1)[1]
header='''EDIT THE SINGLE ATTACHED AUTOTOOL FIFTH DRAFT. Preserve every scientific object, label and route, including the new solid blue connector up the narrow central gutter to Decision and tool execution. Change ONLY the small dashed Update graph junction in the bottom-left whitespace. Two pixel-scale actions on the attached 1586 by 992 image: (1) the dashed vertical line at x=315 currently runs from the very bottom feedback lane near y=968 up to the Tool Inertia Graph boundary at y=904. DELETE ONLY its lower segment from y=945 to y=968, leaving the bottom horizontal Next decision feedback lane intact and leaving the vertical segment from y=943 upward to the existing arrowhead at y=904 intact. The lower Next decision feedback must no longer turn upward into the graph. (2) The dashed horizontal Update graph line from Add to history currently terminates at about (457,943). EXTEND that same horizontal dashed line LEFT to (315,943), so it joins the retained vertical arrow segment. The resulting maintenance route must be one continuous polyline: Add to history -> left along y=943 -> upward at x=315 -> Tool Inertia Graph boundary at y=904. It is ABOVE and DISCONNECTED from the separate bottom Next decision feedback line at y=968. The label Update graph stays in place over its correct line. Do not draw a third line, a junction dot, another arrowhead, or any new label. All other composition and pixels stay unchanged. This correction changes only which existing line is connected to the upward graph arrow; it adds no new method. The full production specification follows for completeness, with this exact local junction instruction taking priority over any earlier maintenance-routing wording.

'''
prompt=header+body
assert 20426<=len(''.join(prompt.split())) and len(prompt)<=32000
(PAIR/'prompt.next.txt').write_bytes(prompt.encode('utf-8'))
print(json.dumps({'characters':len(prompt),'nonwhitespace':len(''.join(prompt.split()))}))
