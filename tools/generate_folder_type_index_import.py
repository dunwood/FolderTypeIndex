#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse, fnmatch, json, os, sys
from pathlib import Path
from datetime import datetime

# ============ 过滤配置 ============
SKIP_DIRS = {'.git','node_modules','.next','.open-next','dist','build','out','.cache','venv','.venv','__pycache__','.wrangler','.vercel','.idea','.vscode','.pytest_cache','.mypy_cache'}

# 源码扩展名 - 默认排除 (除非在特殊目录)
SRC_EXTS = {'.py','.js','.jsx','.ts','.tsx','.css','.scss','.sass','.html','.htm','.java','.c','.cpp','.h','.hpp','.cs','.go','.rs','.php','.rb','.swift','.kt','.m','.mm','.vue','.svelte','.sh','.bash','.bat','.cmd','.ps1'}

# 锁文件/开发配置 - 默认排除 (部署配置除外)
LOCK_DEV_FILES = {'package-lock.json','pnpm-lock.yaml','yarn.lock','tsconfig.json','jsconfig.json','eslint.config.js','eslint.config.mjs','.prettierrc','.prettierignore','.gitignore','.gitattributes','.editorconfig','pyproject.toml','setup.cfg','requirements.txt','Pipfile','Pipfile.lock','poetry.lock','Cargo.toml','Cargo.lock','go.mod','go.sum','Makefile','makefile','CMakeLists.txt','*.sln','*.csproj','*.vcxproj'}

# 部署相关配置 - 应保留并归入部署资料  
DEPLOY_FILES = {'dockerfile','docker-compose.yml','compose.yml','compose.yaml','wrangler.toml','vercel.json','netlify.toml','railway.json','nginx.conf','procfile','fly.toml','render.yaml'}

# 常见文档扩展名 - 可进入其他资料  
DOC_EXTS = {'.md','.txt','.pdf','.docx','.doc','.pptx','.ppt','.xlsx','.xls','.csv','.jsonl','.bib','.epub','.mobi'}

# 资料价值目录名 (命中则保留)
DOC_DIRS = {'docs','doc','documentation','notes','note','knowledge','materials','material','resources','resource','references','reference','papers','paper','research','prompts','prompt','data','dataset','datasets','logs','log','reports','report','tasks','task','guides','guide','manual','tutorials','tutorial','examples','example','specs','spec'}

# 资料价值关键词 (文件名命中则保留)
DOC_KEYWORDS = ['summary','总结','记录','notes','note','report','报告','方案','设计','plan','规划','spec','需求','requirement','analysis','分析','复盘','review','readme','changelog','contributing','license','agents','claude']

# 特殊保留文件 (无论位置都保留)
SPECIAL_FILES = {'readme.md','contributing.md','changelog.md','license','license.md','agents.md','claude.md','claude.txt'}

# 分类规则: (分类名, 关键词列表, 扩展名列表)
RULES = [
    ('操作指南',['guide','指南','教程','操作','说明','manual','howto','readme','使用','入门','install','setup','配置'],['.md','.txt','.docx','.pdf','.rst']),
    ('部署资料',['deploy','部署','vercel','cloudflare','wrangler','docker','dockerfile','compose','nginx','域名','dns','worker','pages'],['.md','.txt','.json','.yaml','.yml','.toml']),
    ('文献资料',['paper','论文','文献','reference','references','article','research','arxiv','citation'],['.pdf','.md','.docx','.bib','.tex']),
    ('实验数据',['data','dataset','datasets','实验','测试','样本','sample','eval','benchmark','result','metrics','统计'],['.csv','.xlsx','.json','.jsonl','.parquet','.db']),
    ('Prompt资料',['prompt','提示词','agent','persona','role','角色','workflow','工作流'],['.md','.txt','.json','.yaml']),
    ('日志',['log','logs','日志','记录','debug','trace','error'],['.log','.txt','.md','.json']),
]
DEFAULT_CAT = '其他资料'

