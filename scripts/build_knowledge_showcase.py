"""Build the published README image gallery from its actual paired assets."""
from pathlib import Path
import html,json,re

ROOT=Path(__file__).resolve().parents[1]
KB=ROOT/'knowledge-base'
CATEGORIES={
    'geometry-4d':('三维重建与动态几何','3D reconstruction and dynamic geometry'),
    'agents-retrieval':('智能体、工具与检索','Agents, tools and retrieval'),
    'molecular-science':('分子建模与 AI for Science','Molecular modeling and AI for Science'),
    'visual-generation':('图像、视频生成与编辑','Image and video generation'),
    'embodied-control':('具身控制与世界模型','Embodied control and world models'),
    'visual-perception':('视觉理解、分割与空间定位','Visual understanding and spatial perception')}

def gallery(records,prefix='',english=False):
    parts=[]
    statuses={'approved_reference':'Approved reference' if english else '已认可参考',
              'draft_pending_review':'Review draft · not admitted' if english else '待审阅草图 · 未入库'}
    links=['Full-size image','Full prompt','Case details'] if english else ['查看原图','完整 prompt','案例详情']
    for category,names in CATEGORIES.items():
        rows=[r for r in records if r['category']==category]
        if not rows:continue
        parts.append('### '+names[int(english)]+'\n\n<table>\n')
        for start in range(0,len(rows),2):
            pair=rows[start:start+2];parts.append('<tr>\n')
            for r in pair:
                image=html.escape(prefix+r['image'],quote=True)
                prompt=html.escape(prefix+r['prompt'],quote=True)
                details=html.escape(prefix+r['details'],quote=True)
                name=html.escape(r['name']);status=html.escape(statuses[r['status']])
                span=' colspan="2"' if len(pair)==1 else ' width="50%"'
                parts.append(f'<td{span} valign="top" align="center">\n<strong>{name}</strong><br>\n'
                             f'<sub>{status}</sub><br>\n'
                             f'<a href="{image}"><img src="{image}" alt="{name} — {status}" width="440"></a><br>\n'
                             f'<a href="{image}">{links[0]}</a> · <a href="{prompt}">{links[1]}</a> · '
                             f'<a href="{details}">{links[2]}</a>\n</td>\n')
            parts.append('</tr>\n')
        parts.append('</table>\n\n')
    return ''.join(parts)

def build():
    records=json.loads((KB/'showcase/index.json').read_text(encoding='utf-8'))['records']
    assert len({r['id'] for r in records})==len(records)
    for r in records:
        assert r['category'] in CATEGORIES
        for key in ['image','prompt','details']:
            assert (KB/r[key]).is_file(),r[key]
    approved=sum(r['status']=='approved_reference' for r in records)
    drafts=sum(r['status']=='draft_pending_review' for r in records)
    for filename,heading,insertion,english in [
        ('README.md','## Knowledge base','## Why Sivia?',True),
        ('README_ZH.md','## 科研绘图知识库','## 为什么使用 Sivia？',False)]:
        p=ROOT/filename;s=p.read_text(encoding='utf-8')
        a=s.index(heading);b=s.index('\n## ',a+3);s=s[:a]+s[b+1:]
        s=re.sub(r'!\[[^\n]*\]\(knowledge-base/cases/[^\n]+/figure\.png\)\n\n<p align="center">[^\n]*</p>\n\n','',s)
        if english:
            intro=(f'**{len(records)} illustrated entries: {approved} approved references and {drafts} review drafts.** '
                   'Every entry displays its own image below. Click an image for the full-size version, '
                   'or open its complete production prompt and case notes.\n\n'
                   'Neuralangelo, ReAct and DiffDock are the approved historical references. '
                   'D4RT, AutoTool and SigmaDock are recent-paper augmentation drafts with review notes. '
                   'These are generated conceptual illustrations.\n\n'
                   '[Browse the classified knowledge base](knowledge-base/README.md)\n\n')
        else:
            intro=(f'**{len(records)} 个图文条目：{approved} 个已认可参考、{drafts} 个待审阅草图。** '
                   '每个条目都直接展示对应图片；点击图片可查看原图，也可打开完整生产 prompt 和案例详情。\n\n'
                   'Neuralangelo、ReAct、DiffDock 是已认可的历史参考；D4RT、AutoTool、SigmaDock 是近期论文增广草图，附有待修订说明。'
                   '图片均为生成的概念插图。\n\n'
                   '[浏览分类知识库](knowledge-base/README.md)\n\n')
        block=heading+'\n\n'+intro+gallery(records,'knowledge-base/',english)
        at=s.index(insertion);s=s[:at]+block+s[at:];p.write_text(s,encoding='utf-8')
    kbtext=('# Sivia 科研绘图知识库\n\n'
            f'当前展示 **{len(records)} 个实际图文配对**：{approved} 个已认可参考、{drafts} 个待审阅草图。'
            '每个条目各展示一张图片，并提供原图、完整 prompt、来源与修订说明。\n\n'
            '[机器可读展示清单](showcase/index.json) · [贡献图文配对](CONTRIBUTING.md)\n\n')
    kbtext+=gallery(records)
    kbtext+=('## 使用这些案例\n\n'
             '根据新论文的领域、科学对象、机制拓扑与构图需求匹配已认可参考；结合图片阅读完整 prompt，'
             '迁移布局、实体表现和局部展开方式，再依据新论文改写科学内容。待审阅草图用于观察和反馈，不自动进入已认可参考池。\n\n'
             '图像应以科学对象和必要关系充分占据画面，浅色底板、空框与大标题不能充当有效内容。'
             '标签、连线端点和公式需对照论文核验；完整 prompt 按所选参考的[长度规则](../skills/design-scientific-figure/references/imagegen-prompt-detail.md)检查。\n\n'
             '所有图均为生成的概念插图，不是实验结果。已查看的来源论文家族和衍生物排除未来封闭评测。\n\n'
             '## 历史条目\n\n'
             '早期示例保留在 [cases](cases/) 目录中供追溯，不属于当前已认可参考池。\n')
    (KB/'README.md').write_text(kbtext,encoding='utf-8')
    print(json.dumps({'readmes':3,'illustrated_entries':len(records),'approved_references':approved,'review_drafts':drafts}))

if __name__=='__main__':build()
