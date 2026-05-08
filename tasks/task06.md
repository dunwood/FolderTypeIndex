# task06：修复扫描子目录分组逻辑，并重新设计 GUI 界面

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

当前已经完成：

1. GUI 已支持“扫描生成导入 JSON”
2. GUI 已支持选择任意扫描目录
3. 扫描后可手动点击“导入 Codex JSON”
4. 不自动修改 `index_data.json`

---

## 本任务目标

本任务做两件事：

### 目标 A：修复扫描子目录时的项目根识别问题

当前如果用户直接扫描：

```text
D:\AI Project\FolderTypeIndex\docs
```

导入后会错误地把：

```text
Codex接入Qwen操作指南.md
FolderTypeIndex_操作指南.md
USER_GUIDE.md
```

这些文件名本身当成分类节点，或者把 `docs` 误当成项目名。

正确结果应该是：

```text
操作指南
  FolderTypeIndex
    docs
      Codex接入Qwen操作指南.md
      FolderTypeIndex_操作指南.md
      USER_GUIDE.md
```

也就是说：

- 扫描项目内子目录时，仍应识别真正的项目根目录
- 项目名应是 `FolderTypeIndex`
- `docs` 应作为项目下子目录，而不是项目名，更不能把文件名建成分类

---

### 目标 B：重新设计 GUI，使界面更清爽、现代、好用

当前 GUI 虽然功能能用，但界面较丑，布局拥挤，视觉层次差。

本任务不是只修小 bug，而是做一次**轻量级 GUI 改版**：

- 保留原有核心功能
- 不大改数据结构
- 不影响已有 JSON 读写
- 重点优化界面布局、按钮区、信息层次、可读性和易用性

---

## 强制安全规则

必须遵守：

1. 不复制真实文件
2. 不移动真实文件
3. 不删除真实文件
4. 不修改被扫描目录中的任何真实文件
5. 不自动修改 `index_data.json`
6. 不自动导入生成结果
7. 不提交真实生成的 `folder_type_index_import.json`
8. 不破坏已有导入 / 导出 / 扫描功能
9. 不大规模重写整个程序架构
10. 只在当前项目内修改 GUI 与扫描逻辑

---

## A 部分：修复扫描子目录时的项目根识别

### 1. 问题说明

如果用户扫描的是某个项目内的子目录，例如：

```text
D:\AI Project\FolderTypeIndex\docs
```

脚本不应把 `docs` 当项目名，也不应把文件名当分类节点。

应尽量向上识别真正的项目根。

---

### 2. 项目根识别规则

请在扫描脚本中增加“向上寻找项目根目录”的逻辑。

建议函数：

```text
find_project_root(scan_root)
```

从用户选中的目录开始，向上查找，直到找到疑似项目根目录。

可使用如下判断条件：如果某个目录中存在以下任一文件或目录，则可视为项目根候选：

```text
.git
README.md
LICENSE
package.json
pyproject.toml
docs
src
app
tasks
```

优先规则建议：

1. 如果当前目录本身包含多个项目，则按多项目模式处理
2. 如果当前目录看起来是单项目根目录，则项目名 = 当前目录名
3. 如果当前目录只是项目内子目录，则向上找到最近的项目根目录
4. 找不到明确项目根时，再退回当前旧逻辑

---

### 3. 扫描结果结构要求

#### 场景 1：扫描多项目目录

例如扫描：

```text
D:\AI Project
```

结果仍应是：

```text
资料类型
  FolderTypeIndex
    docs
      USER_GUIDE.md
  BettaFish
    docs
      README.md
```

#### 场景 2：扫描单项目根目录

例如扫描：

```text
D:\AI Project\FolderTypeIndex
```

结果应是：

```text
资料类型
  FolderTypeIndex
    docs
      USER_GUIDE.md
    tasks
      task05.md
```

#### 场景 3：扫描项目内子目录

例如扫描：

```text
D:\AI Project\FolderTypeIndex\docs
```

结果仍应是：

```text
资料类型
  FolderTypeIndex
    docs
      USER_GUIDE.md
      FolderTypeIndex_操作指南.md
```

而不是：

```text
资料类型
  docs
    USER_GUIDE.md
```

也不是：

```text
资料类型
  USER_GUIDE.md
    USER_GUIDE.md
```

---

### 4. 文件叶子节点必须正确

继续确保生成 JSON 时：

- `tree_path` 只放分类路径
- `name` 放文件名
- 文件叶子节点类型为：

```text
文件链接
```

不要把文件名放进 `tree_path`。

---

## B 部分：重新设计 GUI 界面

### 1. 改版原则

目标是“更像正式工具”，而不是临时 Tkinter 原型。

要求：

1. 保留现有全部核心功能
2. 界面更整洁
3. 信息层次更清楚
4. 操作按钮更集中
5. 左右布局更合理
6. 常用功能优先展示
7. 不要为了美观破坏稳定性

---

### 2. 建议新布局

