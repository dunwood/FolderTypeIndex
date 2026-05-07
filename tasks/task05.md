# task05：GUI 支持选择任意扫描文件夹

## 当前状态

项目根目录：

```text
D:\AI Project\FolderTypeIndex
```

当前 GUI 目录：

```text
D:\AI Project\FolderTypeIndex\folder_type_index_v4_codex_import
```

扫描脚本：

```text
D:\AI Project\FolderTypeIndex\tools\generate_folder_type_index_import.py
```

已完成：

1. GUI 已有“扫描生成导入 JSON”按钮。
2. 当前按钮默认扫描固定目录：

```text
D:\AI Project
```

3. 生成文件：

```text
D:\AI Project\FolderTypeIndex\folder_type_index_import.json
```

4. 生成后仍由用户点击“导入 Codex JSON”手动导入。
5. 不自动修改 `index_data.json`。

---

## 本任务目标

把当前固定扫描：

```text
D:\AI Project
```

改为用户可选择任意扫描目录。

用户点击：

```text
扫描生成导入 JSON
```

后，先弹出文件夹选择框，让用户选择要扫描的目录。

例如可以选择：

```text
D:\AI Project
D:\Obsidian
D:\某个资料库
D:\某个单独项目
```

然后再生成：

```text
D:\AI Project\FolderTypeIndex\folder_type_index_import.json
```

---

## 强制安全规则

必须遵守：

1. 不复制真实文件。
2. 不移动真实文件。
3. 不删除真实文件。
4. 不修改被扫描目录中的任何真实文件。
5. 不自动导入生成结果。
6. 不直接修改 `index_data.json`。
7. 不提交真实生成的 `folder_type_index_import.json`。
8. 不破坏已有“导入 Codex JSON”功能。
9. 不破坏已有“生成导入模板”功能。
10. 不大规模重构 GUI。
11. 只做最小可用修改。

---

## 需要实现的功能

### 1. 点击按钮后先选择文件夹

修改现有“扫描生成导入 JSON”按钮逻辑。

点击后先调用文件夹选择框。

如果当前 GUI 是 Tkinter，使用：

```python
filedialog.askdirectory(...)
```

要求：

1. 标题建议：

```text
选择要扫描的文件夹
```

2. 初始目录优先为：

```text
D:\AI Project
```

如果不存在，则使用项目根目录。

3. 如果用户取消选择，直接返回，不执行扫描。

---

### 2. 确认框显示用户选择的目录

选择目录后，弹出确认框。

确认框必须显示实际选择的目录，例如：

```text
将扫描以下目录：

D:\Obsidian

并生成导入文件：

D:\AI Project\FolderTypeIndex\folder_type_index_import.json

此操作只读取文件名、路径、扩展名等元信息。
不会复制、移动、删除真实文件。
不会自动修改 index_data.json。

是否继续？
```

用户点“否”时，不执行扫描。

---

### 3. 调用扫描脚本时传入用户选择的目录

原来固定：

```text
--root "D:\AI Project"
```

现在改成：

```text
--root 用户选择的目录
```

输出仍然固定为项目根目录下：

```text
folder_type_index_import.json
```

max-files 仍然使用：

```text
5000
```

---

### 4. 单项目目录分组优化

当前扫描脚本的项目名取法是：扫描根目录下第一层文件夹名。

如果扫描的是：

```text
D:\AI Project
```

这没问题，结构是：

```text
资料类型
  项目名
    文件
```

但如果用户选择的是单个项目目录，例如：

```text
D:\AI Project\BettaFish
```

当前逻辑可能会把 `docs`、`tasks` 等当成项目名。

请优化扫描脚本：

如果扫描根目录本身看起来像单个项目，则项目名应使用扫描根目录名称。

例如 root 是：

```text
D:\AI Project\BettaFish
```

导入结构应是：

```text
操作指南
  BettaFish
    docs
      README.md
```

而不是：

```text
操作指南
  docs
    README.md
```

建议实现方式：

1. 增加内部判断：

```text
single_project_mode
```

2. 判断条件可以简单一点：

如果 root 目录中存在以下任一文件/目录，认为它是单项目根目录：

```text
README.md
package.json
pyproject.toml
.git
docs
src
app
tasks
```

3. 单项目模式下：

```text
project_name = root 文件夹名
subs = 相对路径中除文件名外的目录
```

4. 多项目模式下保持原逻辑：

```text
project_name = root 下第一层文件夹
subs = 相对路径中第一层之后、文件名之前的目录
```

---

### 5. 弹窗统计不要乱码

继续保持 task04 修复后的中文显示效果。

如果调用 subprocess，请确保 stdout/stderr 解码稳定。

优先使用：

```python
encoding="utf-8"
errors="replace"
```

如果 Windows 仍乱码，再使用：

```python
env["PYTHONIOENCODING"] = "utf-8"
```

---

## 测试要求

### 1. GUI 启动测试

运行：

```powershell
cd "D:\AI Project\FolderTypeIndex"
python folder_type_index_v4_codex_import\folder_type_index.py
```

确认 GUI 能启动。

---

### 2. 选择 D:\AI Project 测试

点击：

```text
扫描生成导入 JSON
```

选择：

```text
D:\AI Project
```

确认：

1. 会弹确认框。
2. 确认框显示 `D:\AI Project`。
3. 点击“是”后能生成 JSON。
4. 成功提示不乱码。

---

### 3. 选择单项目目录测试

再点击：

```text
扫描生成导入 JSON
```

选择一个单独项目目录，例如：

```text
D:\AI Project\FolderTypeIndex
```

或其他实际存在项目目录。

确认导入结构里项目名使用该目录名，例如：

```text
FolderTypeIndex
```

而不是把 `docs`、`tasks` 当成项目名。

---

### 4. 导入测试

生成后点击：

```text
导入 Codex JSON
```

选择：

```text
D:\AI Project\FolderTypeIndex\folder_type_index_import.json
```

确认可以导入。

---

## Git 要求

可以提交：

```text
folder_type_index_v4_codex_import\folder_type_index.py
folder_type_index_v4_codex_import\folder_type_index.pyw
tools\generate_folder_type_index_import.py
tasks\task05.md
```

不要提交：

```text
folder_type_index_import.json
index_data.json
*.zip
```

提交信息建议：

```text
allow selecting scan root folder
```

---

## 完成后汇报格式

```text
Task05 完成情况：

1. 修改文件：
- ...

2. 新增功能：
- 点击“扫描生成导入 JSON”后可选择任意扫描目录

3. 单项目目录优化：
- 是否已实现
- 判断规则是什么

4. 测试结果：
- GUI 是否启动成功
- 选择 D:\AI Project 是否生成成功
- 选择单项目目录是否生成成功
- 成功弹窗中文是否正常
- 导入 Codex JSON 是否成功

5. Git：
- commit 是否成功
- push 是否成功

6. 安全确认：
- 没有修改 index_data.json
- 没有提交 folder_type_index_import.json
- 没有复制、移动、删除真实文件
- 没有修改被扫描目录中的真实内容
```
