"""Cache primary PDFs for local inspection. Downloads are not redistribution assets."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import json, hashlib, requests, fitz
from collect_sources import collect, ROWS, ROOT

def get_pdf(r):
    d=ROOT/'sources'/r['id']; p=d/'paper.pdf'
    if not p.exists():
        response=requests.get(r['pdf_url'],timeout=90)
        response.raise_for_status()
        if not response.content.startswith(b'%PDF'): raise ValueError('not a PDF response')
        p.write_bytes(response.content)
    doc=fitz.open(p)
    pages=[page.get_text() for page in doc]
    (d/'paper.txt').write_text('\n'.join(f'\n--- PAGE {i+1} ---\n{t}' for i,t in enumerate(pages)),encoding='utf-8')
    hits=[i+1 for i,t in enumerate(pages) if any(x in t.lower() for x in ('figure 1:','figure 2:','figure 3:','fig. 1.','fig. 2.','fig. 3.'))]
    return {'id':r['id'],'pages':len(doc),'pdf_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'figure_pages':hits}

if __name__=='__main__':
    path=ROOT/'candidates.json'; data=json.loads(path.read_text(encoding='utf-8'))
    ids={r['id'] for r in data['records']}
    for row in ROWS:
        if row[0] not in ids:
            try:
                r=collect(row);data['records'].append(r);print('added',row[0],flush=True)
            except Exception as e: print('metadata-error',row[0],str(e),flush=True)
    data['records'].sort(key=lambda r:[x[0] for x in ROWS].index(r['id']))
    data['errors']=[x for x in data['errors'] if x['id'] not in {r['id'] for r in data['records']}]
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    out=[];errors=[]
    with ThreadPoolExecutor(max_workers=6) as pool:
        jobs={pool.submit(get_pdf,r):r['id'] for r in data['records']}
        for f in as_completed(jobs):
            try:
                r=f.result();out.append(r);print(json.dumps(r),flush=True)
            except Exception as e: errors.append({'id':jobs[f],'error':str(e)});print('pdf-error',jobs[f],str(e),flush=True)
    (ROOT/'pdf-inspection.json').write_text(json.dumps({'downloaded':out,'errors':errors},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