推荐改为三块：

#### 顶部工具栏

集中放主要操作按钮，例如：

```text
新建一级分类
扫描生成导入 JSON
导入 Codex JSON
生成导入模板
导出 Markdown
```

要求：

- 按钮高度统一
- 间距更均匀
- 常用按钮靠前
- 次要按钮靠后

可以加一个简洁标题：

```text
FolderTypeIndex
按资料类型重组的项目文件超链接索引树
```

---

#### 左侧：索引树区域

保留索引树，但做这些优化：

1. 区域标题更明显，例如：

```text
索引树
```

2. 树区域占比略大
3. 列宽更合理
4. “类型”列不要过于拥挤
5. 可以保留“本地路径”列，但不要让界面挤爆
6. 左下角的“添加子 / 添加文件 / 添加文件夹 / 添加网址 / 上移 / 下移 / 标记移 / 移动到”重新排版，不要一排挤满

建议改成两排按钮，或分组摆放。

---

#### 右侧：详情 / 编辑区

保留：

```text
名称
类型
本地路径
网址
备注
```

但做以下优化：

1. 标签对齐
2. 输入框宽度更合理
3. 备注框更大
4. “浏览文件 / 浏览文件夹”按钮位置更清楚
5. “保存修改 / 打开资源 / 删除索引节点”做成底部操作区
6. 可以加区域标题：

```text
详情 / 编辑
```

---

### 3. 视觉优化要求

即使仍使用 Tkinter，也请尽量优化：

1. 统一字体大小
2. 适度增大按钮和输入框高度
3. 合理留白
4. 让标题、分区、正文层次明显
5. 避免所有控件都挤在一起
6. 窗口默认尺寸适当放大
7. 调整行高、列宽、padding

如果当前项目已使用 ttk，请优先用 ttk 风格优化。

---

### 4. 可用性优化建议

如果改动成本不高，可以顺手做以下小优化：

1. 窗口最下方状态栏显示当前数据文件路径
2. 点击树节点时，右侧编辑区刷新更直观
3. 顶部扫描按钮文案可简化为：

```text
扫描生成导入
```

4. 导入完成 / 扫描完成的弹窗文案更清晰
5. 保持中文显示正常，不要乱码

---

### 5. 兼容性要求

必须保持：

1. 原有 `index_data.json` 可正常读取
2. 原有“导入 Codex JSON”仍可用
3. 原有“生成导入模板”仍可用
4. 原有“导出 Markdown”仍可用
5. 原有双击打开文件/文件夹/网址仍可用
6. 原有扫描按钮仍可生成导入 JSON
7. 原有任意目录扫描仍可用

---

## 测试要求

### 1. GUI 启动测试

运行：

```powershell
cd "D:\AI Project\FolderTypeIndex"
python folder_type_index_v4_codex_import\folder_type_index.py
```

确认：

- GUI 可正常启动
- 新界面布局明显改善
- 按钮功能都还在

---

### 2. 扫描 D:\AI Project 测试

选择：

```text
D:\AI Project
```

确认：

- 能生成导入 JSON
- 成功弹窗正常
- 导入后结构正常

---

### 3. 扫描单项目根目录测试

选择：

```text
D:\AI Project\FolderTypeIndex
```

确认：

- 项目名为 `FolderTypeIndex`
- `docs`、`tasks` 作为其下子目录

---

### 4. 扫描项目子目录测试

选择：

```text
D:\AI Project\FolderTypeIndex\docs
```

确认：

- 项目名仍为 `FolderTypeIndex`
- `docs` 作为子目录
- `Codex接入Qwen操作指南.md`、`FolderTypeIndex_操作指南.md` 作为文件链接，不再变成分类节点

---

### 5. 导入测试

点击：

```text
导入 Codex JSON
```

导入：

```text
D:\AI Project\FolderTypeIndex\folder_type_index_import.json
```

确认：

- 可导入
- 文件节点类型正确
- 双击能打开真实文件

---

## Git 要求

可以提交：

```text
folder_type_index_v4_codex_import\folder_type_index.py
folder_type_index_v4_codex_import\folder_type_index.pyw
tools\generate_folder_type_index_import.py
tasks\task06.md
```

不要提交：

```text
folder_type_index_import.json
index_data.json
*.zip
```

提交信息建议：

```text
redesign gui and fix project root detection
```

---

## 完成后汇报格式

```text
Task06 完成情况：

1. 修改文件：
- ...

2. 子目录扫描修复：
- 项目根识别是否已修复
- 识别规则是什么
- 扫描 docs 子目录时结果是否正确

3. GUI 改版：
- 做了哪些布局与视觉优化
- 哪些按钮位置调整了
- 是否保持原功能可用

4. 测试结果：
- GUI 是否启动成功
- 扫描 D:\AI Project 是否成功
- 扫描 FolderTypeIndex 根目录是否成功
- 扫描 FolderTypeIndex\docs 是否成功
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
