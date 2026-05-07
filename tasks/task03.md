# task03：优化扫描过滤与分类规则，减少无效代码文件进入索引

## 当前状态

Task02 已完成：

1. 已新增扫描脚本：

```text
tools\generate_folder_type_index_import.py
```

2. 已能扫描：

```text
D:\AI Project
```

3. 已能生成：

```text
folder_type_index_import.json
```

4. GUI 已经可以成功导入生成的 JSON。

5. 当前问题：

正式生成 2000 个条目中，大量文件进入了：

```text
其他资料
```

例如很多代码文件、配置文件、普通项目文件并不需要进入这个资料索引树。

本软件的目标不是做“全项目文件浏览器”，而是做“按资料类型重组的项目资料索引树”。

因此 task03 的目标是：优化扫描脚本，让它只索引有资料价值的文件，默认排除大多数源码文件和构建产物。

---

## 本任务目标

修改：

```text
tools\generate_folder_type_index_import.py
```

重点实现：

1. 默认排除源码文件。
2. 默认排除构建产物、依赖文件、缓存文件。
3. 只保留有资料价值的文档、部署配置、Prompt、数据、日志、论文等。
4. 大幅减少“其他资料”。
5. 让生成的索引树更清爽，适合 GUI 浏览。
6. 确保导入后叶子节点是真正的“文件链接”，不要把文件名误建成分类节点。

---

## 强制安全规则

必须遵守：

1. 不复制真实文件。
2. 不移动真实文件。
3. 不删除真实文件。
4. 不修改 `D:\AI Project` 下任何真实项目内容。
5. 不修改 `index_data.json`。
6. 不提交真实生成的 `folder_type_index_import.json`。
7. 只修改扫描脚本和必要文档。
8. 生成 JSON 只用于用户手动导入测试。
9. 扫描时只读取文件名、路径、扩展名、上级目录名等元信息。
10. 不批量读取真实文件正文。

---

## 需要解决的问题

### 问题 1：大量源码文件不该进入索引

默认排除常见源码扩展名：

```text
.py
.js
.jsx
.ts
.tsx
.css
.scss
.sass
.html
.htm
.java
.c
.cpp
.h
.hpp
.cs
.go
.rs
.php
.rb
.swift
.kt
.m
.mm
.vue
.svelte
```

注意：

如果源码文件本身位于明确资料目录，例如：

```text
docs
guides
manual
prompts
examples
```

可以保留少量示例，但第一版仍以排除为主，避免噪音。

---

### 问题 2：普通配置文件不应全部进入索引

默认排除普通开发配置文件：

```text
package-lock.json
pnpm-lock.yaml
yarn.lock
tsconfig.json
jsconfig.json
eslint.config.*
.prettierrc
.prettierignore
.gitignore
.gitattributes
```

但以下部署相关配置应保留并归入“部署资料”：

```text
Dockerfile
docker-compose.yml
compose.yml
wrangler.toml
vercel.json
netlify.toml
railway.json
nginx.conf
```

---

### 问题 3：“其他资料”需要收紧

不是所有不匹配的文件都应该进入“其他资料”。

修改规则：

只有满足以下条件之一的文件，才允许进入“其他资料”：

1. 是常见文档文件：

```text
.md
.txt
.pdf
.docx
.doc
.pptx
.ppt
.xlsx
.xls
.csv
.jsonl
.bib
```

2. 位于明显资料目录：

```text
docs
doc
documentation
notes
knowledge
materials
resources
references
papers
research
prompts
data
datasets
logs
reports
tasks
```

3. 文件名明显有资料价值：

```text
summary
总结
记录
notes
note
report
报告
方案
设计
plan
规划
spec
需求
requirement
analysis
分析
复盘
review
```

否则不要纳入索引。

---

### 问题 4：保留 README / CLAUDE / AGENTS 等项目说明文件

以下文件应保留，通常归入“操作指南”或“Prompt资料”：

```text
README.md
CLAUDE.md
AGENTS.md
CONTRIBUTING.md
CHANGELOG.md
```

建议分类：

- `README.md` → 操作指南
- `CONTRIBUTING.md` → 操作指南
- `CHANGELOG.md` → 日志
- `CLAUDE.md` → Prompt资料
- `AGENTS.md` → Prompt资料

---