# ============ 工具函数 ============
def norm(p): return str(Path(p)).lower()
def get_proj(root,fp): 
    r=Path(fp).relative_to(root)
    p=[x for x in r.parts if x]
    return p[0] if p else 'unknown'

def is_src_ext(fn):
    return any(fn.lower().endswith(e) for e in SRC_EXTS)

def is_lock_or_dev_config(fn):
    fnl=fn.lower()
    lock_files={f.lower() for f in LOCK_DEV_FILES}
    if fnl in lock_files: return True
    if any(('*' in pat) and fnmatch.fnmatch(fnl, pat.lower()) for pat in lock_files): return True
    if fnl.startswith('.') and fnl not in {f.lower() for f in DEPLOY_FILES} and fnl not in {f.lower() for f in SPECIAL_FILES}: return True
    return False

def is_deploy_config(fn):
    return fn.lower() in {f.lower() for f in DEPLOY_FILES}

def is_doc_ext(fn):
    return any(fn.lower().endswith(e) for e in DOC_EXTS)

def in_doc_dir(fp):
    parts=[p.lower() for p in Path(fp).parts]
    return any(d in parts for d in DOC_DIRS)

def has_doc_keyword(fn):
    fnl=fn.lower()
    return any(k.lower() in fnl for k in DOC_KEYWORDS)

def is_special_file(fn):
    return fn.lower() in {f.lower() for f in SPECIAL_FILES}

def skip_dir(d): return d.lower() in {x.lower() for x in SKIP_DIRS}

def skip_generated_file(fn):
    fnl=fn.lower()
    return fnl in {'index_data.json','folder_type_index_import.json','.env'} or fnl.startswith('.env.')

def match_cat(fn,fp,pd):
    nl,pl,pdl=fn.lower(),fp.lower(),pd.lower()
    for cat,kws,exts in RULES:
        if any(nl==e.lower() or nl.endswith(e.lower()) for e in exts):
            if any(k.lower() in nl or k.lower() in pl or k.lower() in pdl for k in kws): return cat
    return None

def should_index_file(fn,fp,pd):
    # 1. 特殊保留文件总是保留
    if is_special_file(fn): return True
    # 2. 部署配置保留并归类到部署资料  
    if is_deploy_config(fn): return True
    # 3. 源码文件默认排除。FolderTypeIndex 不是源码浏览器。
    if is_src_ext(fn): return False
    # 4. 锁文件/开发配置排除 (部署配置已在上一步处理)
    if is_lock_or_dev_config(fn): return False
    # 5. 文档扩展名可保留  
    if is_doc_ext(fn): return True
    # 6. 在资料目录的文件可保留  
    if in_doc_dir(fp): return True
    # 7. 文件名有资料关键词可保留  
    if has_doc_keyword(fn): return True
    # 8. 其他默认排除，不进入其他资料  
    return False

