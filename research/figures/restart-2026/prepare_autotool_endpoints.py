"""Save the exact full prompt for an endpoint-only repair of the fourth draft."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[3]
PAIR=ROOT/'knowledge-base/restart-2026/pairs/autotool'
source=(PAIR/'prompt.txt').read_text(encoding='utf-8')
target=PAIR/'prompt.next.txt'
header='''EDIT THE SINGLE ATTACHED AUTOTOOL FOURTH DRAFT. Preserve its exact compact composition, every scientific object, all labels, colors and the existing correct two-route shared execution. Make only TWO connector endpoint repairs. First, add the missing information handoff from the filled LoadAuthorNet card at the bottom-right of the central Parameter filling panel into the enclosing Two-route decision inset. On the attached 1586 by 992 canvas, start at approximately (1040,875), exit right into the narrow inter-panel gutter, turn upward at x=1060, continue to y=151, then turn right and END on the LEFT BORDER of the enclosing decision inset near (1078,151). Keep this thin dark-blue information connector outside all panel interiors; it carries candidate and argument status into the decision. It MUST NOT enter Observation, Execute tool, either completed call, or either colored branch directly. Do not add a long label in the narrow gutter; the existing two checks explain the input. This continuous connector resolves the missing input relationship without changing the decision logic. Second, the existing dashed bottom maintenance arrow labeled Update graph currently ends below the Tool Inertia Graph instead of touching it. Extend its left endpoint along the existing y=943 lane to approximately x=335, then turn upward and finish with a clear upward arrowhead ON the bottom boundary of Tool Inertia Graph near (335,904). Do not change the separate observation-to-current-context feedback loop or the Record trajectories arrow. These are endpoint corrections only. Preserve all other pixels as closely as possible. The full scientific specification below remains binding; these two precise connector instructions override only its previous routing choices. No new scientific mechanisms or decorative content.

'''
body=source.split('\n\n',1)[1]
body=body.replace('Use the attached approved ReAct image only as a reference for','The original approved ReAct reference supplied guidance for')
body=body.replace('via a single short arrow labeled Candidate + argument status','via the single input connector in the inter-panel gutter defined by the edit instruction')
prompt=header+body
floor=len(''.join((ROOT/'knowledge-base/cases/react/prompt.txt').read_text(encoding='utf-8').split()))
assert floor<=len(''.join(prompt.split())) and len(prompt)<=32000
target.write_bytes(prompt.encode('utf-8'))
print(json.dumps({'characters':len(prompt),'nonwhitespace':len(''.join(prompt.split())),'minimum':floor}))
