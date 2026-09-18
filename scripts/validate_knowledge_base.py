"""Validate acceptance isolation, exact pair provenance and retrieval invariants."""
import collections, hashlib, json, sqlite3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];KB=ROOT/'knowledge-base'
errors=[];checks=0
def check(ok,message):
    global checks
    checks+=1
    if not ok:errors.append(message)
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
idx=read(KB/'index.json');active=idx['records']
legacy_ids={'neuralangelo','react','diffdock'}
recent_ids={'cvpr25-vggt','cvpr25-megasam','iclr25-reviwo','cvpr25-robospatial','cvpr25-people-places-cameras','cvpr25-motion-aware-video-mllm','cvpr25-dense-sfm'}
check(idx['schema_version']=='sivia.knowledge_base.index.v3','index schema')
check({r['id'] for r in active}==legacy_ids|recent_ids,'reference pool differs from user acceptance')
check(idx['total_pairs']==len(active)==10,'active count')
check(idx['publication_allowed'] is True,'publication permission')
excluded=read(KB/'archive/excluded-39.json')['records']
check(len(excluded)==39 and all(not r['eligible_reference'] for r in excluded),'rejected history eligibility')
check(not ({r['id'] for r in active}&{r['id'] for r in excluded}),'active/archive overlap')
for r in active:
    check(r['category'] in idx['categories'],'active category outside restart taxonomy '+r['id'])
    for key,hkey in [('prompt','prompt_sha256'),('image','image_sha256')]:
        p=KB/r[key];check(p.exists(),f'missing {p}')
        if p.exists():check(sha(p)==r[hkey],f'anchor {key} hash mismatch: {r["id"]}')
    if r['id'] in legacy_ids:
        check(r['admission']=='user_approved_legacy_anchor' and r['recent_year_new_pair'] is False,f'legacy status {r["id"]}')
    else:
        check(r['admission']=='user_approved_recent_overview' and r['recent_year_new_pair'] is True and r['pair_status']=='approved_and_published',f'recent status {r["id"]}')
        check(r['id'] in recent_ids and r['category'].startswith('recent-'),'recent category '+r['id'])
cards=read(KB/'restart-2026/candidates.json')['records'];pairs=read(KB/'restart-2026/pairs.json')['records']
check(len(cards)==24 and len({r['id'] for r in cards})==24,'candidate count or duplicate')
check(set(collections.Counter(c['category'] for c in cards).values())=={4},'category balance')
check(len({c['category'] for c in cards})==6,'six categories')
check(len(pairs)==3==idx['new_generated_draft_pairs'],'actual draft count')
check(idx['new_approved_pairs']==len(recent_ids),'new approval count')
excluded_eval=set(read(KB/'evaluation-exclusions.json')['case_ids'])
for c in cards:
    check(c['conference_window_eligible'] and c['official_url'].startswith('https://'),'source eligibility '+c['id'])
    check(c['admission']=='not_admitted' and c['user_approval']=='pending' and not c['publication_allowed'],'candidate admission '+c['id'])
    check(c['id'] in excluded_eval,'evaluation exclusion '+c['id'])
    best=c['conditional_matches'][0]
    check(c['selected_anchor']==(best['anchor_id'] if best['score']>=.5 else None),'no-match threshold '+c['id'])
for r in pairs:
    p=KB/'restart-2026'/r['prompt'];im=KB/'restart-2026'/r['image']
    check(p.is_file() and im.is_file(),'missing actual pair '+r['id'])
    if not(p.is_file() and im.is_file()):continue
    s=p.read_text(encoding='utf-8');n=sum(not x.isspace() for x in s)
    check(p.read_bytes()==s.encode('utf-8'),'exact UTF-8 LF tool text '+r['id'])
    check(sha(p)==r['prompt_sha256'] and sha(im)==r['image_sha256'],'pair hash '+r['id'])
    check(im.read_bytes().startswith(b'\x89PNG\r\n\x1a\n'),'PNG signature '+r['id'])
    check(len(s)==r['prompt_characters']<=32000,'tool maximum '+r['id'])
    check(n==r['prompt_nonwhitespace_characters']>=r['template_nonwhitespace_characters'],'length floor '+r['id'])
    check(r['pair_status']=='generated_draft_pending_review' and not r['publication_allowed'],'draft admission '+r['id'])
    for v in r['versions']:
        vp=p.parent/v['prompt'];vi=p.parent/v['image']
        check(vp.is_file() and vi.is_file(),'missing version '+r['id'])
        if vp.exists() and vi.exists():check(sha(vp)==v['prompt_sha256'] and sha(vi)==v['image_sha256'],'version hash '+r['id'])
db=sqlite3.connect(KB/'restart-2026/conditional.sqlite')
check(db.execute('PRAGMA integrity_check').fetchone()[0]=='ok','SQLite integrity')
check(db.execute('PRAGMA foreign_key_check').fetchall()==[],'SQLite foreign keys')
check({r[0] for r in db.execute('SELECT id FROM anchors')}=={r['id'] for r in active},'SQLite active pool')
check(dict(db.execute('SELECT id,domain FROM anchors'))=={r['id']:r['category'] for r in active},'SQLite/index category alignment')
check(db.execute('SELECT count(*) FROM candidates').fetchone()[0]==24,'SQLite candidates')
check(db.execute('SELECT count(*) FROM matches').fetchone()[0]==240,'SQLite matching rows')
check(db.execute("SELECT count(*) FROM candidates WHERE status='generated_draft_pending_review'").fetchone()[0]==3,'SQLite actual drafts')
db.close()
report={'valid':not errors,'checks':checks,'errors':errors,'active_legacy':3,'active_recent':len(recent_ids),'excluded_history':39,'candidates':24,'actual_drafts':3,'new_admitted':len(recent_ids),'publication_allowed':True,'scope':'structural/provenance validation only, not visual acceptance'}
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
