# task02：Codex VS 扫描项目并生成 FolderTypeIndex 导入 JSON

## 当前状态

项目根目录：

```text
D:\AI Project\FolderTypeIndex
```

当前可运行版本位于：

```text
D:\AI Project\FolderTypeIndex\folder_type_index_v4_codex_import
```

这一版已经具备基本功能：

1. GUI 索引树。
2. 支持分类、文件链接、文件夹链接、网址、备注。
3. 支持编辑节点。
4. 双击节点可打开真实文件、文件夹或网页。
5. 数据保存到 `index_data.json`。
6. 支持“导入 Codex JSON”。
7. 支持“生成导入模板”。

本任务不是重做 GUI，也不是重构项目结构。

本任务目标是：让 Codex 在 VS Code 中扫描真实项目目录，识别资料类型，并生成 FolderTypeIndex 可导入的 JSON 文件。

---

## 本任务目标

新增一个独立的扫描生成脚本：

```text
tools\generate_folder_type_index_import.py
```

它负责扫描：

```text
D:\AI Project
```

识别项目文件属于哪类资料：

```text
操作指南
部署资料
文献资料
实验数据
Prompt资料
日志
其他资料
```

然后生成：

```text
folder_type_index_import.json
```

该 JSON 必须符合当前 FolderTypeIndex GUI 的“导入 Codex JSON”格式。

---

## 强制安全规则

必须遵守：

1. 不复制真实文件。
2. 不移动真实文件。
3. 不删除真实文件。
4. 不修改 `D:\AI Project` 下任何真实项目内容。
5. 不改变真实项目目录结构。
6. 不直接修改 `index_data.json`。
7. 不直接向现有索引写入数据。
8. 只生成导入文件 `folder_type_index_import.json`。
9. 扫描时只读取文件名、路径、扩展名、上级目录名等元信息。
10. 不读取大量文件正文内容。
11. 不提交真实生成的 `folder_type_index_import.json` 到 GitHub。
12. 不提交包含用户真实本地路径的扫描结果。

---

## 第一步：确认现有导入格式

先查看当前 GUI 代码中这两个功能：

1. “生成导入模板”
2. “导入 Codex JSON”

必须找出真实字段结构。

不要凭空设计新 JSON 格式。

请在代码中搜索关键词：

```text
导入
Codex
template
import
folder_type_index_import
index_data
```

确认当前导入 JSON 的结构后，再写生成脚本。

---

## 第二步：新增 tools 目录和扫描脚本

如果没有 `tools` 目录，新建：

```text
tools
```

新增脚本：

```text
tools\generate_folder_type_index_import.py
```

脚本支持命令：

```powershell
python tools\generate_folder_type_index_import.py --root "D:\AI Project" --out "folder_type_index_import.json"
```

必须支持：

```powershell
--dry-run
--max-files 5000
```

示例：

```powershell
python tools\generate_folder_type_index_import.py --root "D:\AI Project" --out "folder_type_index_import.json" --dry-run --max-files 500
```

---

## 第三步：扫描范围

默认扫描：

```text
D:\AI Project
```

但必须跳过当前项目自身的这些生成文件和 Git 目录：

```text
D:\AI Project\FolderTypeIndex\.git
D:\AI Project\FolderTypeIndex\folder_type_index_import.json
D:\AI Project\FolderTypeIndex\index_data.json
```

也要跳过常见无意义目录：

```text
.git
node_modules
.next
.open-next
dist
build
out
.cache
venv
.venv
__pycache__
.wrangler
.vercel
.idea
.vscode
```

---

## 第四步：分类规则

第一版用规则匹配，不接 AI API。

根据：

1. 文件名
2. 扩展名
3. 上级目录名
4. 项目名

进行分类。

### 操作指南

关键词：

```text
guide
指南
教程
操作
说明
manual
howto
how-to
readme
使用
入门
```

常见后缀：

```text
.md
.txt
.docx
.pdf
```

### 部署资料

关键词：

