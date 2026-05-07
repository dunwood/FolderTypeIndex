#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse, json, os, sys
from pathlib import Path
from datetime import datetime

SKIP_DIRS = {'.git','node_modules','.next','.open-next','dist','build','out','.cache','venv','.venv','__pycache__','.wrangler','.vercel','.idea','.vscode'}
SKIP_EXTS = {'.pyc','.pyo','.pyd','.so','.dll','.exe','.bin'}
RULES = [
    ('操作指南',['guide','指南','教程','操作','说明','manual','howto','readme','使用','入门'],['.md','.txt','.docx','.pdf']),
    ('部署资料',['deploy','部署','vercel','cloudflare','wrangler','docker','dockerfile','compose','nginx','dns'],['.md','.txt','.json','.yaml','.yml','.toml']),
    ('文献资料',['paper','论文','文献','reference','research','arxiv','citation'],['.pdf','.md','.docx','.bib']),
    ('实验数据',['data','dataset','实验','测试','样本','sample','eval','benchmark','result','metrics'],['.csv','.xlsx','.json','.jsonl','.parquet','.db']),
    ('Prompt资料',['prompt','提示词','agent','persona','role','角色','workflow','工作流'],['.md','.txt','.json','.yaml']),
    ('日志',['log','logs','日志','记录','debug','trace','error'],['.log','.txt','.md','.json']),
]
DEFAULT_CAT = '其他资料'

def norm(p): return str(Path(p)).lower()
def get_proj(root,fp): r=Path(fp).relative_to(root);p=[x for x in r.parts if x];return p[0] if p else 'unknown'
def match_cat(fn,fp,pd):
    nl,pl,pdl=fn.lower(),fp.lower(),pd.lower()
    for cat,kws,exts in RULES:
        if any(nl==e.lower() or nl.endswith(e.lower()) for e in exts):
            if any(k.lower() in nl or k.lower() in pl or k.lower() in pdl for k in kws): return cat
    return DEFAULT_CAT
def skip_dir(d): return d.lower() in {x.lower() for x in SKIP_DIRS}
def skip_file(f): return any(f.lower().endswith(e.lower()) for e in SKIP_EXTS)
def is_self(root,fp,pn):
    fpl=norm(fp)
    for p in [norm(os.path.join(root,pn,x)) for x in ['.git','index_data.json','folder_type_index_import.json']]:
        if fpl.startswith(p): return True
    return False

def scan(root,maxf,dry):
    rp=Path(root).resolve();items=[];stats={'total':0,'by_cat':{},'skip':0};seen=set()
    print('[扫描]',rp,'max=',maxf,'dry=',dry)
    for dp,dns,fns in os.walk(rp):
        dns[:]=[d for d in dns if not skip_dir(d)]
        if is_self(root,dp,'FolderTypeIndex'): continue
        for fn in fns:
            if stats['total']>=maxf: print('[扫描] 已达限制',maxf); break
            if skip_file(fn): stats['skip']+=1; continue
            fp=os.path.join(dp,fn);fpn=norm(fp)
            if fpn in seen: continue
            seen.add(fpn)
            if is_self(root,fp,'FolderTypeIndex'): stats['skip']+=1; continue
            cat=match_cat(fn,fp,os.path.basename(dp));proj=get_proj(root,fp)
            rel=Path(fp).relative_to(rp);subs=[p for p in rel.parts[1:-1] if p]
            tp=[cat,proj]+subs;nt='文件链接';note=cat+'-'+proj
            items.append({'tree_path':tp,'name':fn,'type':nt,'path':str(Path(fp).resolve()),'url':'','note':note})
            stats['total']+=1;stats['by_cat'][cat]=stats['by_cat'].get(cat,0)+1
            if dry and stats['total']%100==0: print('[dry]',stats['total'],'...')
    return items,stats

def gen_json(items,out):
    o={'version':1,'generated_at':datetime.now().isoformat(),'items':items}
    op=Path(out);op.parent.mkdir(parents=True,exist_ok=True)
    op.write_text(json.dumps(o,ensure_ascii=False,indent=2),encoding='utf-8')
    print('[输出]',op.resolve())

def prstats(s,dry):
    m='[dry-run]' if dry else '[生成]'
    print('',m,'完成: 总=',s['total'],', 跳过=',s['skip'])
    print('  分类:')
    for c,n in sorted(s['by_cat'].items(),key=lambda x:-x[1]): print('   ',c+':',n)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',default=r'D:\AI Project')
    ap.add_argument('--out',default='folder_type_index_import.json')
    ap.add_argument('--dry-run',action='store_true')
    ap.add_argument('--max-files',type=int,default=5000)
    args=ap.parse_args()
    if not os.path.isdir(args.root): print('[错误]',args.root,file=sys.stderr);sys.exit(1)
    items,stats=scan(args.root,args.max_files,args.dry_run)
    prstats(stats,args.dry_run)
    if not args.dry_run: 
        gen_json(items,args.out)
        print('', '[提示] 用 GUI 导入:',Path(args.out).resolve())
    else: print('', '[dry-run] 未写入')
    print('', '[安全] 仅读取元信息，未修改文件')
    print('[安全] 勿提交含真实路径的 JSON')
    return 0
if __name__=='__main__': sys.exit(main())
