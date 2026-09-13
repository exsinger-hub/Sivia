"""Collect official main-track candidates; candidate does not mean accepted image."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urljoin
import hashlib, json
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
CVF = 'https://openaccess.thecvf.com/content/CVPR2026/html/'
ICLR = 'https://proceedings.iclr.cc/paper_files/paper/2026/hash/'
NEURIPS = 'https://proceedings.neurips.cc/paper_files/paper/2025/hash/'
SUFFIX = '-Abstract-Conference.html'
ROWS = [
 ('d4rt','geometry-4d','CVPR',2026,CVF+'Zhang_Efficiently_Reconstructing_Dynamic_Scenes_One_D4RT_at_a_Time_CVPR_2026_paper.html'),
 ('fuser','geometry-4d','CVPR',2026,CVF+'Jiang_FUSER_Feed-Forward_Multiview_3D_Registration_Transformer_and_SE3N_Diffusion_Refinement_CVPR_2026_paper.html'),
 ('4dpm','geometry-4d','CVPR',2026,CVF+'Mazur_4D_Primitive-Mache_Glueing_Primitives_for_Persistent_4D_Scene_Reconstruction_CVPR_2026_paper.html'),
 ('superfrusta','geometry-4d','CVPR',2026,CVF+'Ganeshan_Residual_Primitive_Fitting_of_3D_Shapes_with_SuperFrusta_CVPR_2026_paper.html'),
 ('autotool','agents-retrieval','AAAI',2026,'https://ojs.aaai.org/index.php/AAAI/article/view/40389'),
 ('mobile-agent-rag','agents-retrieval','AAAI',2026,'https://ojs.aaai.org/index.php/AAAI/article/view/40241'),
 ('ai-researcher','agents-retrieval','NeurIPS',2025,NEURIPS+'0d904d300a105809a2114d727851e759'+SUFFIX),
 ('mle-search','agents-retrieval','NeurIPS',2025,NEURIPS+'328b81881da145412f2bc56c998dfb6a'+SUFFIX),
 ('sigmadock','molecular-science','ICLR',2026,ICLR+'4c1516dc8f1643c94d164a436ce8fe51'+SUFFIX),
 ('star-md','molecular-science','ICLR',2026,ICLR+'f1f2ecd9db4c1faaa2ba9c716dc3e413'+SUFFIX),
 ('demodiff','molecular-science','ICLR',2026,ICLR+'a6b41bed7b8c1abfcf34591d7ae13424'+SUFFIX),
 ('dynapharm','molecular-science','NeurIPS',2025,NEURIPS+'027af285dc29d3388002c2d223ab1772'+SUFFIX),
 ('thinkgen','visual-generation','CVPR',2026,CVF+'Jiao_ThinkGen_Generalized_Thinking_for_Visual_Generation_CVPR_2026_paper.html'),
 ('dynavid','visual-generation','CVPR',2026,CVF+'Jin_Learning_to_Generate_Highly_Dynamic_Videos_using_Synthetic_Motion_Data_CVPR_2026_paper.html'),
 ('seeu','visual-generation','CVPR',2026,CVF+'Yuan_SeeU_Seeing_the_Unseen_World_via_4D_Dynamics-aware_Generation_CVPR_2026_paper.html'),
 ('ar-rag','visual-generation','NeurIPS',2025,NEURIPS+'294fe7aabe8f67e8aca8c0eab2bcfbc4'+SUFFIX),
 ('cosmos-policy','embodied-control','ICLR',2026,ICLR+'748becc400a57c0e31cfe6a2e7951467'+SUFFIX),
 ('worldgym','embodied-control','ICLR',2026,ICLR+'7f5e909ac0324db03506b380c695ffaf'+SUFFIX),
 ('memer','embodied-control','ICLR',2026,ICLR+'9da515b1ad19d032a7398f00f5ff9b0c'+SUFFIX),
 ('pcd','embodied-control','ICLR',2026,ICLR+'b6d67c380f8bde2adc4247d0036c0c73'+SUFFIX),
 ('seggraph','visual-perception','NeurIPS',2025,NEURIPS+'13388efc819c09564c66ab2dc8463809'+SUFFIX),
 ('roborefer','visual-perception','NeurIPS',2025,NEURIPS+'29416b66c2149872b9d1415a3fd2c5e0'+SUFFIX),
 ('ms-temba','visual-perception','CVPR',2026,CVF+'Sinha_MS-Temba_Multi-Scale_Temporal_Mamba_for_Understanding_Long_Untrimmed_Videos_CVPR_2026_paper.html'),
 ('soft-boundaries','visual-perception','CVPR',2026,CVF+'Zhang_Guardians_of_the_Hair_Rescuing_Soft_Boundaries_in_Depth_Stereo_CVPR_2026_paper.html'),
]

def collect(row):
    cid,category,venue,year,url=row
    d=ROOT/'sources'/cid; d.mkdir(parents=True,exist_ok=True)
    response=requests.get(url,timeout=45); response.raise_for_status()
    (d/'official.html').write_bytes(response.content)
    soup=BeautifulSoup(response.content,'html.parser')
    meta=soup.find('meta',attrs={'name':'citation_title'})
    title=meta.get('content') if meta else None
    if not title:
        node=soup.select_one('#papertitle') or soup.find('h1') or soup.find('h4')
        title=node.get_text(' ',strip=True) if node else soup.title.get_text(' ',strip=True)
    links=[(a.get_text(' ',strip=True).lower(),urljoin(url,a['href'])) for a in soup.select('a[href]')]
    pdf=next((u for t,u in links if t in ('pdf','[pdf]','paper') and ('pdf' in u or '/article/view/' in u)),None)
    pdfmeta=soup.find('meta',attrs={'name':'citation_pdf_url'})
    if pdfmeta: pdf=pdfmeta.get('content')
    abstract=soup.select_one('#abstract') or soup.select_one('.abstract')
    text=soup.get_text('\n',strip=True)
    (d/'official.txt').write_text(text,encoding='utf-8')
    dates=[x.get('content') for x in soup.find_all('meta',attrs={'name':'citation_publication_date'})]
    return {'id':cid,'title':title,'category':category,'venue':venue,'year':year,'official_url':url,
            'pdf_url':pdf,'official_page_sha256':hashlib.sha256(response.content).hexdigest(),
            'official_date_metadata':dates,'abstract':abstract.get_text(' ',strip=True) if abstract else None,
            'main_track_verification':'official proceedings page; track text retained',
            'recency_basis':'main-conference proceedings edition within 2025-09-13..2026-09-13',
            'preprint_first_date':None,'source_figure_review':'pending','pair_status':'candidate_only',
            'user_approval':'pending','publication_allowed':False}

if __name__=='__main__':
    out=[]; errors=[]
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures={pool.submit(collect,x):x[0] for x in ROWS}
        for f in as_completed(futures):
            try:
                x=f.result();out.append(x);print(x['id'],x['title'],flush=True)
            except Exception as e:
                errors.append({'id':futures[f],'error':str(e)});print('ERROR',futures[f],str(e),flush=True)
    out.sort(key=lambda r:[x[0] for x in ROWS].index(r['id']))
    (ROOT/'candidates.json').write_text(json.dumps({'window':['2025-09-13','2026-09-13'],'records':out,'errors':errors},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'collected':len(out),'errors':errors}))