# ============ 扫描函数 ============
def scan(root,maxf,dry):
    rp=Path(root).resolve()
    items=[]
    stats={'total':0,'indexed':0,'skip_src':0,'skip_lock':0,'skip_generated':0,'skip_novalue':0,'limited':False,'by_cat':{}}
    seen=set()
    samples={}
    stop_scan=False
    print('[扫描]',rp,'max=',maxf,'dry=',dry)

    for dp,dns,fns in os.walk(rp):
        dns[:]=[d for d in dns if not skip_dir(d)]

        for fn in fns:
            if stats['total']>=maxf:
                if not stats['limited']:
                    print('[扫描] 已达限制',maxf)
                    stats['limited']=True
                stop_scan=True
                break

            stats['total']+=1
            fp=os.path.join(dp,fn)
            fpn=norm(fp)
            if fpn in seen: continue
            seen.add(fpn)
            pd=os.path.basename(dp)

            if skip_generated_file(fn):
                stats['skip_generated']+=1; continue

            # 过滤判断：源码文件默认排除；部署配置和特殊文件已在 should_index_file 内保留。
            if is_src_ext(fn) and not is_special_file(fn):
                stats['skip_src']+=1; continue
            if is_lock_or_dev_config(fn) and not is_deploy_config(fn):
                stats['skip_lock']+=1; continue
            if not should_index_file(fn,fp,pd):
                stats['skip_novalue']+=1; continue

            # 分类匹配
            cat=match_cat(fn,fp,pd)
            if not cat:
                if is_special_file(fn):
                    if 'readme' in fn.lower() or 'contributing' in fn.lower() or 'license' in fn.lower(): cat='操作指南'
                    elif 'changelog' in fn.lower(): cat='日志'
                    elif 'claude' in fn.lower() or 'agents' in fn.lower(): cat='Prompt资料'
                    else: cat='操作指南'
                elif is_deploy_config(fn): cat='部署资料'
                else: cat=DEFAULT_CAT

            proj=get_proj(root,fp)
            rel=Path(fp).relative_to(rp)
            subs=[p for p in rel.parts[1:-1] if p]  # 排除项目名和文件名
            tp=[cat,proj]+subs  # tree_path 不包含文件名
            note='自动扫描:'+fn[:30]
            items.append({'tree_path':tp,'name':fn,'type':'文件链接','path':str(Path(fp).resolve()),'url':'','note':note})
            stats['indexed']+=1
            stats['by_cat'][cat]=stats['by_cat'].get(cat,0)+1
            if cat not in samples: samples[cat]=[]
            if len(samples[cat])<5: samples[cat].append({'name':fn,'proj':proj,'path':fp})
            if dry and stats['indexed']%100==0: print('[dry] indexed',stats['indexed'],'...')

        if stop_scan:
            break

    return items,stats,samples

# ============ 输出函数 ============
def gen_json(items,out):
    o={'version':1,'generated_at':datetime.now().isoformat(),'items':items}
    op=Path(out);op.parent.mkdir(parents=True,exist_ok=True)
    op.write_text(json.dumps(o,ensure_ascii=False,indent=2),encoding='utf-8')
    print('[输出]',op.resolve())

def prstats(s,samples,dry):
    m='[dry-run]' if dry else '[生成]'
    print('',m,'统计:')
    print('  扫描文件数:',s['total'])
    print('  已索引文件数:',s['indexed'])
    print('  跳过源码文件:',s['skip_src'])
    print('  跳过配置/锁文件:',s['skip_lock'])
    print('  跳过生成/敏感文件:',s.get('skip_generated',0))
    print('  跳过无资料价值:',s['skip_novalue'])
    print('  是否达到 max-files 限制:','是' if s.get('limited') else '否')
    print('  分类统计:')
    if not s['by_cat']:
        print('    无')
    for c,n in sorted(s['by_cat'].items(),key=lambda x:-x[1]):
        print('   ',c+':',n)
    if samples and dry:
        print('  分类样例 (dry-run):')
        for c in sorted(samples.keys()):
            print('   ',c+':')
            for it in samples[c][:5]:
                print('     -',it['proj']+'/'+it['name'])

# ============ 主函数 ============
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',default=r'D:\AI Project')
    ap.add_argument('--out',default='folder_type_index_import.json')
    ap.add_argument('--dry-run',action='store_true')
    ap.add_argument('--max-files',type=int,default=5000)
    args=ap.parse_args()
    if not os.path.isdir(args.root): print('[错误]',args.root,file=sys.stderr);sys.exit(1)
    items,stats,samples=scan(args.root,args.max_files,args.dry_run)
    prstats(stats,samples,args.dry_run)
    if not args.dry_run: 
        gen_json(items,args.out)
        print('', '[提示] 用 GUI 导入:',Path(args.out).resolve())
    else: print('', '[dry-run] 未写入文件')
    print('', '[安全] 仅读取元信息，未修改文件')
    print('[安全] 勿提交含真实路径的 JSON')
    return 0
if __name__=='__main__': sys.exit(main())
