import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

// This stage freezes a backend-neutral handoff. It does not create a slide.
const dir = path.dirname(fileURLToPath(import.meta.url));
const objects = [];
const palette = { ink:'26363D', secondary:'52636A', teal:'12635F', tealLight:'EAF3F0', rust:'9B4D32', rustLight:'FAF0EB', neutral:'F2F5F6', rule:'A6B4B9', white:'FFFFFF' };
function shape(name,type,bounds,fill,line='ink',width=0.8,level='L1',extra={}) {
  objects.push({name,kind:'shape',type,bounds,fill:palette[fill]??fill,line:palette[line]??line,width,level,...extra});
}
function text(name,value,bounds,size=8,color='ink',bold=false,level='L1',extra={}) {
  objects.push({name,kind:'text',text:value,bounds,size,color:palette[color]??color,bold,level,...extra});
}
function line(name,points,color='ink',width=1.1,arrow=true,level='L1',extra={}) {
  objects.push({name,kind:'line',points,color:palette[color]??color,width,arrow,level,...extra});
}

// Exact geometry is in mm. All font sizes are physical point sizes at 170 mm.
text('figure_title','Evidence-gated retrieval agent',[4,2.7,113,6.4],13,'ink',true,'title');
text('frozen_weights','All model weights frozen',[119,3.5,47,5],8,'ink',true,'L2',{align:'right'});
text('evidence_boundary','Retrieved text is evidence.\nNever instructions or weight updates.',[4,12,60,9],7.4,'secondary',false,'L2');

shape('question',5,[4,31,18,12],'white');
text('question_label','User\nquestion',[5,32.2,16,9],8.5,'ink',false,'L1',{align:'center'});
shape('retrieve',1,[29,31,24,12],'neutral');
text('retrieve_label','Retrieve',[30,34,22,6],9,'ink',true,'L1',{align:'center'});
shape('draft',16,[61,30,24,14],'white');
text('draft_label','Draft / revise',[62,34,21,6],8.5,'ink',false,'L1',{align:'center'});
shape('source_spans',16,[69,12,27,9],'tealLight','teal',0.75,'L2');
text('source_spans_label','Source spans',[70,14,24,5],8,'teal',false,'L2',{align:'center'});

// A native claim-to-span comparison, with a check mark as the focal mechanism.
shape('evidence_gate',9,[96,26,22,22],'teal','teal',1.0);
text('gate_label','Evidence check',[96.8,19,30,5],10,'teal',true);
shape('gate_claim_strip',1,[99.1,30.4,12.7,4.3],'white','white',0);
text('gate_claim_text','claim',[100,30.55,11,3.9],7.5,'teal',true,'L1',{align:'center'});
shape('gate_span_strip',1,[99.1,40,12.7,4.3],'white','white',0);
text('gate_span_text','span',[100,40.1,11,3.9],7.5,'teal',true,'L1',{align:'center'});
line('glyph_claim_span_link',[[102,34.9],[102,39.5]],'white',0.8,false);
line('glyph_check_short',[[106.2,36.2],[108.7,38.5]],'white',1.8,false);
line('glyph_check_long',[[108.7,38.5],[113.6,33.6]],'white',1.8,false);

shape('supported_answer',67,[143,29,23,15],'tealLight','teal',0.9);
text('answer_label','Answer\n+ citations',[144,31,21,9],8.6,'teal',true,'L1',{align:'center'});
shape('abstain',6,[143,48,23,10],'rustLight','rust',0.9);
text('abstain_label','Abstain',[145,50,19,6],8.6,'rust',true,'L1',{align:'center'});

