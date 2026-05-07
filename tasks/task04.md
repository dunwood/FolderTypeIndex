# task04：把“扫描生成导入 JSON”集成到 GUI 按钮中

## 当前状态

项目根目录：

```text
D:\AI Project\FolderTypeIndex
```

当前 GUI 可运行版本位于：

```text
D:\AI Project\FolderTypeIndex\folder_type_index_v4_codex_import
```

已完成：

1. Task01：MIT 开源项目初始化并推送 GitHub。
2. Task02：新增扫描脚本 `tools\generate_folder_type_index_import.py`。
3. Task03：优化扫描过滤规则，修复 `max-files` 停止条件。
4. 生成的 `folder_type_index_import.json` 已通过 GUI 导入测试。
5. 当前工作区已 clean，远程 GitHub 已同步。

现在的问题：

用户仍然需要在 PowerShell 手动运行：

```powershell
python tools\generate_folder_type_index_import.py --root "D:\AI Project" --out "folder_type_index_import.json" --max-files 5000
```

然后再回到 GUI 点击“导入 Codex JSON”。

本任务目标是：在 GUI 中增加“扫描生成导入 JSON”入口，让用户不用手动跑命令。

---

## 本任务目标

在现有 GUI 中新增一个按钮或菜单项：

```text
扫描生成导入 JSON
```

点击后，GUI 可以调用现有扫描脚本：

```text
tools\generate_folder_type_index_import.py
```

生成：

```text
folder_type_index_import.json
```

生成完成后弹窗提示用户：

```text
已生成导入 JSON，可点击“导入 Codex JSON”导入。
```

本任务只负责从 GUI 触发生成导入 JSON，不自动导入，不直接修改 `index_data.json`。

---

## 强制安全规则

必须遵守：

1. 不复制真实文件。
2. 不移动真实文件。
3. 不删除真实文件。
4. 不修改 `D:\AI Project` 下任何真实项目内容。
5. 不自动修改 `index_data.json`。
6. 不自动导入生成结果。
7. 不提交真实生成的 `folder_type_index_import.json`。
8. 不破坏已有“导入 Codex JSON”功能。
9. 不破坏已有“生成导入模板”功能。
10. 不大规模重构 GUI。
11. 只做最小可用集成。

---

## 需要实现的功能

### 1. 找到 GUI 主程序

先在当前项目中确认 GUI 主程序位置。

重点查看：

```text
folder_type_index_v4_codex_import
```

搜索关键词：

```text
导入 Codex JSON
生成导入模板
index_data.json
tkinter
PyQt
customtkinter
```

确定当前 GUI 是如何添加按钮或菜单的。

---

### 2. 在 GUI 中新增入口

在现有按钮区域或菜单区域增加：

```text
扫描生成导入 JSON
```

要求：

1. 不影响原有按钮布局。
2. 不删除原有按钮。
3. 按钮文字清楚。
4. 点击后执行扫描生成流程。

如果当前 GUI 是 Tkinter，可以使用现有按钮风格。

---

### 3. 默认扫描参数

第一版先用默认参数，不做复杂设置界面：

```text
root = D:\AI Project
out = D:\AI Project\FolderTypeIndex\folder_type_index_import.json
max-files = 5000
dry-run = False
```

如果实现方便，可以在点击按钮后弹出确认框：

```text
将扫描 D:\AI Project，并生成 folder_type_index_import.json。
不会复制、移动、删除真实文件。
是否继续？
```

建议必须有确认框。

---

### 4. 调用扫描脚本

优先使用安全、简单、稳定方式。

可以选择两种方式之一。

#### 方案 A：subprocess 调用脚本

从 GUI 中执行：

```powershell
python tools\generate_folder_type_index_import.py --root "D:\AI Project" --out "folder_type_index_import.json" --max-files 5000
```

要求：

1. 工作目录必须是项目根目录 `D:\AI Project\FolderTypeIndex`。
2. 能捕获 stdout / stderr。
3. 成功后弹窗显示生成位置和统计摘要。
4. 失败后弹窗显示错误信息。

#### 方案 B：导入脚本函数

