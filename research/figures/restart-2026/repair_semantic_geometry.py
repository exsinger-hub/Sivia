from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
PAIRS=ROOT/'knowledge-base/restart-2026/pairs'

a=PAIRS/'sigmadock'
s=(a/'prompt.v1.txt').read_text(encoding='utf-8')
s=s.replace('Use the attached approved DiffDock illustration as a visual reference','Use the historical approved DiffDock illustration as a visual reference')
s='\n\n'.join(p for p in s.split('\n\n') if not p.startswith('The scope is a mechanism illustration,') and not p.startswith('The pocket is known and fixed in this method setting.'))
header='''EDIT THE ATTACHED SIGMADOCK DRAFT LOCALLY. Preserve the dense molecular composition and all three protein scenes. Correct the top Reverse diffusion annotation to ONE arrow from t=T at LEFT toward t=0 at RIGHT; delete the left-facing arrowhead. In the local update block, change the operation label to “Reverse step” with the small second line “uses z_t”; its current-state dependence must be explicit without adding a long crossing wire. Redraw the two lower triangle subpanels completely as clean enlarged 3D geometric constructions with exactly FOUR labeled physical vertices A, B, C, D in each. Remove the extra unlabeled purple vertex and all dangling terminal atoms from these local geometry drawings. Use solid A–B, B–C, C–D bonds; the ONLY orange dashed distance edge is A–C and the ONLY violet dashed edge is B–D. In the current draft d_AC incorrectly reaches D: remove that line and draw A–C with unmistakable endpoints. Likewise replace the current d_BD line with B–D. Put the labels A, B, C, D right next to their own vertices. Draw triangle ABC in pale amber and triangle BCD in pale violet, sharing the solid B–C hinge edge. Their visible shared edge is exactly B–C. At the second subpanel keep A, B and C fixed, rotate D around B–C and show a faint prior D only as a ghost. Preserve the same two diagonal endpoint identities. The dihedral arc surrounds B–C. Use large simple spheres and sticks in these two panels so every endpoint can be inspected; do not add decorative molecular side branches there. The attached SigmaDock image is the edit target, and the following is the full scientific specification.\n\n'''
(a/'prompt.txt').write_text(header+s,encoding='utf-8')