// The main spine and evidence route use real connected native connectors.
line('question_to_retrieve',[[22,37],[29,37]],'ink',1.1,true,'L1',{attachStart:{name:'question',site:4},attachEnd:{name:'retrieve',site:2}});
line('passages_to_draft',[[53,37],[61,37]],'ink',1.1,true,'L1',{attachStart:{name:'retrieve',site:4},attachEnd:{name:'draft',site:2}});
line('claims_to_gate',[[85,37],[96,37]],'ink',1.1,true,'L1',{attachStart:{name:'draft',site:4},attachEnd:{name:'evidence_gate',site:3}});
line('retrieve_to_spans',[[41,31],[41,23],[82.5,23],[82.5,21]],'teal',0.8,true,'L2',{semantics:'data',prominence:'secondary'});
line('spans_to_gate',[[96,16.5],[128,16.5],[128,25],[107,25],[107,26]],'teal',0.8,true,'L2',{semantics:'data',prominence:'secondary',endpoint:'top of evidence_gate at x=107,y=26; route clears the label'});
line('supported_branch',[[118,37],[143,37]],'teal',1.1,true,'L1',{attachStart:{name:'evidence_gate',site:7}});
text('supported_condition','All cited claims\nsupported',[120.1,28.1,22,8],7.2,'teal',false,'L2',{align:'center'});

line('unsupported_stem',[[107,48],[107,53]],'rust',1.1,false,'L2');
shape('unsupported_junction',9,[106.4,52.4,1.2,1.2],'rust','rust',0,'L2');
line('retry_branch',[[107,53],[41,53],[41,43]],'rust',1.1,true,'L2',{semantics:'feedback',prominence:'primary'});
line('abstain_branch',[[107,53],[143,53]],'rust',1.1,true,'L2',{semantics:'control',prominence:'primary'});
text('retry_condition','Unsupported, attempt < 3',[47,47.7,49,4.5],7.5,'rust',false,'L2');
text('retry_action','Retrieve more evidence, then revise',[46.5,54.3,58,4.5],7.3,'rust',false,'L2');
text('abstain_condition','Unsupported\nat attempt 3',[117,44.2,25,8],7.2,'rust',false,'L2',{align:'center'});

// Paired a/b references link the expanded operations to their main groups.
text('detail_ref_a','a',[50,27,3,3.6],7.2,'secondary',false,'L3',{italic:true});
text('detail_ref_b_draft','b',[82,26,3,3.6],7.2,'secondary',false,'L3',{italic:true});
text('detail_ref_b_gate','b',[124.8,17.5,3,3.6],7.2,'secondary',false,'L3',{italic:true});
line('detail_separator_a',[[4,61],[80,61]],'rule',0.45,false,'L3');
line('detail_separator_b',[[89,61],[166,61]],'rule',0.45,false,'L3');
text('detail_a_heading','a  Retrieval',[4,62,76,4.4],8,'ink',true,'L3');
text('detail_a_prepare','Prepare: chunk → embed → index',[4,67,76,4.2],7.5,'secondary',false,'L3');
text('detail_a_online','Online: index lookup → rerank → passages',[4,72,76,4.2],7.5,'secondary',false,'L3');
text('detail_b_heading','b  Drafting and checking',[89,62,77,4.4],8,'ink',true,'L3');
text('detail_b_draft','Assemble prompt → generate → parse claims',[89,67,77,4.2],7.5,'secondary',false,'L3');
text('detail_b_check','Each cited claim + source span → support check',[89,72,77,4.2],7.5,'secondary',false,'L3');

