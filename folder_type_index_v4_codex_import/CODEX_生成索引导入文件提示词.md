# 给 Codex 的提示词：生成 FolderTypeIndex 导入 JSON

你在 VS Code / Codex 中执行本任务。

目标：扫描我的项目总目录，把“操作指南、部署资料、文献资料、实验数据、Prompt资料”等重要文件整理成 FolderTypeIndex 可导入的 JSON。

## 项目总目录

请优先扫描：

```text
D:\AI Project
```

如果这个目录不存在，再根据当前工作区实际目录处理。

## 输出文件

请生成：

```text
D:\AI Project\folder_type_index_import.json
```

## JSON 格式

必须是合法 UTF-8 JSON，结构如下：

```json
{
  "version": 1,
  "items": [
    {
      "tree_path": ["操作指南", "项目名", "子分类"],
      "name": "显示名称",
      "type": "文件链接",
      "path": "真实本地路径",
      "url": "",
      "note": "一句话说明"
    }
  ]
}
```

## 分类规则

请按“资料类型”重组，不要按真实文件夹原样输出。

一级分类建议：

```text
操作指南
部署资料
文献资料
实验数据
Prompt资料
日志记录
截图资料
项目任务
```

二级分类通常是项目名，例如：

```text
操作指南 / AI项目教练 / Codex使用
部署资料 / 大观园 / Cloudflare
文献资料 / ABKI-Med / 问诊方法论
实验数据 / ABKI-Med / 盲测记录
```

## 识别规则

优先收录这些文件：

```text
README
AGENTS
CLAUDE
指南
教程
说明
手册
安装
部署
运行
配置
操作
任务
prompt
Prompt
实验
评测
结果
数据
论文
文献
reference
research
docs
tasks
evaluation
results
deploy
cloudflare
vercel
```

不要收录：

```text
node_modules
.git
.next
dist
build
.cache
venv
.env
package-lock.json
pnpm-lock.yaml
yarn.lock
图片缓存
临时文件
```

## 类型判断

- 真实文件：type = "文件链接"
- 真实文件夹：type = "文件夹链接"
- 网页：type = "网址"
- 纯分类：type = "分类"

## 重要要求

1. 不移动、不复制、不删除真实文件。
2. 只生成 JSON。
3. 每条 item 的 path 必须是 Windows 绝对路径。
4. tree_path 是索引树中的父路径，不包含当前文件名。
5. name 是当前索引节点显示名。
6. 尽量少而精，先收录重要指南、部署、文献、实验数据，不要把所有 md 都塞进去。
7. 生成后检查 JSON 语法有效。
