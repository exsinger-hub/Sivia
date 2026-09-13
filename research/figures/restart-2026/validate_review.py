from pathlib import Path
import hashlib, json, subprocess, sys
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[3];KB=ROOT/'knowledge-base';OUT=KB/'restart-2026'
soup=BeautifulSoup((OUT/'gallery.html').read_text(encoding='utf-8'),'html.parser')
assert len(soup.select('.pair'))==3
assert len(soup.select('.candidate'))==24
assert len(soup.select('#category option'))==7
links=[]
for a in soup.select('[href],img[src]'):
    u=a.get('href') or a.get('src')
    if not u.startswith(('http://','https://','#')):
        p=(OUT/u).resolve();assert p.is_relative_to(ROOT)
        assert p.is_file(),u
        links.append(u)
assert len(soup.select('.pair details pre'))==3
for card,record in zip(soup.select('.pair'),json.loads((OUT/'pairs.json').read_text(encoding='utf-8'))['records']):
    assert card.select_one('pre').get_text()==(OUT/record['prompt']).read_text(encoding='utf-8')
def query(cid):
    return json.loads(subprocess.check_output([sys.executable,'-X','utf8',str(ROOT/'scripts/restart_conditional_kb.py'),'--query',cid],encoding='utf-8'))
assert query('d4rt')['selected_anchor']=='neuralangelo'
assert query('sigmadock')['selected_anchor']=='diffdock'
assert query('autotool')['selected_anchor']=='react'
assert query('thinkgen')['selected_anchor'] is None
assert query('unknown-candidate')['status']=='no_eligible_match'
database_hash=hashlib.sha256((OUT/'conditional.sqlite').read_bytes()).hexdigest()
def condition_query(*args):
    return json.loads(subprocess.check_output([sys.executable,'-X','utf8',str(ROOT/'scripts/restart_conditional_kb.py'),*args],encoding='utf-8'))
assert condition_query('--category','agents-retrieval','--objects','tool,graph,text','--topology','feedback,conditional_branch','--composition','flow_loop,local_detail')['selected_anchor']=='react'
assert condition_query('--category','geometry-4d','--objects','camera,point_cloud','--topology','geometric_transform','--composition','dense_3d,local_detail')['selected_anchor']=='neuralangelo'
assert condition_query('--category','molecular-science','--objects','protein,molecule','--topology','diffusion,conditioning','--composition','dense_3d,object_sequence')['selected_anchor']=='diffdock'
assert condition_query('--category','unseen-domain','--objects','unseen-object','--topology','unseen-relation','--composition','unseen-layout')['selected_anchor'] is None
assert condition_query('--objects','tool')['selected_anchor'] is None
bad=subprocess.run([sys.executable,str(ROOT/'scripts/restart_conditional_kb.py'),'--query','d4rt','--category','geometry-4d'],capture_output=True,text=True)
assert bad.returncode==2
assert hashlib.sha256((OUT/'conditional.sqlite').read_bytes()).hexdigest()==database_hash
before=hashlib.sha256((KB/'index.json').read_bytes()).hexdigest()
p=subprocess.run([sys.executable,str(ROOT/'scripts/finalize_knowledge_base.py')],capture_output=True,text=True)
assert p.returncode!=0 and 'user-rejected entries' in (p.stdout+p.stderr)
assert hashlib.sha256((KB/'index.json').read_bytes()).hexdigest()==before
print(json.dumps({'valid':True,'html_pairs':3,'html_candidates':24,'local_links_verified':len(links),'full_prompt_embeds_exact':3,'retrieval_positive_negative_checks':11,'condition_queries_preserve_database_bytes':True,'legacy_finalizer_cannot_restore_rejected_pool':True,'browser_rendering':'not executed: file URL blocked by Browser Use policy'},indent=2))
