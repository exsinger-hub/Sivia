"""Fit actual tool limit by removing duplicate prose, never truncating tool input."""
from pathlib import Path
import json, re
ROOT=Path(__file__).resolve().parents[3]
PAIRS=ROOT/'knowledge-base/restart-2026/pairs'

def remove_section(s,start,end):
    a=s.index('\n'+start+'\n');b=s.index('\n'+end+'\n',a)
    return s[:a]+s[b:]

a=PAIRS/'autotool/prompt.txt'; original=a.parent/'prompt.unsubmitted-overlimit.txt'
if not original.exists(): original.write_text(a.read_text(encoding='utf-8'),encoding='utf-8')
s=original.read_text(encoding='utf-8')
s=remove_section(s,'TEXT AND SYMBOL CONTRACT','VISUAL GRAMMAR AND TYPOGRAPHY')
s='\n\n'.join(p for p in s.split('\n\n') if not p.startswith('The fallback scene still contributes meaningful visual density:'))
a.write_text(s,encoding='utf-8')

a=PAIRS/'sigmadock/prompt.txt';original=a.parent/'prompt.unsubmitted-overlimit.txt'
if not original.exists(): original.write_text(a.read_text(encoding='utf-8'),encoding='utf-8')
s=original.read_text(encoding='utf-8')
s=remove_section(s,'FR3D LOCAL DETAIL AND DUMMY ATOMS','FIXED PROTEIN POCKET')
s=remove_section(s,'CONDITIONS, MODEL OUTPUTS AND ROUTE OWNERSHIP','EXACT LABELS AND MATHEMATICAL TEXT')
# Final scientific checks repeat the already specified geometry; retain occupancy.
start=s.index('\nFINAL SCIENTIFIC AND SPATIAL CHECK\n')
keep=s.index('\nCheck meaningful occupancy',start)
s=s[:start]+'\nFINAL SPATIAL CHECK\n'+s[keep:]
paragraphs=s.split('\n\n')
prefixes=[
 'The repeated pocket scenes are not different protein candidates.',
 'The protein patch behind this local example stays fixed',
 'Maintain consistent fragment identity through the input, library',
 'If a precise chemically valid merge cannot be represented',
]
s='\n\n'.join(p for p in paragraphs if not any(p.startswith(prefix) for prefix in prefixes))
a.write_text(s,encoding='utf-8')

report=[]
for cid,anchor in [('d4rt','neuralangelo'),('autotool','react'),('sigmadock','diffdock')]:
    p=(PAIRS/cid/'prompt.txt').read_text(encoding='utf-8')
    t=(ROOT/'knowledge-base/cases'/anchor/'prompt.txt').read_text(encoding='utf-8')
    n=len(re.sub(r'\s','',p));floor=len(re.sub(r'\s','',t))
    report.append({'id':cid,'characters':len(p),'nonwhitespace':n,'floor':floor,'floor_pass':n>=floor,'tool_max_characters':32000,'tool_max_pass':len(p)<=32000})
    assert n>=floor and len(p)<=32000, report[-1]
print(json.dumps(report,indent=2))
