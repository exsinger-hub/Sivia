#!/usr/bin/env python3
"""Read-only density diagnostics and contact sheets for a knowledge wave."""
from __future__ import annotations
import argparse,hashlib,json,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter

ROOT=Path(__file__).resolve().parents[1]
KB=ROOT/'knowledge-base'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def max_empty_rectangle(occ):
    rows,cols=occ.shape; height=np.zeros(cols,dtype=int); best=0
    for y in range(rows):
        height=np.where(occ[y],0,height+1); stack=[]
        for x in range(cols+1):
            h=int(height[x]) if x<cols else 0; start=x
            while stack and stack[-1][1]>h:
                sx,sh=stack.pop(); best=max(best,sh*(x-sx)); start=sx
            if not stack or stack[-1][1]<h: stack.append((start,h))
    return best/(rows*cols)

def measure(path):
    with Image.open(path) as im: rgb=im.convert('RGB')
    arr=np.asarray(rgb,dtype=np.int16)
    near=((arr.min(2)>=245)&((arr.max(2)-arr.min(2))<=10))
    work=rgb.copy(); work.thumbnail((1200,1200),Image.Resampling.LANCZOS)
    hi=np.asarray(work.filter(ImageFilter.MaxFilter(3)),dtype=np.int16)
    lo=np.asarray(work.filter(ImageFilter.MinFilter(3)),dtype=np.int16)
    detail=(hi-lo).max(2)>=24
    warr=np.asarray(work,dtype=np.int16)
    # Whitespace screen includes pale panel fills and long borders.  The local
    # detail mask is kept separately because it intentionally undercounts them.
    content=(warr.min(2)<247)|((warr.max(2)-warr.min(2))>8)
    h,w=content.shape; cols,rows=32,20
    xs=np.linspace(round(.015*w),round(.985*w),cols+1).round().astype(int)
    ys=np.linspace(round(.03*h),round(.97*h),rows+1).round().astype(int)
    frac=np.array([[content[ys[y]:ys[y+1],xs[x]:xs[x+1]].mean() for x in range(cols)] for y in range(rows)])
    detail_frac=np.array([[detail[ys[y]:ys[y+1],xs[x]:xs[x+1]].mean() for x in range(cols)] for y in range(rows)])
    occ=frac>=.06
    empty=max_empty_rectangle(occ)
    return {'size':list(rgb.size),'sha256':sha(path),'near_white_fraction':float(near.mean()),'content_grid_fraction':float(occ.mean()),'detail_grid_fraction':float((detail_frac>=.015).mean()),'largest_empty_rectangle_fraction':float(empty),'density_screen_pass':bool(occ.mean()>=.78 and empty<=.10)}

def sheet(records,index,audit):
    thumb_w,thumb_h=720,480; label_h=42; gap=14
    canvas=Image.new('RGB',(thumb_w*2+gap*3,(thumb_h+label_h)*3+gap*4),'#d9dde3')
    d=ImageDraw.Draw(canvas)
    for j,r in enumerate(records):
        with Image.open(KB/r['image']) as im:
            im=im.convert('RGB'); im.thumbnail((thumb_w,thumb_h),Image.Resampling.LANCZOS)
            x=gap+(j%2)*(thumb_w+gap); y=gap+(j//2)*(thumb_h+label_h+gap)
            canvas.paste(im,(x+(thumb_w-im.width)//2,y))
            d.rectangle((x,y+thumb_h,x+thumb_w,y+thumb_h+label_h),fill='white')
            source_label=f"{r.get('venue','legacy')} {r.get('year','')}".strip()
            d.text((x+8,y+thumb_h+9),f"{r['id']} | {source_label} | {r['category']}",fill='black')
    canvas.save(audit/f'contact-{index:02d}.png')

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--manifest',default='paper-wave-24.json')
    ap.add_argument('--audit-name',default='paper-wave-24')
    args=ap.parse_args()
    wave=json.loads((KB/args.manifest).read_text(encoding='utf-8'))
    audit=KB/'audit'/args.audit_name
    audit.mkdir(parents=True,exist_ok=True)
    out=[]
    for r in wave['records']:
        p=KB/r['image']; out.append({**r,**measure(p)})
    for i in range(0,len(out),6): sheet(out[i:i+6],i//6+1,audit)
    report={'schema_version':'sivia.paper_knowledge.density_audit.v1','count':len(out),'method':'near-white pixels plus 32x20 meaningful-content and local-detail grids; pale panel fills and borders count as occupied for the whitespace gate; numerical screen is a triage aid, not semantic admission','thresholds':{'content_grid_fraction_min':.78,'largest_empty_rectangle_fraction_max':.10,'cell_content_fraction_min':.06},'pass_count':sum(x['density_screen_pass'] for x in out),'records':out}
    (audit/'measurements.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'count':len(out),'pass':report['pass_count'],'failed':[{'id':x['id'],'occ':round(x['content_grid_fraction'],4),'empty':round(x['largest_empty_rectangle_fraction'],4)} for x in out if not x['density_screen_pass']]},ensure_ascii=False))

if __name__=='__main__':main()
