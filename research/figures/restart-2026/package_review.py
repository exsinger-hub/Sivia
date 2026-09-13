"""Package actual drafts, conditional retrieval records and an honest review UI."""
from pathlib import Path
import collections, hashlib, html, json, re
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[3];KB=ROOT/'knowledge-base';OUT=KB/'restart-2026'

def dump(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes((json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def largest_empty(grid):
    heights=np.zeros(grid.shape[1],dtype=int);best=0
    for row in ~grid:
        heights=np.where(row,heights+1,0);stack=[]
        for j,h in enumerate(list(heights)+[0]):
            left=j
            while stack and stack[-1][1]>h:
                pos,old=stack.pop();best=max(best,old*(j-pos));left=pos
            stack.append((left,int(h)))
    return best/grid.size
def diagnostic(p):
    im=Image.open(p).convert('RGB');a=np.asarray(im,dtype=np.int16)
    contrast=np.zeros(a.shape[:2],dtype=bool)
    contrast[1:,:]|=np.max(np.abs(a[1:]-a[:-1]),axis=2)>=28
    contrast[:,1:]|=np.max(np.abs(a[:,1:]-a[:,:-1]),axis=2)>=28
    ys=np.linspace(0,a.shape[0],41,dtype=int);xs=np.linspace(0,a.shape[1],61,dtype=int)
    grid=np.array([[contrast[ys[y]:ys[y+1],xs[x]:xs[x+1]].mean()>=.035 for x in range(60)] for y in range(40)])
    return {'size':list(im.size),'near_white_pixel_fraction':float(np.all(a>=242,axis=2).mean()),'contrast_grid_occupied_fraction':float(grid.mean()),'largest_low_contrast_rectangle_fraction':float(largest_empty(grid)),'grid':[60,40],'contrast_threshold':28,'tile_edge_fraction_threshold':.035,'role':'diagnostic only; flat fills excluded, text/borders/texture still contribute; no automatic quality/admission verdict'}

DETAILS={
 'd4rt':{'anchor':'neuralangelo','versions':3,'source_visual_review':'assistant inspected original PDF p2 Figure 2 at rendered resolution','scientific_checks':['Independent query calls remain separate and reuse F.','Five embedding summands; source patch is not a sixth summand.','Both coordinate clouds feed Umeyama, whose output is relative camera pose.'],'notes':['Small labels require full-size viewing; schematic geometry is not a measured output.'],'files':['exec-912a06cb-2a33-42f5-acd3-047149b76368.png','exec-af615861-0644-4131-8fbe-246ab8adf7ad.png','exec-1dd029f9-b1de-4389-8c3b-c20c32f765db.png'],'references':['neuralangelo/figure.png','d4rt/figure.v1.png','d4rt/figure.v2.png']},
 'autotool':{'anchor':'react','versions':6,'source_visual_review':'Official PDF method text and Figure 2 caption inspected via web; original figure raster inspection remains pending because local PDF download failed and the web screenshot tool returned a citation without a model-visible image.','scientific_checks':['Both-checks-pass and any-check-fails routes converge before shared execution.','LLM output and argument completeness no longer bypass execution to reach observation.','Parameter source value a is preserved through the example.','Candidate and argument information now reaches the enclosing decision region through a continuous gutter connector.'],'notes':['The history-to-graph maintenance line is continuous, but an extra arrowhead near Add to history makes its direction ambiguous and still needs correction.','Original source figure visual assessment is still pending.'],'files':['exec-74ef6236-6d0d-403d-9ea0-d0a38b737b21.png','exec-fdca3479-d892-4069-838e-cdf2df151966.png','exec-d783b576-135d-4e2c-944e-a2a7f95b0a89.png','exec-d5698d2b-d3e6-440e-94d6-c6cbdd1ed1e2.png','exec-6027c6ee-5e2e-422e-8848-310a300c820c.png','exec-517c319a-0f7b-4efc-ae00-c58c72d4bba4.png'],'references':['react/figure.png','autotool/figure.v1.png','react/figure.png','autotool/figure.v3.png','autotool/figure.v4.png','autotool/figure.v5.png']},
 'sigmadock':{'anchor':'diffdock','versions':4,'source_visual_review':'assistant inspected original PDF p3 Figure 1 and p6 Figure 3; read sections 2.2.3–2.4 and appendix FR3D algorithm','scientific_checks':['Protein pocket remains fixed; reverse direction is T to 0.','Local geometry uses A–C and B–D distance associations with a B–C dihedral axis.','Fragment score and reverse-step roles remain distinct; current-state dependence is labeled.'],'notes':['Small angle-label artifacts remain in the lower construction; publication typography needs another precision pass.','Generic molecular graphics were not validated as a chemical structure.'],'files':['exec-331ff9aa-d5e9-42fd-bea9-8dd37cbcaac4.png','exec-68400a8d-c3a7-4fea-b5a7-d9adde4500ca.png','exec-8861166a-c3bc-4eea-a9c8-2d31ce5dd2ba.png','exec-4371ce07-1094-4ca9-bf54-c1e853a2b906.png'],'references':['diffdock/figure.png','sigmadock/figure.v1.png','sigmadock/figure.v1.png','sigmadock/figure.v3.png']}
}

def package():
    # Each actual tool prompt was loaded as Unicode text with LF line endings.
    # Preserve that exact UTF-8 representation in files on Windows as well.
    for prompt_file in (OUT/'pairs').glob('*/prompt*.txt'):
        prompt_file.write_bytes(prompt_file.read_text(encoding='utf-8').encode('utf-8'))
    source={r['id']:r for r in json.loads((OUT/'candidates.json').read_text(encoding='utf-8'))['records']}
    records=[]
    for cid,spec in DETAILS.items():
        d=OUT/'pairs'/cid;p=d/'prompt.txt';im=d/'figure.png'
        prompt=p.read_text(encoding='utf-8');template=KB/'cases'/spec['anchor']/'prompt.txt'
        row={'id':cid,'title':source[cid]['title'],'venue':source[cid]['venue'],'year':source[cid]['year'],
             'category':source[cid]['category'],'selected_anchor':spec['anchor'],'source_url':source[cid]['official_url'],'source_pdf':source[cid]['pdf_url'],
             'source_visual_review':spec['source_visual_review'],'source_review_scope':source[cid]['review_scope'],
             'pair_status':'generated_draft_pending_review','admission':'not_admitted','user_approval':'pending','publication_allowed':False,
             'prompt':f'pairs/{cid}/prompt.txt','image':f'pairs/{cid}/figure.png','prompt_sha256':digest(p),'image_sha256':digest(im),
             'prompt_characters':len(prompt),'prompt_nonwhitespace_characters':len(re.sub(r'\s','',prompt)),
             'template':f'../cases/{spec["anchor"]}/prompt.txt','template_sha256':digest(template),'template_nonwhitespace_characters':len(''.join(template.read_text(encoding='utf-8').split())),
             'tool_max_prompt_characters':32000,'exact_production_text_saved':True,
             'generation_tool':'built-in image_gen','provider_model_id':None,'seed':None,'cost':None,
             'successful_image_calls':spec['versions'],'assistant_visual_review':'provisional; not human evaluation or admission',
             'scientific_checks':spec['scientific_checks'],'remaining_review_notes':spec['notes'],
             'density_diagnostic':diagnostic(im),'all_scientific_pixels':'generated conceptual illustration','sealed_evaluation_eligible':False}
        row['length_floor_pass']=row['prompt_nonwhitespace_characters']>=row['template_nonwhitespace_characters']
        row['tool_length_pass']=len(prompt)<=32000
        row['versions']=[]
        for i,(file,ref) in enumerate(zip(spec['files'],spec['references']),1):
            final=i==spec['versions'];pp=d/('prompt.txt' if final else f'prompt.v{i}.txt');ii=d/('figure.png' if final else f'figure.v{i}.png')
            row['versions'].append({'version':i,'prompt':pp.name,'image':ii.name,'prompt_sha256':digest(pp),'image_sha256':digest(ii),'generated_original_filename':file,'reference_image':ref,'selected_for_review':final})
        dump(d/'case.json',row);records.append(row)
        (d/'README.md').write_text(f'''# {cid} — 条件匹配试配对\n\n状态：**实际生成，待审阅；未入库、未推送**。\n\n来源：[{row['title']}]({row['source_url']})，{row['venue']} {row['year']}。匹配参考：{spec['anchor']}。\n\n![生成草图](figure.png)\n\n[完整实际提交 prompt](prompt.txt) · [版本与校验记录](case.json)\n\nPrompt：{len(prompt):,} 字符；{row['prompt_nonwhitespace_characters']:,} 非空白字符；参考下限 {row['template_nonwhitespace_characters']:,}；工具上限 32,000 字符。\n\n源图检查：{spec['source_visual_review']}\n\n检查内容：\n\n'''+''.join(f'- {x}\n' for x in spec['scientific_checks'])+'\n仍需审阅：\n\n'+''.join(f'- {x}\n' for x in spec['notes'])+'\n图片和分子/几何示例是生成的概念插图，不是实验结果，也不是人类金标准。\n',encoding='utf-8')
    dump(OUT/'pairs.json',{'schema_version':'sivia.restart.pairs.v1','actual_draft_pairs':len(records),'approved_new_pairs':0,'records':records})
    dump(OUT/'generation-summary.json',{'successful_image_calls':sum(s['versions'] for s in DETAILS.values()),'failed_calls':2,'failure_notes':['One rejected parallel AutoTool invocation did not retain its error detail.','Retry returned HTTP 400: prompt 33701 characters exceeded 32000. No image was produced.'],'actual_draft_pairs':3,'approved_new_pairs':0,'model_id':None,'cost':None,'paid_benchmark_experiments':0})
    return records

def gallery(records):
    e=html.escape;data=json.loads((OUT/'candidates.json').read_text(encoding='utf-8'))['records'];cats=json.loads((OUT/'taxonomy.json').read_text(encoding='utf-8'))['categories']
    parts=['''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sivia 条件匹配重启审阅</title><style>
*{box-sizing:border-box}body{margin:0;background:#f3f5f7;color:#192835;font:16px/1.65 system-ui,"Microsoft YaHei",sans-serif}main{max-width:1320px;margin:auto;padding:30px}h1{font-size:32px;margin:0 0 10px}h2{margin:32px 0 12px}a{color:#086d8e}header,.pair,.candidate,.rules{background:white;border:1px solid #dce3e8;border-radius:12px;padding:22px;margin-bottom:18px}.counts{display:flex;gap:12px;flex-wrap:wrap}.count{background:#eef6f6;padding:12px 18px;border-radius:8px}.count strong{font-size:25px;margin-right:8px}.muted{color:#576777}.pill{display:inline-block;background:#fff2cd;border-radius:6px;padding:2px 8px;font-size:13px;margin:3px}.pair img{width:100%;height:auto;display:block;margin-top:15px;background:#fff}.pair h2{margin:0}.meta{display:flex;gap:18px;flex-wrap:wrap}.anchor{max-width:360px!important}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:15px}.candidate{margin:0;padding:18px}.candidate h3{font-size:18px;line-height:1.4;margin:4px 0 12px}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f8fafb;padding:18px;max-height:600px;overflow:auto;font:13px/1.6 ui-monospace,monospace}summary{cursor:pointer;font-weight:600;padding:8px 0}label{margin-right:14px}select,input{font:inherit;padding:7px;border:1px solid #b8c8d1;border-radius:6px}input{min-width:260px}table{border-collapse:collapse;width:100%}td,th{padding:8px;border-bottom:1px solid #dce3e8;text-align:left}#empty{display:none}small{font-size:13px}nav{display:flex;gap:20px;margin-top:14px}@media(max-width:750px){main{padding:15px}.grid{grid-template-columns:1fr}h1{font-size:26px}input{min-width:180px}}</style><main>
<header><small>SIVIA · 2026-09-13 · LOCAL REVIEW</small><h1>从已认可案例条件匹配，重建近期论文增广集</h1><p>借鉴可解释的视觉结构，用新论文的真实机制改写；浅色底板不计作科学内容。当前页面是可审阅草稿包。</p><div class="counts"><div class="count"><strong>3</strong>已认可历史参考</div><div class="count"><strong>24</strong>近期论文候选</div><div class="count"><strong>3</strong>实际生成试配对</div><div class="count"><strong>0</strong>本轮新入库</div></div><nav><a href="#pairs">查看新图与完整 prompt</a><a href="#candidates">按六大类查看候选</a><a href="../README.md">知识库说明</a></nav></header>
<div class="rules"><b>审阅口径</b><p>近期范围按会议论文集版本：2025-09-13 至 2026-09-13；首次预印本日期尚未逐篇核对。Neuralangelo、ReAct、DiffDock 是获认可的历史参考，不计入近期新增。其余 39 对历史图退出参考池。候选论文不等于合格图，生成草图也不等于入库。</p><p>检索分数只说明标签匹配程度，不是美学分数。正式入库需要低无效空白、科学关系正确、标签可读及用户确认；推送权限仍为关闭。</p></div><h2 id="pairs">三个实际生成试配对</h2>''']
    for r in records:
        c=next(c for c in data if c['id']==r['id']);anchor=r['selected_anchor'];p=(OUT/r['prompt']).read_text(encoding='utf-8')
        parts.append(f'''<article class="pair"><h2>{e(r['id'])}</h2><span class="pill">{e(r['venue'])} {r['year']}</span><span class="pill">待审阅 · 未入库</span><p>{e(c['claim'])}</p><div class="meta"><span>匹配：<b>{anchor}</b></span><span>{r['prompt_characters']:,} 字符 / {r['prompt_nonwhitespace_characters']:,} 非空白字符</span><a href="{e(r['source_url'])}">官方论文来源</a><a href="{r['prompt']}">完整 prompt 文件</a><a href="pairs/{r['id']}/case.json">修订记录</a></div><a href="{r['image']}"><img src="{r['image']}" alt="{e(r['id'])} 新生成草图"></a><details><summary>匹配依据与仍需审阅的细节</summary><p>{e(c['conditional_matches'][0]['transfer'])}</p><p>不迁移：{e(c['do_not_transfer'])}</p><p>源图检查：{e(r['source_visual_review'])}</p><ul>{''.join('<li>'+e(n)+'</li>' for n in r['remaining_review_notes'])}</ul><p>科学密度检查以对象和关系为准；数值仅为诊断：细节网格占用 {r['density_diagnostic']['contrast_grid_occupied_fraction']:.1%}，最大连续低对比区域 {r['density_diagnostic']['largest_low_contrast_rectangle_fraction']:.1%}。边框和文字也可能产生局部边缘，不能据此自动入库。</p><img class="anchor" src="../cases/{anchor}/figure.png" alt="匹配的已认可参考"></details><details><summary>展开完整实际提交 prompt（全文）</summary><pre>{e(p)}</pre></details></article>''')
    parts.append('<h2 id="candidates">24 篇候选 · 六大类</h2><p>其中 21 篇尚未生成配对。候选的原图质量和具体方法需要在生产前逐篇审阅；弱匹配不会强行借用旧案例机制。</p><p><label>大类 <select id="category"><option value="">全部</option>'+''.join(f'<option value="{cid}">{e(label)}</option>' for cid,label in cats.items())+'</select></label><input id="search" aria-label="搜索论文" placeholder="论文名、会议或关键词"></p><div class="grid">')
    for c in data:
        match=c['conditional_matches'][0]; selected=c['selected_anchor'] or '低于匹配阈值，需要新的布局参考'
        parts.append(f'''<article class="candidate" data-category="{c['category']}" data-search="{e((c['title']+' '+c['venue']+' '+c['claim']).lower())}"><small>{e(cats[c['category']])} · {c['venue']} {c['year']}</small><h3><a href="{e(c['official_url'])}">{e(c['title'])}</a></h3><span class="pill">{'已有生成草图' if c['id'] in DETAILS else '候选，未生成'}</span><p>{e(c['claim'])}</p><p><b>匹配参考：</b>{selected} <small>（最高检索值 {match['score']:.3f}）</small></p><details><summary>布局计划与边界</summary><p>{e(c['layout'])}</p><p>{e(c['do_not_transfer'])}</p><p>{e(c['figure_review'])}</p><a href="{e(c['pdf_url'])}">官方 PDF</a></details></article>''')
    parts.append('''</div><p id="empty">没有符合条件的候选。</p><p class="muted">源论文家族、历史图及其衍生物只用于学习/开发，排除未来封闭评测。本页没有触发 GitHub 推送或入库操作。</p></main><script>const cat=document.getElementById('category'),q=document.getElementById('search');function filter(){let n=0;for(const c of document.querySelectorAll('.candidate')){const show=(!cat.value||c.dataset.category===cat.value)&&c.dataset.search.includes(q.value.trim().toLowerCase());c.hidden=!show;if(show)n++}document.getElementById('empty').style.display=n?'none':'block'}cat.addEventListener('change',filter);q.addEventListener('input',filter);</script></html>''')
    (OUT/'gallery.html').write_text(''.join(parts),encoding='utf-8')

def showcase_entries(records):
    """Choose one current image per active reference or generated review entry."""
    index=json.loads((KB/'index.json').read_text(encoding='utf-8'))
    names={'neuralangelo':'Neuralangelo','react':'ReAct','diffdock':'DiffDock',
           'd4rt':'D4RT','autotool':'AutoTool','sigmadock':'SigmaDock'}
    entries=[]
    for r in index['records']:
        entries.append({'id':r['id'],'name':names.get(r['id'],r.get('title',r['id'])),
                        'category':r['category'],'image':r['image'],'prompt':r['prompt'],
                        'details':r['readme'],'status':'approved_reference',
                        'selection_reason':'Current image bound to the user-approved reference record.'})
    seen={e['id'] for e in entries}
    for r in records:
        if r['id'] in seen:continue
        entries.append({'id':r['id'],'name':names.get(r['id'],r.get('title',r['id'])),
                        'category':r['category'],'image':'restart-2026/'+r['image'],
                        'prompt':'restart-2026/'+r['prompt'],
                        'details':f"restart-2026/pairs/{r['id']}/README.md",
                        'status':'draft_pending_review',
                        'selection_reason':'Current actual generated review image; remaining quality notes stay in case details.'})
        seen.add(r['id'])
    for entry in entries:
        for key in ['image','prompt','details']:
            if not (KB/entry[key]).is_file():raise FileNotFoundError(entry[key])
        entry['image_sha256']=digest(KB/entry['image'])
    dump(OUT/'readme-showcase.json',{'schema_version':'sivia.readme_showcase.v1',
         'selection_policy':'One current image per active or generated review entry; excluded history and ungenerated candidates are not showcase entries.',
         'entries':entries})
    return entries

def showcase_markup(entries,categories,prefix='',language='zh'):
    english=language=='en'
    category_names={
        'geometry-4d':'3D reconstruction and dynamic geometry',
        'agents-retrieval':'Agents, tools and retrieval',
        'molecular-science':'Molecular modeling and AI for Science',
        'visual-generation':'Image and video generation',
        'embodied-control':'Embodied control and world models',
        'visual-perception':'Visual understanding and spatial perception'}
    status_names={'approved_reference':'Approved reference' if english else '已认可参考',
                  'draft_pending_review':'Review draft · not admitted' if english else '待审阅草图 · 未入库'}
    links=['Full-size image','Full prompt','Case details'] if english else ['查看原图','完整 prompt','案例详情']
    title='### Image gallery' if english else '### 逐条图片展示'
    intro=('Each entry has its own current image. Click an image to inspect it at full size.' if english else
           '每个条目展示一张对应的当前图片；点击图片可查看原图。')
    parts=[title+'\n\n'+intro+'\n\n']
    for cid,label in categories.items():
        group=[entry for entry in entries if entry['category']==cid]
        if not group:continue
        parts.append('#### '+(category_names.get(cid,label) if english else label)+'\n\n<table>\n')
        for start in range(0,len(group),2):
            row=group[start:start+2]
            parts.append('<tr>\n')
            for entry in row:
                span=' colspan="2"' if len(row)==1 else ' width="50%"'
                name=html.escape(entry['name']);status=html.escape(status_names[entry['status']])
                image_url=html.escape(prefix+entry['image'],quote=True)
                prompt_url=html.escape(prefix+entry['prompt'],quote=True)
                detail_url=html.escape(prefix+entry['details'],quote=True)
                parts.append(f'<td{span} valign="top" align="center">\n<strong>{name}</strong><br>\n'
                             f'<sub>{status}</sub><br>\n'
                             f'<a href="{image_url}"><img src="{image_url}" alt="{name} — {status}" width="440"></a><br>\n'
                             f'<a href="{image_url}">{links[0]}</a> · <a href="{prompt_url}">{links[1]}</a> · '
                             f'<a href="{detail_url}">{links[2]}</a>\n</td>\n')
            parts.append('</tr>\n')
        parts.append('</table>\n\n')
    return ''.join(parts)

def readmes(records):
    candidates=json.loads((OUT/'candidates.json').read_text(encoding='utf-8'))['records'];cats=json.loads((OUT/'taxonomy.json').read_text(encoding='utf-8'))['categories']
    entries=showcase_entries(records)
    text='''# 科研绘图知识库 · 条件匹配重启版\n\n本地审阅版，尚未推送。当前有效参考池是用户认可的 **Neuralangelo、ReAct、DiffDock 3 对**；其余 **39 对**保留为历史排除项。原先“42 对全部通过”的结论只代表旧数值筛查，不能代表用户认可或科学质量。\n\n[打开图文审阅页](restart-2026/gallery.html) · [机器索引](index.json) · [SQLite 条件匹配数据库](restart-2026/conditional.sqlite) · [24 篇候选](restart-2026/candidates.json) · [历史排除项](archive/excluded-39.json)\n\n本轮已完成 3 个实际生成试配对；其余 21 篇尚未生成。新入库为 0，全部等待审阅。\n\n## 条件匹配\n\n按领域、科学对象、机制拓扑、构图形式四个维度匹配，仅检索用户认可的历史参考。默认权重 0.30 / 0.30 / 0.25 / 0.15；匹配值低于 0.5 时不自动选择参考。该值是可解释的检索启发式，不是视觉质量分数。\n\n```bash\npython scripts/restart_conditional_kb.py --query d4rt\npython scripts/validate_knowledge_base.py\n```\n\n每条记录保留借鉴内容、禁止迁移的科学内容和弱匹配提示。现有三个参考覆盖有限；弱匹配的生成、机器人等候选仍需新论文图形支持，不能强行套版。\n\n## 三个试配对\n\n| 新论文 | 匹配参考 | 完整 prompt | 状态 |\n| --- | --- | --- | --- |\n'''
    for r in records:text+=f"| [{r['id']}]({r['source_url']}) · {r['venue']} {r['year']} | {r['selected_anchor']} | [全文](restart-2026/{r['prompt']}) · {r['prompt_nonwhitespace_characters']:,} 非空白字符 | 实际草图，未入库 |\n"
    text+='\n## 六大类候选\n\n近期范围按会议论文集版本为 **2025-09-13—2026-09-13**。原始预印本首次公开日期尚未逐篇核对；历史参考不计入近期新增。下面是候选，不是已评定的优秀源图名单。\n'
    for cid,label in cats.items():
        text+=f'\n### {label}\n\n'
        for c in candidates:
            if c['category']==cid:text+=f"- [{c['title']}]({c['official_url']}) — {c['venue']} {c['year']}；{'已生成试配对' if c['id'] in DETAILS else '待源图审阅与生成'}。\n"
    text+='''\n## 入库与长度要求\n\n- 科学对象、细节和必要连线应充分占据画面；浅色底板、空框、边框和大标题不能代替有效内容。\n- 长度下限为匹配参考完整 prompt 的非空白 Unicode 字符数，接口上限为 32,000 总字符；提交前两项都检查，实际提交全文必须与保存文件一致。\n- 自动对比度网格只辅助找空白，不能判定科学正确性、图形美学或用户认可。\n- 标签、端点、对象身份及训练/推理范围需单独核对。所有草图保留修订历史和剩余问题。\n- 用户确认后才允许新条目入库和推送；当前 publication_allowed=false。不启动模型实验。\n\n源论文 PDF/网页的本地检查缓存不纳入发布包；保留官方链接和已取得的校验散列。所有已接触源论文家族和衍生物均排除未来封闭评测。生成概念图不能作为实测结果或人类金标准。\n'''
    text=text.replace('## 条件匹配\n','## 条件匹配\n\n[按新需求的条件直接查询：命令、词表与增广流程](restart-2026/retrieval-guide.md)\n')
    text=text.replace('## 条件匹配\n',showcase_markup(entries,cats)+'## 条件匹配\n',1)
    (KB/'README.md').write_text(text,encoding='utf-8')
    for filename,heading,new in [
      ('README.md','## Knowledge base','''## Knowledge base\n\nThe active reference pool has **3 user-approved historical pairs**: Neuralangelo, ReAct and DiffDock. The other 39 of the previous 42 pairs are archived as excluded references. The earlier density screen did not establish visual acceptance.\n\nThis local restart contains **24 recent main-conference candidates in six categories** and **3 actual generated calibration pairs**, all pending review; 21 candidates have not yet been generated. No new pair is admitted and nothing from this restart has been pushed. Conference-edition window: 2025-09-13 through 2026-09-13; first-preprint dates remain unverified.\n\nConditional retrieval uses domain, scientific objects, topology and composition, with explicit transfer boundaries and a no-match outcome. Browse the [review gallery](knowledge-base/restart-2026/gallery.html), [classified knowledge base](knowledge-base/README.md) or [active index](knowledge-base/index.json). Full submitted prompts, reference bindings and revision notes accompany each draft.\n\n'''),
      ('README_ZH.md','## 科研绘图知识库','''## 科研绘图知识库\n\n当前参考池仅有用户认可的 **Neuralangelo、ReAct、DiffDock 3 对**。上一版 42 对中的其余 39 对已转为历史排除项，旧空白率筛查不代表质量认可。\n\n本地重启版按六大类整理 **24 篇近期主会候选**，完成 **3 个实际生成试配对**，均待审阅；其余 21 篇尚未生成。新入库为 0，本轮尚未推送。近期口径为 2025-09-13—2026-09-13 的会议论文集版本，首次预印本日期尚未逐篇核验。\n\n条件匹配按领域、科学对象、机制拓扑、构图形式检索，记录借鉴与禁止迁移的内容，弱匹配不强行套版。查看[图文审阅页](knowledge-base/restart-2026/gallery.html)、[分类知识库](knowledge-base/README.md)和[有效索引](knowledge-base/index.json)。每张草图附完整实际提交 prompt、参考绑定及修订记录。\n\n''')]:
        p=ROOT/filename;s=p.read_text(encoding='utf-8');a=s.index(heading);b=s.index('\n## ',a+3)
        s=s[:a]+s[b+1:]
        s=re.sub(r'!\[Neuralangelo[^\]]*\]\(knowledge-base/cases/neuralangelo/figure\.png\)\n\n<p align="center">[^\n]*</p>\n\n','',s)
        new+=showcase_markup(entries,cats,prefix='knowledge-base/',language='en' if filename=='README.md' else 'zh')
        insertion='## Why Sivia?' if filename=='README.md' else '## 为什么使用 Sivia？'
        position=s.index(insertion);s=s[:position]+new+s[position:]
        p.write_text(s,encoding='utf-8')
    oldsummary=KB/'archive/generation-summary.before-restart.json'
    if not oldsummary.exists():oldsummary.write_bytes((KB/'generation-summary.json').read_bytes())
    dump(KB/'generation-summary.json',{'current':'restart-2026/generation-summary.json','historical':'archive/generation-summary.before-restart.json','note':'Historical 24-pair wave is excluded from the current reference pool except the three specifically approved anchors.'})

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--readmes-only',action='store_true');args=parser.parse_args()
    if args.readmes_only:
        records=json.loads((OUT/'pairs.json').read_text(encoding='utf-8'))['records'];readmes(records)
        print(json.dumps({'readmes_updated':['README.md','README_ZH.md','knowledge-base/README.md'],
                          'showcase_entries':len(json.loads((OUT/'readme-showcase.json').read_text(encoding='utf-8'))['entries'])}))
    else:
        records=package();gallery(records);readmes(records)
        print(json.dumps({'actual_drafts':len(records),'approved_new':0,'generated_images':sum(d['versions'] for d in DETAILS.values()),'density':{r['id']:r['density_diagnostic'] for r in records}},indent=2))
