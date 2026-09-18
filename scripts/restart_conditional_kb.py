"""Rebuild a reviewable SQLite reference pool from explicit acceptance and tags.

Scores are transparent retrieval heuristics, never image-quality or human scores.
"""
from pathlib import Path
import argparse, datetime, hashlib, json, sqlite3, sys
sys.stdout.reconfigure(encoding='utf-8')

REPO=Path(__file__).resolve().parents[1]
KB=REPO/'knowledge-base'
WORK=REPO/'research/figures/restart-2026'
APPROVED={'neuralangelo','react','diffdock'}
WEIGHTS={'domain':.30,'objects':.30,'topology':.25,'composition':.15}
MINIMUM_MATCH=.5

def write_json(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes((json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))

def overlap(query,ref):
    return len(set(query)&set(ref))/len(set(query)) if query else 0.0

def rank(case,anchors):
    result=[]
    for ref in anchors:
        parts={'domain':float(case['category']==ref['domain']),
               'objects':overlap(case['objects'],ref['objects']),
               'topology':overlap(case['topology'],ref['topology']),
               'composition':overlap(case['composition'],ref['composition'])}
        score=sum(parts[k]*w for k,w in WEIGHTS.items())
        result.append({'anchor_id':ref['id'],'score':round(score,4),'components':parts,
                       'matched':{k:sorted(set(case[k])&set(ref[k])) for k in ['objects','topology','composition']},
                       'transfer':ref['transfer'],'forbidden':ref['forbidden']})
    return sorted(result,key=lambda x:(-x['score'],x['anchor_id']))

def build():
    plan=json.loads((WORK/'conditional_plan.json').read_text(encoding='utf-8'))
    if {a['id'] for a in plan['anchors']} != APPROVED or len(plan['anchors']) != len(APPROVED):
        raise ValueError('Only the three user-approved restart anchors may enter the reference database')
    sources=json.loads((WORK/'candidates.json').read_text(encoding='utf-8'))
    for cid,number,pdfnumber,title in [
      ('autotool','40389','44350','AutoTool: Efficient Tool Selection for Large Language Model Agents'),
      ('mobile-agent-rag','40241','44202','Mobile-Agent-RAG: Driving Smart Multi-Agent Coordination with Contextual Knowledge Empowerment for Long-Horizon Mobile Automation')]:
        if cid not in {r['id'] for r in sources['records']}:
            sources['records'].append({'id':cid,'title':title,'category':'agents-retrieval','venue':'AAAI','year':2026,
               'official_url':f'https://ojs.aaai.org/index.php/AAAI/article/view/{number}',
               'pdf_url':f'https://ojs.aaai.org/index.php/AAAI/article/view/{number}/{pdfnumber}',
               'official_date_metadata':['2026-03-14'],'official_page_sha256':None,
               'evidence_transport':'web tool read official page and PDF; requests HTML download failed',
               'main_track_verification':'AAAI-26 Technical Tracks; official OJS page Section field',
               'preprint_first_date':None,'pair_status':'candidate_only','user_approval':'pending','publication_allowed':False})
    sources['errors']=[]
    sources['retrieval_notes']=['AAAI official evidence verified via web tool; local HTML hashes unavailable.']
    write_json(WORK/'candidates.json',sources)
    source_by_id={s['id']:s for s in sources['records']}
    cards=[]
    for c in plan['cases']:
        card=source_by_id[c['id']]|c
        card['recency_basis']='Conference proceedings edition, not first arXiv posting'
        card['recency_window']=sources['window']
        card['conference_window_eligible']=card['venue'] in ['CVPR','ICLR','AAAI'] and card['year']==2026 or card['venue']=='NeurIPS' and card['year']==2025
        card['recency_precision']='AAAI exact issue publication date' if card['venue']=='AAAI' else 'conference edition; day not asserted'
        card['figure_review']='assistant source-figure review recorded' if 'review_scope' in c else 'pending method and visual inspection'
        matches=rank(card,plan['anchors'])
        card['conditional_matches']=matches
        card['selected_anchor']=matches[0]['anchor_id'] if matches[0]['score']>=.5 else None
        card['match_strength']='domain-and-structure' if matches[0]['components']['domain'] else 'partial-visual-grammar'
        card['weak_match_requires_source_specific_layout']=matches[0]['components']['domain']==0
        card['pair_status']='candidate_only'
        card['user_approval']='pending'
        card['admission']='not_admitted'
        card['publication_allowed']=False
        card['sealed_evaluation_eligible']=False
        pair_meta=KB/'restart-2026/pairs'/card['id']/'case.json'
        if pair_meta.exists():
            p=json.loads(pair_meta.read_text(encoding='utf-8'))
            card['pair_status']=p['pair_status']
            card['pair_metadata']=f"restart-2026/pairs/{card['id']}/case.json"
            card['source_visual_review']=p['source_visual_review']
            card['figure_review']=p['source_visual_review']
        cards.append(card)
    write_json(KB/'restart-2026/candidates.json',{'schema_version':'sivia.restart.candidates.v1','records':cards})
    write_json(KB/'restart-2026/taxonomy.json',{'categories':plan['categories'],'axes':['category','objects','topology','composition'],'retrieval_weights':{'domain':.30,'objects':.30,'topology':.25,'composition':.15},'minimum_match':.5,'score_role':'retrieval heuristic; not a quality score'})
    old_archive=KB/'archive/index.before-restart-2026.json'
    if not old_archive.exists():
        write_json(old_archive,json.loads((KB/'index.json').read_text(encoding='utf-8')))
    old=json.loads(old_archive.read_text(encoding='utf-8'))
    anchor_by_id={a['id']:a for a in plan['anchors']}
    active=[];excluded=[]
    for r in old['records']:
        r=r.copy()
        r['historical_density_not_acceptance']=r.pop('density',None)
        r.pop('manual_visual_review',None)
        r['admission']='user_approved_legacy_anchor' if r['id'] in APPROVED else 'excluded_by_user_restart'
        r['eligible_reference']=r['id'] in APPROVED
        r['recent_year_new_pair']=False
        r['user_feedback_date']='2026-09-13'
        if r['id'] in APPROVED:
            r['historical_category']=r.get('category')
            r['category']=anchor_by_id[r['id']]['domain']
            r['conditional_tags']={key:anchor_by_id[r['id']][key] for key in ['objects','topology','composition']}
            if 'admission_basis' in r:
                r['historical_admission_basis']=r.pop('admission_basis')
        (active if r['id'] in APPROVED else excluded).append(r)
    write_json(KB/'archive/excluded-39.json',{'reason':'User accepted only Neuralangelo, ReAct, DiffDock on restart; prior numerical density screening was insufficient.','records':excluded})
    write_json(KB/'index.json',{'schema_version':'sivia.knowledge_base.index.v3','total_pairs':len(active),'active_reference_pairs':len(active),'historical_pairs':len(old['records']),'excluded_historical_pairs':len(excluded),'recent_source_candidates':len(cards),'new_generated_draft_pairs':sum(c['pair_status']=='generated_draft_pending_review' for c in cards),'new_approved_pairs':0,'restart_status':'local_review_pending_user_confirmation','publication_allowed':False,'categories':plan['categories'],'records':active,'candidate_manifest':'restart-2026/candidates.json','archive_manifest':'archive/excluded-39.json'})
    dbpath=KB/'restart-2026/conditional.sqlite'
    db=sqlite3.connect(dbpath)
    # This generated database contains only our own derived index tables.
    db.executescript('DROP TABLE IF EXISTS anchors; DROP TABLE IF EXISTS candidates; DROP TABLE IF EXISTS matches; CREATE TABLE anchors (id TEXT PRIMARY KEY, approval TEXT NOT NULL CHECK(approval="user_approved"), domain TEXT NOT NULL, metadata TEXT NOT NULL); CREATE TABLE candidates (id TEXT PRIMARY KEY, category TEXT NOT NULL, eligible INTEGER NOT NULL, status TEXT NOT NULL, metadata TEXT NOT NULL); CREATE TABLE matches (candidate_id TEXT NOT NULL REFERENCES candidates(id), anchor_id TEXT NOT NULL REFERENCES anchors(id), score REAL NOT NULL, details TEXT NOT NULL, PRIMARY KEY(candidate_id,anchor_id));')
    for a in plan['anchors']: db.execute('INSERT INTO anchors VALUES (?,?,?,?)',(a['id'],'user_approved',a['domain'],json.dumps(a,ensure_ascii=False)))
    for c in cards:
        db.execute('INSERT INTO candidates VALUES (?,?,?,?,?)',(c['id'],c['category'],int(c['conference_window_eligible']),c['pair_status'],json.dumps(c,ensure_ascii=False)))
        for m in c['conditional_matches']: db.execute('INSERT INTO matches VALUES (?,?,?,?)',(c['id'],m['anchor_id'],m['score'],json.dumps(m,ensure_ascii=False)))
    db.commit()
    assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    assert db.execute('SELECT count(*) FROM anchors').fetchone()[0]==3
    assert len(cards)==24 and len(excluded)==39
    assert all(c['conference_window_eligible'] for c in cards)
    db.close()
    exclusions=json.loads((KB/'evaluation-exclusions.json').read_text(encoding='utf-8'))
    exclusions['case_ids']=sorted(set(exclusions['case_ids'])|{c['id'] for c in cards}|{r['id'] for r in old['records']})
    exclusions['restart_note']='Rejected history remains excluded from sealed evaluation; rejection does not undo exposure.'
    write_json(KB/'evaluation-exclusions.json',exclusions)
    print(json.dumps({'anchors':len(active),'excluded':len(excluded),'candidates':len(cards),'sqlite_integrity':'ok','matches':[(c['id'],c['selected_anchor'],c['conditional_matches'][0]['score']) for c in cards]},ensure_ascii=False))

def open_readonly():
    return sqlite3.connect((KB/'restart-2026/conditional.sqlite').as_uri()+'?mode=ro',uri=True)

def query(cid):
    db=open_readonly()
    rows=db.execute('SELECT m.details FROM matches m JOIN anchors a ON a.id=m.anchor_id JOIN candidates c ON c.id=m.candidate_id WHERE c.id=? AND c.eligible=1 AND a.approval=? ORDER BY m.score DESC,m.anchor_id',(cid,'user_approved')).fetchall()
    matches=[json.loads(x[0]) for x in rows]
    selected=matches[0]['anchor_id'] if matches and matches[0]['score']>=.5 else None
    print(json.dumps({'candidate_id':cid,'selected_anchor':selected,'minimum_match':.5,'status':'matched' if selected else 'no_eligible_match','score_role':'retrieval heuristic, not a quality score','matches':matches},ensure_ascii=False,indent=2))
    db.close()

def query_conditions(category,objects,topology,composition):
    """Rank existing approved references for a new, explicitly tagged brief.

    No candidate is created and no source or image is admitted by this operation.
    Missing axes contribute zero instead of inflating partial-condition matches.
    """
    split=lambda value: sorted({x.strip() for x in (value or '').split(',') if x.strip()})
    conditions={'category':category,'objects':split(objects),'topology':split(topology),'composition':split(composition)}
    with open_readonly() as db:
    anchors=[json.loads(row[0]) for row in db.execute('SELECT metadata FROM anchors WHERE approval=?',('user_approved',))]
    # The published index may contain the three legacy anchors plus explicitly
    # approved recent overview pairs. Query all eligible references in that
    # index; the build path still protects the original review-plan contract.
    published = json.loads((KB/'index.json').read_text(encoding='utf-8'))
    allowed={r['id'] for r in published['records'] if r.get('eligible_reference')}
    anchors=[a for a in anchors if a['id'] in allowed]
    matches=rank(conditions,anchors)
    selected=matches[0]['anchor_id'] if matches and matches[0]['score']>=MINIMUM_MATCH else None
    print(json.dumps({'conditions':conditions,'selected_anchor':selected,'minimum_match':MINIMUM_MATCH,
       'status':'matched' if selected else 'no_eligible_match',
       'score_role':'retrieval heuristic, not a quality score; missing axes contribute zero',
       'source_eligibility':'not assessed by tag retrieval; verify a recent main-conference source before augmentation',
       'reference_files':{'prompt':f'cases/{selected}/prompt.txt','image':f'cases/{selected}/figure.png'} if selected else None,
       'matches':matches},ensure_ascii=False,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--query',help='Query an existing source candidate by id')
    p.add_argument('--category',help='New brief category, such as agents-retrieval')
    for key in ['objects','topology','composition']:
        p.add_argument('--'+key,help='Comma-separated tags from the conditional taxonomy')
    args=p.parse_args()
    has_conditions=any(getattr(args,k) is not None for k in ['category','objects','topology','composition'])
    if args.query and has_conditions:
        p.error('Use either --query or new-brief condition flags, not both')
    if args.query:
        query(args.query)
    elif has_conditions:
        query_conditions(args.category,args.objects,args.topology,args.composition)
    else:
        build()