const brief = {
  B1:'An LLM retrieval agent takes a user question, retrieves passages, and drafts an answer.',
  B2:'Checks each cited claim against source spans; retrieves more evidence and revises if unsupported (at most three attempts); returns a supported answer with citations or abstains.',
  B3:'Index preparation includes chunking and embedding; online includes index lookup and reranking, prompt assembly, generation and claim parsing; logging is an implementation detail.',
  B4:'Retrieved content is evidence, never an instruction or weight update. All weights frozen.',
  B5:'Main claim: evidence checking controls revision and abstention. No experimental data or numerical performance claims.',
  B6:'Single-slide editable overview, 170 mm wide × 80 mm high, with linked detail explanation.'
};
const nodeMap = [
  ['question','question','direct','L1',null,'B1'],
  ['retrieve','retrieve','direct','L1','detail_a_heading','B1'],
  ['passages','source_spans','grouped','L2','detail_a_online','B1'],
  ['draft_or_revise','draft','direct','L1','detail_b_heading','B1/B2'],
  ['source_spans','source_spans','direct','L2','detail_b_check','B2'],
  ['support_check','evidence_gate','direct','L1','detail_b_check','B2'],
  ['supported_answer_with_citations','supported_answer','direct','L1',null,'B2'],
  ['abstain','abstain','direct','L1',null,'B2'],
  ['chunk','retrieve','grouped','L3','detail_a_prepare','B3'],
  ['embed','retrieve','grouped','L3','detail_a_prepare','B3'],
  ['index','retrieve','grouped','L3','detail_a_prepare/detail_a_online','B3'],
  ['index_lookup','retrieve','grouped','L3','detail_a_online','B3'],
  ['rerank','retrieve','grouped','L3','detail_a_online','B3'],
  ['prompt_assembly','draft','grouped','L3','detail_b_draft','B3'],
  ['generation','draft','grouped','L3','detail_b_draft','B3'],
  ['claim_parsing','draft','grouped','L3','detail_b_draft','B3'],
  ['cited_claim','gate_claim_strip','direct','L1','detail_b_check','B2'],
  ['attempt_counter','retry_condition/abstain_condition','textual','L2','detail.md#attempts','B2'],
  ['frozen_weights','frozen_weights','textual','L2',null,'B4'],
  ['logging',null,'permitted_omission','L3','detail.md#logging','B3']
].map(([contract_id,visual_id,mode,level,expansion,source_ref])=>({contract_id,visual_id,mode,level,expansion,source_ref, ...(mode==='permitted_omission'?{reason:'The brief classifies logging as an implementation detail; it has no evidence-checking or control role.'}:{})}));
function edge(id,source,target,semantics,prominence,mode,visual_id,level,source_ref,extra={}) {
  return {id,source,target,semantics,prominence,mode,visual_id,must_survive_at:level,source_ref,...extra};
}
const edges = [
  edge('E01','question','retrieve','data','primary','direct','question_to_retrieve','L1','B1'),
  edge('E02','retrieve','draft_or_revise','data','primary','direct','passages_to_draft','L1','B1',{payload:'retrieved passages'}),
  edge('E03','retrieve','source_spans','data','secondary','direct','retrieve_to_spans','L2','B2'),
  edge('E04','source_spans','support_check','data','secondary','direct','spans_to_gate','L2','B2',{payload:'source spans, retained provenance'}),
  edge('E05','draft_or_revise','support_check','data','primary','grouped','claims_to_gate','L1','B2/B3',{expansion:'detail_b_draft',payload:'parsed cited claims and source references'}),
  edge('E06','support_check','supported_answer_with_citations','control','primary','direct','supported_branch','L2','B2',{condition:'all cited claims supported',label:'supported_condition'}),
  edge('E07','support_check','retrieve','feedback','primary','direct','unsupported_stem/retry_branch','L2','B2',{condition:'unsupported and attempt < 3',label:'retry_condition/retry_action',route_lane:'y=53 mm; return at x=41 mm'}),
  edge('E08','support_check','abstain','control','primary','direct','unsupported_stem/abstain_branch','L2','B2',{condition:'unsupported and attempt = 3',label:'abstain_condition'}),
  edge('E09','chunk','embed','transform','secondary','grouped','detail_a_prepare','L3','B3',{composite:'retrieve'}),
  edge('E10','embed','index','data','secondary','grouped','detail_a_prepare','L3','B3',{composite:'retrieve'}),
  edge('E11','index','index_lookup','data','secondary','grouped','detail_a_prepare/detail_a_online','L3','B3',{composite:'retrieve',expansion:'detail.md#retrieval'}),
  edge('E12','index_lookup','rerank','data','secondary','grouped','detail_a_online','L3','B3',{composite:'retrieve'}),
  edge('E13','rerank','passages','data','secondary','grouped','detail_a_online','L3','B3',{composite:'retrieve'}),
  edge('E14','passages','prompt_assembly','data','secondary','grouped','passages_to_draft','L1','B1/B3',{composite:'draft',expansion:'detail.md#drafting'}),
  edge('E15','question','prompt_assembly','data','secondary','grouped','question_to_retrieve/passages_to_draft','L1','B1',{composite:'question-conditioned online pipeline',expansion:'detail.md#drafting',invariant:'The user question remains part of the task context along the main spine.'}),
  edge('E16','prompt_assembly','generation','data','secondary','grouped','detail_b_draft','L3','B3',{composite:'draft'}),
  edge('E17','generation','claim_parsing','data','secondary','grouped','detail_b_draft','L3','B3',{composite:'draft'}),
  edge('E18','claim_parsing','cited_claim','transform','secondary','grouped','detail_b_draft','L3','B3',{composite:'draft'}),
  edge('E19','cited_claim','support_check','data','primary','direct','gate_claim_strip/glyph_claim_span_link/glyph_check_long','L1','B2',{expansion:'detail_b_check'}),
  edge('E20','retrieved_content','instruction_authority','prohibited','secondary','textual','evidence_boundary','L2','B4',{invariant:'Retrieved text is never an instruction.'}),
  edge('E21','retrieved_content','weight_update','prohibited','secondary','textual','evidence_boundary/frozen_weights','L2','B4',{invariant:'No model weights change.'}),
  edge('E22','unsupported_retry','draft_or_revise','feedback','primary','grouped','retry_branch/passages_to_draft','L2','B2',{expansion:'detail.md#attempts',invariant:'Additional retrieval precedes revision, followed by a new check.'}),
  edge('A01','retrieve','retrieval_expansion','association','secondary','textual','detail_ref_a/detail_a_heading','L3','B6',{convention:'paired a labels, no arrowhead'}),
  edge('A02','draft_or_revise/support_check','checking_expansion','association','secondary','textual','detail_ref_b_draft/detail_ref_b_gate/detail_b_heading','L3','B6',{convention:'paired b labels, no arrowhead'})
];
const spec = {
  artifact_mode:'publication', figure_archetype:'directed spine with bounded feedback', source:brief, source_attribution:'synthetic regression brief defined for this plugin test (B1–B6)',
  figure_claim:'Evidence checking controls revision and abstention.',
  audience:'Researchers reading an LLM retrieval-agent method overview.',
  canvas:{width_mm:170,height_mm:80,publication_width_mm:170,effective_font_formula:'source_font_pt * 170 / 170',main_font_pt:8.5,secondary_min_pt:7.2,usable_bounds_mm:[4,2.7,162,74]},
  assumptions:['At most three attempts means one initial draft/check and at most two further draft/check cycles.','The brief specifies cited-claim support; no stronger truth, completeness or checker-accuracy guarantee is added.'],
  narrative_map:{first_glance:'A user question leads to a draft whose evidence check decides answer, retry or abstention.',working_understanding:'Retrieved source spans enter the checker independently. Unsupported drafts return for evidence and revision only while an attempt remains.',technical_inspection:'Linked a/b expansions preserve offline preparation and online order; detail.md defines interfaces and attempt counting.',reading_logic:'left-to-right spine plus short return loop',entry:'question',focal_region:'evidence_gate',exit:['supported_answer','abstain'],levels:{L1:['question','retrieve','draft','evidence_gate','supported_answer','abstain'],L2:['source_spans','evidence_boundary','frozen_weights','supported_condition','retry_condition','retry_action','abstain_condition'],L3:objects.filter(o=>o.level==='L3').map(o=>o.name)},mandatory_visible_cues:['spans_to_gate','supported_condition','retry_condition','abstain_condition','evidence_boundary','frozen_weights'],regions:[{id:'main',bounds_mm:[4,12,162,46.8],question:'How does checking determine the outcome?'},{id:'detail_a',bounds_mm:[4,61,76,15.2],question:'What is prepared, and what runs online?'},{id:'detail_b',bounds_mm:[89,61,77,15.2],question:'What enters the checker, and how is it produced?'}]},
  abstraction_map:{nodes:nodeMap,edges},
  visual_grammar_receipt:{claim_in_one_sentence:'Evidence checking controls revision and abstention.',primary_reading_spine:'Question → retrieval → draft/revise → check → cited answer; lower retry and abstain split.',entry_and_exit:'Left input, right pair of outcomes.',dominant_focal_zone:'22 mm dark teal disc containing separate editable claim and span strips linked by a check.',hierarchy_levels:'L1 mechanism and outcome; L2 evidence/scope/conditions; L3 operational expansions.',role_to_shape_mapping:{input:'small rounded entry',operator:'square-edged rectangle',draft_state:'folded page',source_evidence:'folded source-span strip',focal_mechanism:'native disc plus claim/span/check composite',supported_output:'document silhouette',abstention:'octagonal terminal',scope:'unboxed note'},connector_prominence_levels:{primary:'1.1 pt, dark ink/teal/rust; directed data or control',secondary:'0.8 pt, source evidence route; paired letters for detail associations'},typography_roles:{title:'Arial 13 pt bold',focal:'Arial 10 pt bold',main:'Arial 8.5–9 pt',detail:'Arial 7.5–8 pt',condition:'Arial 7.2–7.5 pt'},semantic_palette:palette,grayscale_plan:'Disc remains the darkest mass; branch text and separate routes retain semantics after hue removal.',meaningful_content_hull:[4,2.7,162,73.5],whitespace_functions:[{bounds_mm:[54,22,35,6],role:'hierarchy',purpose:'Separate the raised evidence path from online processing.'},{bounds_mm:[89,25,7,22],role:'focal_protection',purpose:'Keep the checker silhouette isolated from the draft.'},{bounds_mm:[41,48,66,9],role:'connector_lane',purpose:'Reserve the bounded retry route and its labels.'},{bounds_mm:[4,58.8,162,2.2],role:'grouping',purpose:'Separate main argument and expansions.'}],evidence_role:'Source spans are schematic inputs. No empirical outputs or measurements are supplied.',expressive_layer_if_any:'None; all glyphs have a scientific role.',forbidden_motifs:['equal-weight card wall','shadows/gradients','full-width policy footer','color-only branching','decorative icons'],reference_firewall:{allowed:['synthetic regression brief defined for this plugin test (B1–B6)','requested YOFO instructions'],external_visual_references:[],forbidden_transfer:['other agents findings','main conversation judgments','source-specific topology','result values'],note:'No external paper image or template is used; semantic grammar comes from the requested instructions.'},review_sizes:{native_mm:[170,80],powerpoint_export_px:[2040,960],screen_review_px:[850,400]}},
  style_dna:{skeleton:'directed spine with raised evidence input and local lower feedback fork',focal_strategy:'high-contrast claim/span glyph, distinct from operator and output silhouettes',visual_mass:'checker dominates native filled shapes; source evidence is a smaller raised operand',line_behavior:'two prominence weights with condition labels; connected main edges and explicit segmented routed edges',whitespace:'reserved routes and separation between scientific abstraction levels',depth:'flat, no shadows'},
  silhouette_exploration:{file:'silhouettes.svg',chosen:'spine',alternatives:[{id:'spine',reason:'Fits the wide slot, keeps distinct left entry and right outcomes, and gives the checker the dominant mass.'},{id:'radial',reason_not_selected:'Spends the short vertical dimension on outcomes and makes the operational expansion less readable.'}]},
  geometry_tokens:{outer_margin_mm:4,main_baseline_y_mm:37,return_lane_y_mm:53,detail_top_y_mm:61,main_stroke_pt:1.1,evidence_stroke_pt:0.8,annotation_stroke_pt:0.45},
  editability:{raster_count:0,raster_declarations:[],native_families:['text','autoshape','connector','line'],grouping:'Stable object names keep all primitive elements individually editable. Multi-segment routes have shared edge-name prefixes.',connector_limit:'Straight main connectors are attached. Multi-segment routes are native line segments with fixed waypoints, so rerouting is required after node movement.'},
  evidence_budget:{experimental_data_available:false,experimental_visual_mass:0,reason:'Architecture-only brief supplies no measurements. Source-span and draft glyphs are conceptual operands, not experimental results.'},
  construction_order:['main glyphs and labels','evidence route','decision branches and conditions','linked details','renderer export'],objects,
  review:{independent_reviewer:'pending; separate fresh reviewer to be assigned by the main agent',self_score:null,required_exports:['full','title-hidden','title-and-L3-hidden','grayscale of actual title-and-L3-hidden export','grayscale of actual title-hidden full-density export'],construction_checks:[{detect:'Unsupported native geometry or COM export failure',action:'Repair native object construction or report target rendering pending.'},{detect:'Text bound exceeds its allocated box',action:'Rewrite or recompose the affected box at the declared font size.'},{detect:'Review deletion removes a live connector endpoint',action:'Keep the semantic endpoint and remove annotation-only objects.'},{detect:'Missing branch condition or scope label in reduced copy',action:'Remove the object from the L3 set and regenerate fresh copies.'}]}
};
fs.writeFileSync(path.join(dir,'design-spec.json'),JSON.stringify(spec,null,2)+'\n');
fs.writeFileSync(path.join(dir,'review-plan.json'),JSON.stringify({slide:1,title_names:['figure_title'],detail_names:objects.filter(o=>o.level==='L3').map(o=>o.name),publication_width_mm:170},null,2)+'\n');
// Only a coarse composition study, never used as target-renderer evidence.
fs.writeFileSync(path.join(dir,'silhouettes.svg'),`<svg xmlns="http://www.w3.org/2000/svg" width="850" height="460" viewBox="0 0 850 460"><rect width="850" height="460" fill="white"/><g fill="#777" stroke="#777" stroke-width="4"><rect x="25" y="80" width="55" height="30"/><rect x="125" y="80" width="65" height="30"/><rect x="235" y="80" width="65" height="30"/><circle cx="375" cy="95" r="40" fill="#222"/><rect x="480" y="62" width="75" height="32"/><rect x="480" y="138" width="75" height="25"/><path d="M80 95H335 M415 95H480 M375 135V157H157V110" fill="none"/><rect x="25" y="185" width="220" height="12" fill="#bbb"/><rect x="320" y="185" width="235" height="12" fill="#bbb"/></g><g fill="#777" stroke="#777" stroke-width="4" transform="translate(50,235)"><rect x="20" y="55" width="50" height="30"/><path d="M70 70H155 M235 70H365 M200 30V5 M200 110V145" fill="none"/><circle cx="195" cy="70" r="40" fill="#222"/><rect x="155" y="-10" width="80" height="20"/><rect x="365" y="55" width="75" height="30"/><rect x="155" y="145" width="80" height="22"/></g><g font-family="Arial" font-size="18" fill="#26363D"><text x="25" y="30">Spine: selected</text><text x="25" y="260">Radial: not selected</text></g></svg>`);
console.log(JSON.stringify({handoff:path.join(dir,'design-spec.json'),objects:objects.length,title_names:1,L3_names:objects.filter(o=>o.level==='L3').length}));