# AutoTool: change failed long-route layout to a local explicit decision inset.
a=PAIRS/'autotool';s=(a/'prompt.v1.txt').read_text(encoding='utf-8')
start=s.index('\nCANVAS AND HIERARCHY\n');end=s.index('\nTASK CONTEXT AND HISTORY\n',start)
layout='''\nCANVAS AND HIERARCHY\n
Use a compact 16:10 landscape white canvas. The figure is a mechanism board with four adjacent occupied scenes. Left 32 percent: task context, trajectory snippets and a large hierarchical Tool Inertia Graph. Center 37 percent: the two score operands, CIPS candidate selection and the detailed parameter-source hierarchy. Right 31 percent: a large TWO-ROW decision inset above a concrete tool execution and author-network return scene. A narrow bottom lane carries observation back to current context. Keep all labels and objects inside 2 percent outer margins. Dense graph nodes, value tokens and author-network objects fill their regions; avoid background-only occupancy. Title AutoTool is modest and scientific content begins immediately below it.

The right decision inset replaces all long cross-panel decision branches. Row one says “Both checks pass” and shows a complete tool+arguments card leading DIRECTLY to one shared Execute tool block. Row two says “Any check fails” and shows Context -> LLM -> complete tool+arguments card leading to the SAME Execute tool block. The two complete calls meet at one short junction immediately above Execute tool. Within this inset the paths are short and locally traceable. There are no No/Yes wires crossing from center to the old lower-left LLM block; the LLM exists only in row two. The center's score and parameter stages have static labeled outcomes and feed this local inset via a single short arrow labeled Candidate + argument status. Draw NO Record execution card in the right column. Observation below the author-network display is the sole source of the bottom Next decision feedback. A small separate record-to-graph maintenance arrow may remain at the left graph edge, with no loop into any argument gate.
'''
s=s[:start]+layout+s[end:]
start=s.index('\nLLM FALLBACK AS A REAL ALTERNATIVE PATH\n');end=s.index('\nEXECUTION, ENVIRONMENT AND OBSERVATION\n',start)
llm='''\nLOCAL FALLBACK IN THE DECISION INSET\n
The LLM route exists only in the second row of the compact right-side decision inset. It receives goal, observation and available-tool descriptions as context, and outputs a complete tool call. Its local condition is Any check fails. The first row bypasses the LLM only under Both checks pass. These checks refer to candidate score above threshold AND all required arguments known. The two rows each terminate at the same shared execution entry. Use the row labels to establish control conditions rather than long branching wires across the graph. The inset contains exactly one LLM block and one shared Execute tool block. The LLM output is not an observation; observations are produced only after the tool interacts with the environment.
'''
s=s[:start]+llm+s[end:]
# Long branch prose from prior failed composition is replaced, not retained as conflicting guidance.
start=s.index('\nFINAL ROUTING AND MEANINGFUL OCCUPANCY\n')
s=s[:start]+'''\nFINAL ROUTING AND MEANINGFUL OCCUPANCY\n
Check the right decision inset locally: Both checks pass -> complete inertial call -> Execute tool. Any check fails -> Context -> LLM -> complete call -> the same Execute tool. Then Execute tool -> author-network environment -> Observation -> Next decision. No arrow from argument completeness may enter Observation, graph records or the next-decision lane. No LLM output may skip execution. Keep the graph and parameter hierarchy large and populated; make the two decision rows readable through short arrows and their explicit conditions. Render this full dense conceptual mechanism board with no performance numbers.
'''
s=s.replace('The first decision gate sits immediately below v*.','A static decision-condition annotation sits immediately below v*.')
start=s.index('Use a compact diamond or rounded decision lozenge with CIPS(v*)')
end=s.index('\n\nArrange the graph-to-frequency',start)
s=s[:start]+'''Use the compact label CIPS(v*) > θ_inertial. A short downward arrow labeled Candidate found reaches the parameter detail. An adjacent static note Otherwise: LLM names the alternative, which is drawn fully in the right decision inset. No long No branch leaves this region. Parameter completeness remains a second required condition before direct execution.\n'''+s[end:]
start=s.index('The second gate is immediately after this collector')
end=s.index('\n\nLOCAL FALLBACK',start)
s=s[:start]+'''The collector is followed by the compact static condition All required args filled. The example author ID a is complete. Use a short labeled output Candidate + argument status to the right decision inset. Both checks pass permits direct execution; any check fails selects the LLM row. These alternatives are drawn only in that local inset. Do not draw a second long Yes/No branch around the bottom of the figure.\n'''+s[end:]
s='\n\n'.join(p for p in s.split('\n\n') if not p.startswith('Label the region LLM fallback') and not p.startswith('At the collector show a short required-argument checklist'))
header='''NEW AUTOTOOL COMPOSITION FROM THE SCIENTIFIC SPECIFICATION BELOW. The attached ReAct image is a visual style reference only. Create a fresh mechanism board; do not reproduce the previous AutoTool long-route drafts. The control logic must be carried by a compact two-row decision inset with local arrows: Both checks pass -> complete inertial call -> shared Execute tool; Any check fails -> Context -> LLM -> complete call -> the same Execute tool. This inset is the only location of the LLM and execution-choice routes. The Tool Inertia Graph and parameter provenance scenes remain concrete and large. Do not draw any Record execution card on the right or any argument-gate arrow into observation.\n\n'''
(a/'prompt.txt').write_text(header+s,encoding='utf-8')
for cid,anchor in [('autotool','react'),('sigmadock','diffdock')]:
    p=(PAIRS/cid/'prompt.txt').read_text(encoding='utf-8');t=(ROOT/'knowledge-base/cases'/anchor/'prompt.txt').read_text(encoding='utf-8')
    assert len(p)<=32000,(cid,len(p))
    assert len(''.join(p.split()))>=len(''.join(t.split())),(cid,len(''.join(p.split())))
    print(cid,len(p),len(''.join(p.split())))