```text
deploy
deployment
部署
vercel
cloudflare
wrangler
railway
docker
dockerfile
compose
nginx
域名
dns
worker
pages
```

常见文件：

```text
Dockerfile
docker-compose.yml
wrangler.toml
vercel.json
```

常见后缀：

```text
.md
.txt
.json
.yaml
.yml
.toml
```

### 文献资料

关键词：

```text
paper
papers
论文
文献
reference
references
article
articles
reading
research
arxiv
citation
bibliography
```

常见后缀：

```text
.pdf
.md
.docx
.bib
```

### 实验数据

关键词：

```text
data
dataset
datasets
实验
测试数据
样本
sample
samples
eval
evaluation
benchmark
result
results
metrics
统计
```

常见后缀：

```text
.csv
.xlsx
.xls
.json
.jsonl
.parquet
.db
.sqlite
```

### Prompt资料

关键词：

```text
prompt
prompts
提示词
system prompt
系统提示词
agent
agents
persona
role
角色
workflow
工作流
```

常见后缀：

```text
.md
.txt
.json
.yaml
.yml
```

### 日志

关键词：

```text
log
logs
日志
记录
debug
trace
runtime
error
crash
report
```

常见后缀：

```text
.log
.txt
.md
.json
```

### 其他资料

没有命中以上规则，但仍值得索引的文件，放入：

```text
其他资料
```

---

## 第五步：生成索引树结构

生成的导入 JSON 顶层按资料类型组织：

```text
操作指南
部署资料
文献资料
实验数据
Prompt资料
日志
其他资料
```

每个资料类型下面按真实项目名分组。

例如真实文件：

```text
D:\AI Project\zero-basic-ai-project-coach\docs\deploy.md
```

导入后结构应接近：

```text
部署资料
  zero-basic-ai-project-coach
    deploy.md
```

文件节点必须指向真实文件绝对路径：

```text
D:\AI Project\zero-basic-ai-project-coach\docs\deploy.md
```

---

## 第六步：去重规则

同一个真实文件在同一个分类下不要重复出现。

Windows 路径大小写不敏感，去重时建议统一转小写。

第一版先采用“最可能分类”，不要把一个文件同时挂到太多分类，避免导入树过乱。

---

## 第七步：dry-run

先运行：

```powershell
python tools\generate_folder_type_index_import.py --root "D:\AI Project" --out "folder_type_index_import.json" --dry-run --max-files 500
```

dry-run 要求：

1. 不写入 `folder_type_index_import.json`。
2. 只打印统计结果。
3. 显示分类数量。
4. 显示预计输出路径。

---

## 第八步：正式生成

dry-run 无误后运行：

```powershell
python tools\generate_folder_type_index_import.py --root "D:\AI Project" --out "folder_type_index_import.json" --max-files 5000
```

生成后检查：

1. JSON 格式合法。
2. 字段符合当前 GUI 导入格式。
3. 能被“导入 Codex JSON”功能读取。
4. 没有修改 `index_data.json`。
5. 没有修改真实项目文件。

---

## 第九步：Git 规则

可以提交：

```text
tools\generate_folder_type_index_import.py
```

不要提交：

```text
index_data.json
folder_type_index_import.json
```

如果 `.gitignore` 没有忽略这些文件，请补充：

```gitignore
index_data.json
folder_type_index_import.json
```

---

## 完成后汇报

请按以下格式汇报：

```text
完成情况：

1. 新增文件：
- tools\generate_folder_type_index_import.py

2. 修改文件：
- 如有，列出

3. 已确认现有导入格式：
- 简要说明字段结构

4. dry-run 结果：
- 扫描文件数
- 各分类数量

5. 正式生成结果：
- 是否生成 folder_type_index_import.json
- 输出位置

6. GUI 导入测试：
- 是否已测试
- 如果未测试，说明待用户手动导入

7. 安全确认：
- 没有修改 index_data.json
- 没有复制、移动、删除真实文件
- 没有修改 D:\AI Project 下真实项目内容
- 没有提交 folder_type_index_import.json
```
