# FolderTypeIndex 操作指南

## 1. 项目位置

项目根目录：

```text
D:\AI Project\FolderTypeIndex
```

当前 GUI 主程序位置：

```text
D:\AI Project\FolderTypeIndex\folder_type_index_v4_codex_import
```

扫描脚本位置：

```text
D:\AI Project\FolderTypeIndex\tools\generate_folder_type_index_import.py
```

导入文件位置：

```text
D:\AI Project\FolderTypeIndex\folder_type_index_import.json
```

真实资料目录：

```text
D:\AI Project
```

---

## 2. 核心原则

FolderTypeIndex 不是文件管理器，而是“资料索引树”。

它只建立超链接索引，不改变真实文件。

必须记住：

1. 不复制真实文件。
2. 不移动真实文件。
3. 不删除真实文件。
4. 删除索引节点，只删除索引，不删除真实文件。
5. 一个真实文件可以被挂到多个资料类型下面。
6. `index_data.json` 是本地真实索引数据，不要提交到 GitHub。
7. `folder_type_index_import.json` 含有本机真实路径，不要提交到 GitHub。

---

## 3. 启动软件

打开 PowerShell，执行：

```powershell
cd "D:\AI Project\FolderTypeIndex"
python folder_type_index_v4_codex_import\folder_type_index.py
```

如果想从 VS Code 启动，也可以在 VS Code 终端中执行同样命令。

---

## 4. 软件界面说明

界面主要分为三部分：

1. 左侧：索引树。
2. 右侧：节点详情 / 编辑区。
3. 顶部和底部：功能按钮。

常见节点类型：

```text
分类
文件链接
文件夹链接
网址
备注
```

---

## 5. 手工添加索引

### 5.1 新增一级分类

点击：

```text
新建一级分类
```

输入分类名称，例如：

```text
操作指南
文献资料
部署资料
实验数据
Prompt资料
日志
```

### 5.2 添加子分类

选中某个分类节点，点击：

```text
添加子
```

可以在该分类下继续建立子分类。

### 5.3 添加文件链接

选中目标分类，点击：

```text
添加文件
```

选择真实文件。

软件只保存文件路径，不复制文件。

### 5.4 添加文件夹链接

选中目标分类，点击：

```text
添加文件夹
```

选择真实文件夹。

软件只保存文件夹路径，不复制文件夹。

### 5.5 添加网址

选中目标分类，点击：

```text
添加网址
```

填写名称和网址。

---

## 6. 编辑节点

选中左侧索引树中的节点后，右侧会显示：

```text
名称
类型
本地路径
网址
备注
```

修改后点击：

```text
保存修改
```

---

## 7. 打开资源

双击左侧节点，或选中节点后点击：

```text
打开资源
```

不同类型的行为：

1. 文件链接：打开真实文件。
2. 文件夹链接：打开真实文件夹。
3. 网址：用浏览器打开网页。
4. 分类 / 备注：通常不打开资源。

---

## 8. 自动扫描生成导入 JSON

当前版本已经集成按钮：

```text
扫描生成导入 JSON
```

点击后会弹出确认框。

确认后，软件会扫描：

```text
D:\AI Project
```

并生成：

```text
D:\AI Project\FolderTypeIndex\folder_type_index_import.json
```

注意：

1. 扫描只读取文件名、路径、扩展名等元信息。
2. 不读取大量文件正文。
3. 不复制、移动、删除真实文件。
4. 不自动修改 `index_data.json`。
5. 只生成导入 JSON，需要用户再手动导入。

---

## 9. 导入 Codex JSON

生成导入 JSON 后，点击：

```text
导入 Codex JSON
```

选择：

```text
D:\AI Project\FolderTypeIndex\folder_type_index_import.json
```

导入完成后会显示统计，例如：

```text
新增：1101
更新/去重：175
跳过：0
```

导入后检查：

1. 左侧是否出现资料类型分类。
2. 文件节点是否显示为“文件链接”。
3. 双击文件节点是否能打开真实文件。

---

## 10. 命令行扫描方式

除了 GUI 按钮，也可以手动用 PowerShell 运行扫描。

### 10.1 dry-run 预览

不生成文件，只看统计：

```powershell
cd "D:\AI Project\FolderTypeIndex"
python tools\generate_folder_type_index_import.py --root "D:\AI Project" --out "folder_type_index_import.json" --dry-run --max-files 2000
```

### 10.2 正式生成

```powershell
cd "D:\AI Project\FolderTypeIndex"
python tools\generate_folder_type_index_import.py --root "D:\AI Project" --out "folder_type_index_import.json" --max-files 5000
```

然后回到 GUI，点击：

```text
导入 Codex JSON
```

---

## 11. 当前自动分类规则

自动扫描会尝试把资料归入：

```text
操作指南
部署资料
文献资料
实验数据
Prompt资料
日志
其他资料
```

默认会排除大量无资料价值文件，例如：

```text
源码文件
锁文件
构建产物
缓存文件
依赖目录
普通开发配置
```

如果仍然发现“其他资料”太多，后续可以继续优化规则。

---

## 12. GitHub 提交注意事项

提交前先检查：

```powershell
cd "D:\AI Project\FolderTypeIndex"
git status --short
```

不要提交：

```text
index_data.json
folder_type_index_import.json
.env
.venv
node_modules
dist
build
临时 zip 文件
```

正常提交示例：

```powershell
git add README.md docs tasks tools folder_type_index_v4_codex_import
git commit -m "update project docs"
git push
```

如果只是查看状态或运行软件，不需要提交。

---

## 13. 常见问题

### 13.1 PowerShell 手动运行命令会消耗大模型 token 吗？

不会。

手动运行：

```powershell
git status
python xxx.py
```

只是本地执行，不消耗大模型 token。

会消耗 token 的是：

```text
Codex
Qwen Agent
Claude Code
Gemini CLI
```

这类 AI Agent 帮你读文件、改代码、执行任务时才会消耗 token。

### 13.2 为什么 folder_type_index_import.json 不提交？

因为它包含真实本地路径，例如：

```text
D:\AI Project\...
```

这些路径属于个人本地环境，不适合上传 GitHub。

### 13.3 为什么 index_data.json 不提交？

因为它是用户本地真实索引数据，也可能包含真实路径和私人资料结构。

### 13.4 删除索引节点会删除真实文件吗？

正常情况下不会。

FolderTypeIndex 的设计原则是：

```text
删除索引，只删除索引记录，不删除真实文件。
```

---

## 14. 推荐日常流程

### 日常使用

```text
启动 GUI
→ 查看 / 打开资料索引
→ 手工新增或编辑节点
→ 保存
```

### 批量更新索引

```text
启动 GUI
→ 点击“扫描生成导入 JSON”
→ 确认生成
→ 点击“导入 Codex JSON”
→ 检查新增节点
```

### 开发维护

```text
修改代码或文档
→ 本地测试
→ git status --short
→ git add
→ git commit
→ git push
```

---

## 15. 当前项目阶段

已完成：

```text
Task01：MIT 开源项目初始化
Task02：扫描生成导入 JSON
Task03：扫描过滤规则优化
Task04：GUI 集成“扫描生成导入 JSON”按钮
```

当前状态：

```text
FolderTypeIndex 已经具备基本可用的 GUI + 自动扫描导入流程。
```