### 问题 5：导入后文件节点类型要正确

请检查当前生成 JSON 的结构，确保：

1. 顶层资料类型节点是“分类”。
2. 项目名节点是“分类”。
3. 中间目录节点是“分类”。
4. 最后的真实文件节点必须是：

```text
type: "文件链接"
```

5. 文件节点应包含真实绝对路径：

```text
path: "D:\AI Project\某项目\某文件.md"
```

6. 文件节点的 `tree_path` 不要错误地把文件名也放进去，导致 GUI 把文件名建成分类。

例如真实文件：

```text
D:\AI Project\BettaFish\docs\README.md
```

推荐结构：

```json
{
  "tree_path": ["操作指南", "BettaFish", "docs"],
  "name": "README.md",
  "type": "文件链接",
  "path": "D:\\AI Project\\BettaFish\\docs\\README.md",
  "url": "",
  "note": "自动扫描：README / docs"
}
```

不要生成成：

```json
{
  "tree_path": ["操作指南", "BettaFish", "docs", "README.md"],
  "name": "README.md",
  "type": "文件链接"
}
```

---

## 建议实现方式

在脚本中加入类似逻辑：

```text
should_skip_dir()
should_skip_file()
is_source_code_file()
is_lock_or_dev_config()
is_useful_document()
classify_file()
```

逻辑顺序建议：

```text
1. 跳过目录
2. 跳过明确无用文件
3. 判断是否是特殊保留文件
4. 判断是否命中明确分类
5. 判断是否有资料价值
6. 否则跳过，不进入“其他资料”
```

---

## 增加统计项

输出统计中增加：

```text
扫描文件数
已索引文件数
跳过源码文件数
跳过配置/锁文件数
跳过无资料价值文件数
操作指南数量
部署资料数量
文献资料数量
实验数据数量
Prompt资料数量
日志数量
其他资料数量
```

dry-run 时额外打印每个分类前 5 个样例。

---

## 测试要求

先运行 dry-run：

```powershell
python tools\generate_folder_type_index_import.py --root "D:\AI Project" --out "folder_type_index_import.json" --dry-run --max-files 2000
```

要求：

1. 不写入 JSON。
2. 输出跳过统计。
3. 输出分类统计。
4. 输出分类样例。
5. “其他资料”数量明显下降。

然后正式生成：

```powershell
python tools\generate_folder_type_index_import.py --root "D:\AI Project" --out "folder_type_index_import.json" --max-files 5000
```

要求：

1. 能生成合法 JSON。
2. JSON 字段仍符合当前 GUI 导入格式。
3. 不修改 `index_data.json`。
4. 不提交 `folder_type_index_import.json`。

---

## 验收标准

完成后应达到：

1. GUI 仍能导入生成的 JSON。
2. 源码文件数量明显减少。
3. “其他资料”不再塞满普通代码文件。
4. 保留 README、CLAUDE、AGENTS、部署配置、论文、数据、日志、Prompt 等资料文件。
5. 文件叶子节点类型正确显示为“文件链接”。
6. 项目结构仍然是：

```text
资料类型
  项目名
    子目录
      文件链接
```

---

## Git 要求

可以提交：

```text
tools\generate_folder_type_index_import.py
tasks\task03.md
```

不要提交：

```text
folder_type_index_import.json
index_data.json
```

提交信息建议：

```text
improve import scanner filtering rules
```

---

## 完成后汇报格式

请按以下格式汇报：

```text
Task03 完成情况：

1. 修改文件：
- tools\generate_folder_type_index_import.py
- tasks\task03.md

2. 本次优化：
- 列出主要过滤规则

3. dry-run 结果：
- 扫描文件数
- 已索引文件数
- 跳过源码文件数
- 跳过配置/锁文件数
- 跳过无资料价值文件数
- 各分类数量
- 每类样例

4. 正式生成结果：
- 是否生成 folder_type_index_import.json
- 输出位置
- 总条目数

5. GUI 导入：
- 是否已测试
- 文件节点是否显示为“文件链接”
- 如未测试，说明待用户手动测试

6. Git：
- commit 是否成功
- push 是否成功

7. 安全确认：
- 没有修改 index_data.json
- 没有提交 folder_type_index_import.json
- 没有复制、移动、删除真实文件
- 没有修改 D:\AI Project 下真实项目内容
```