如果现有结构方便，可以把 `tools\generate_folder_type_index_import.py` 中的 `scan()` / `gen_json()` 函数导入 GUI 调用。

要求：

1. 不破坏脚本原有 CLI 使用方式。
2. 仍然可以继续从命令行运行脚本。
3. GUI 调用时能拿到统计结果。

优先选择改动最小、风险最低的方案。

---

### 5. 生成完成后的提示

生成成功后弹窗提示：

```text
扫描完成。

输出文件：
D:\AI Project\FolderTypeIndex\folder_type_index_import.json

下一步：
请点击“导入 Codex JSON”导入。
```

如果能显示统计摘要更好，例如：

```text
扫描文件数：3593
已索引文件数：1276
其他资料：714
Prompt资料：235
操作指南：191
部署资料：32
```

但第一版不强制做复杂统计 UI。

---

### 6. 不自动导入

本任务不要自动把生成结果写入索引树。

原因：

1. 用户应先知道生成了什么。
2. 避免误导入大量节点。
3. 避免直接修改 `index_data.json`。
4. 继续保留“生成”和“导入”两个明确动作。

所以流程保持为：

```text
点击“扫描生成导入 JSON”
  → 生成 folder_type_index_import.json
  → 用户点击“导入 Codex JSON”
  → 用户确认导入
```

---

### 7. 路径处理

注意 GUI 主程序可能在：

```text
folder_type_index_v4_codex_import
```

而扫描脚本在项目根目录：

```text
tools\generate_folder_type_index_import.py
```

因此不能假设当前工作目录一定正确。

请在代码中稳妥定位项目根目录：

```text
D:\AI Project\FolderTypeIndex
```

或通过当前文件位置向上查找，找到包含：

```text
tools\generate_folder_type_index_import.py
```

的目录。

不要硬编码到用户之外的路径。

---

### 8. 错误处理

如果扫描脚本不存在，提示：

```text
未找到扫描脚本 tools\generate_folder_type_index_import.py
```

如果 Python 执行失败，提示 stderr。

如果生成文件失败，提示用户检查路径权限。

如果用户取消确认框，不做任何操作。

---

## 测试要求

完成后测试：

### 1. GUI 启动测试

启动现有 GUI，确认：

1. 原有功能仍在。
2. 新按钮出现。
3. 原有“导入 Codex JSON”仍在。
4. 原有“生成导入模板”仍在。

### 2. 扫描按钮测试

点击：

```text
扫描生成导入 JSON
```

确认：

1. 有安全确认弹窗。
2. 点击取消时不生成文件。
3. 点击确定时生成 `folder_type_index_import.json`。
4. 生成完成后有提示。
5. 没有修改 `index_data.json`。

### 3. 导入测试

生成后点击：

```text
导入 Codex JSON
```

选择：

```text
D:\AI Project\FolderTypeIndex\folder_type_index_import.json
```

确认仍可导入。

### 4. Git 检查

确认不要提交：

```text
folder_type_index_import.json
index_data.json
```

执行：

```powershell
git status --short
```

如果看到 `folder_type_index_import.json`，说明 `.gitignore` 有问题，需要修复。

---

## Git 要求

可以提交：

```text
GUI 主程序相关文件
tasks\task04.md
```

不要提交：

```text
folder_type_index_import.json
index_data.json
```

提交信息建议：

```text
add gui scanner trigger
```

---

## 完成后汇报格式

请按以下格式汇报：

```text
Task04 完成情况：

1. 修改文件：
- 列出 GUI 文件
- tasks\task04.md

2. 新增 GUI 功能：
- 按钮/菜单名称
- 触发流程

3. 扫描参数：
- root
- out
- max-files

4. 测试结果：
- GUI 是否能启动
- 新按钮是否出现
- 取消确认是否正常
- 点击确认是否能生成 JSON
- 是否能继续用“导入 Codex JSON”导入

5. Git：
- commit 是否成功
- push 是否成功

6. 安全确认：
- 没有修改 index_data.json
- 没有提交 folder_type_index_import.json
- 没有复制、移动、删除真实文件
- 没有修改 D:\AI Project 下其他项目内容
```
