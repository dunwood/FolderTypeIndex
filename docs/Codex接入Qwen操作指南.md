# Codex 接入阿里云百炼 Qwen 操作指南

> 适用场景：OpenAI Codex / Codex CLI 没有 ChatGPT 流量了，想临时或长期切换到阿里云百炼的 Qwen 模型继续用 Codex 做编程任务。  
> 本指南基于 Windows + PowerShell + VS Code + Codex CLI 环境整理。

---

## 0. 先说结论

Codex 可以通过配置文件接入阿里云百炼的 Qwen Responses 接口。

最终要改的是这个文件：

```text
C:\Users\Admin\.codex\config.toml
```

配置成功后，Codex 里会显示类似：

```text
model: qwen3.6-plus
directory: D:\AI Project\你的项目
```

以后无论在 PowerShell 里用 Codex CLI，还是在 VS Code 里用 Codex 面板，都会优先读取这个配置。

---

## 1. 准备工作

你需要准备：

1. 已经安装 Codex CLI；
2. 已经安装 Node.js / npm；
3. 已经有阿里云百炼 API Key；
4. Windows PowerShell；
5. VS Code，可选。

检查 Codex 是否可用：

```powershell
codex --version
```

如果 Codex 提示升级，建议升级：

```powershell
npm install -g @openai/codex
```

或在 Codex 弹窗里选择：

```text
1. Update now
```

---

## 2. 获取阿里云百炼 API Key

进入阿里云百炼控制台，创建 API Key。

注意：

```text
不要把真实 API Key 发给别人，也不要发到 ChatGPT 对话里。
```

如果已经不小心贴出来了，建议立刻去阿里云百炼后台删除旧 Key，重新生成一个新的。

---

## 3. 设置 Windows 环境变量

在 PowerShell 里执行：

```powershell
setx DASHSCOPE_API_KEY "你的百炼API Key"
```

例如：

```powershell
setx DASHSCOPE_API_KEY "sk-xxxxxxxxxxxxxxxx"
```

### 引号要不要？

建议保留引号：

```powershell
setx DASHSCOPE_API_KEY "XXX"
```

引号不会被保存进 Key，它只是告诉 PowerShell 这一整段是字符串。

---

## 4. 重要坑：setx 对当前窗口不生效

`setx` 设置的是“以后新打开的 PowerShell 窗口”的环境变量。

所以你刚设置完，直接执行：

```powershell
echo $env:DASHSCOPE_API_KEY
```

可能什么都看不到。

### 解决办法 A：重新打开 PowerShell

关闭当前 PowerShell，重新打开，再执行：

```powershell
echo $env:DASHSCOPE_API_KEY
```

如果显示 `sk-...`，说明成功。

### 解决办法 B：当前窗口临时设置

如果不想重开 PowerShell，可以在当前窗口执行：

```powershell
$env:DASHSCOPE_API_KEY="你的百炼API Key"
```

然后检查：

```powershell
echo $env:DASHSCOPE_API_KEY
```

---

## 5. 测试阿里云百炼接口是否通

先不要急着配置 Codex，先测试 API Key 和网络是否正常。

### 5.1 测试网络端口

```powershell
Test-NetConnection dashscope.aliyuncs.com -Port 443
```

看到：

```text
TcpTestSucceeded : True
```

说明网络能连上阿里云百炼服务器。

---

### 5.2 用 curl 测试模型接口

建议用 curl，并强制 IPv4：

```powershell
curl.exe -4 -sS -m 30 `
  -o NUL `
  -w "HTTP_CODE=%{http_code} TIME=%{time_total}`n" `
  -H "Authorization: Bearer $env:DASHSCOPE_API_KEY" `
  "https://dashscope.aliyuncs.com/compatible-mode/v1/models"
```

如果返回：

```text
HTTP_CODE=200 TIME=4.189930
```

说明：

```text
API Key 有效
网络正常
接口地址正确
```

### 常见状态码含义

```text
200 = 成功
401 = API Key 错误或没有读到环境变量
403 = 权限问题
404 = 地址写错
000 = 网络、代理、防火墙或超时问题
```

---

## 6. PowerShell 乱码问题

如果你用中文输出，例如：

```powershell
-w "HTTP状态码: %{http_code} 总耗时: %{time_total}秒`n"
```

可能出现乱码：

```text
鎬昏€楁椂...
```

不用管，换成英文输出即可：

```powershell
-w "HTTP_CODE=%{http_code} TIME=%{time_total}`n"
```

---

## 7. 打开 Codex 配置文件

执行：

```powershell
mkdir $env:USERPROFILE\.codex -Force
notepad $env:USERPROFILE\.codex\config.toml
```

在你的电脑上，这个路径通常是：

```text
C:\Users\Admin\.codex\config.toml
```

---

## 8. 写入 Qwen 配置

如果你只想先跑通，推荐使用 `qwen3.6-plus`。

把 `config.toml` 开头改成：

```toml
model_provider = "dashscope"
model = "qwen3.6-plus"

[model_providers.dashscope]
name = "Alibaba Cloud Model Studio / DashScope"
base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
env_key = "DASHSCOPE_API_KEY"
wire_api = "responses"

[windows]
sandbox = "elevated"

[plugins."github@openai-curated"]
enabled = true
```

保存后关闭记事本。

---

## 9. 如果原配置文件里已有项目记录怎么办？

你可能原来已经有很多：

```toml
[projects.'D:\AI Project\folderindex']
trust_level = "trusted"
```

这些是 Codex 对项目目录的信任记录。

如果你熟悉 TOML，可以保留它们。

如果文件已经乱了，比如出现：

```toml
trust_level = "trusted"t']
```

这种明显错误，建议直接重写成最小干净配置：

```powershell
@'
model_provider = "dashscope"
model = "qwen3.6-plus"

[model_providers.dashscope]
name = "Alibaba Cloud Model Studio / DashScope"
base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
env_key = "DASHSCOPE_API_KEY"
wire_api = "responses"

[windows]
sandbox = "elevated"

[plugins."github@openai-curated"]
enabled = true
'@ | Set-Content -Encoding UTF8 $env:USERPROFILE\.codex\config.toml
```

这样会删掉旧的项目授权记录，但不影响项目文件本身。下次进入项目时，Codex 会重新问你是否信任目录。

---

## 10. 检查配置文件

执行：

```powershell
type $env:USERPROFILE\.codex\config.toml
```

确认能看到：

```toml
model_provider = "dashscope"
model = "qwen3.6-plus"

[model_providers.dashscope]
base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
env_key = "DASHSCOPE_API_KEY"
wire_api = "responses"
```

---

## 11. 启动 Codex CLI

先进入具体项目目录，再启动 Codex。

例如：

```powershell
cd "D:\AI Project\folderindex"
codex
```

进入后，如果问你是否信任目录：

```text
Do you trust the contents of this directory?
1. Yes, continue
2. No, quit
```

选择：

```text
1. Yes, continue
```

一般直接按 Enter 就是第 1 项。

---

## 12. 判断是否接入成功

进入 Codex 后，顶部应该显示类似：

```text
OpenAI Codex (v0.128.0)

model:     qwen3.6-plus
directory: D:\AI Project\folderindex
```

底部也可能显示：

```text
qwen3.6-plus default
```

这说明 Codex 已经用上阿里云百炼 Qwen 了。

可以测试一句：

```text
请只回答一句话：你现在是否可以正常工作？
```

如果回复：

```text
是的，我可以正常工作。
```

说明已经跑通。

---

## 13. 重要区别：PowerShell 命令、Codex 自然语言、Codex slash 指令

这是今天最容易踩的坑。

你要分清楚三种输入环境：

```text
PowerShell 提示行：可以输入 codex / codex resume --last / code .
Codex 提示符 ›：主要输入自然语言任务，也可以输入 /resume 这类 slash 指令
VS Code Codex 面板：主要输入自然语言任务，也可能支持 /resume 等界面内指令
```

---

### 13.1 看到这个，说明你在 PowerShell

```powershell
PS C:\Users\Admin>
```

这时先输入下面这句，进入你的项目目录：

```powershell
cd "D:\AI Project\folderindex"
```

进入后，提示行会变成类似：

```powershell
PS D:\AI Project\folderindex>
```

然后根据你的目的，三选一：

```powershell
codex                # 新开 Codex，或者
codex resume --last  # 恢复最近一次 Codex，或者
code .               # 打开 VS Code
```

注意：上面三条不是连续都要执行，而是三选一。

---

### 13.2 看到这个，说明你已经在 Codex 里面

```text
›
```

这时不要再输入 PowerShell 命令，例如：

```text
codex
codex resume --last
cd "D:\AI Project\folderindex"
code .
```

这些都不应该在 `›` 下面输入。

原因是：你已经进入 Codex 了。  
如果再输入 `codex resume --last`，Codex 会把它当成一个“要执行的任务”，可能会出现“Codex 套 Codex”的嵌套执行问题。

---

### 13.3 进入 Codex 后，可以输入什么？

进入 Codex 后，主要输入自然语言任务，例如：

```text
请先只读取项目结构，不要修改文件。
```

或者：

```text
请检查当前项目是否有未提交改动，只列出文件，不要修改。
```

---

### 13.4 那进入 Codex 后还能不能用 / 指令？

可以。Codex CLI 进入 `›` 模式后，支持 slash commands，也就是以 `/` 开头的命令。

例如：

```text
/resume
```

意思是：在 Codex 里面打开已保存会话列表，然后选择一个会话恢复。

注意它和 PowerShell 里的命令不是一回事：

```powershell
codex resume --last
```

这是 PowerShell 里的 Codex 子命令。

而：

```text
/resume
```

这是 Codex 里面的 slash command。

---

### 13.5 最容易混淆的错误

错误理解：

```text
我已经输入 codex 进入 Codex 了，所以在 › 下输入 resume --last 就能恢复记忆。
```

这是错的。

在 `›` 下输入：

```text
resume --last
```

Codex 会把它当成普通自然语言/任务文本，而不是恢复命令。

正确做法有两个：

#### 方式 A：还没进入 Codex，在 PowerShell 里恢复

```powershell
cd "D:\AI Project\folderindex"
codex resume --last
```

#### 方式 B：已经进入 Codex，在 `›` 下使用 slash 指令

```text
/resume
```

然后从列表里选择要恢复的会话。

---

### 13.6 一句话记忆

```text
看到 PS：用 codex resume --last。
看到 ›：用 /resume，或者直接输入自然语言任务。
不要在 › 下输入 codex resume --last。
不要在 › 下输入 resume --last。
```


## 14. 断线后如何重新进入 Codex

### 14.1 重新开一个新会话

在 PowerShell 里：

```powershell
cd "D:\AI Project\folderindex"
codex
```

### 14.2 恢复最近一次会话

在 PowerShell 里：

```powershell
cd "D:\AI Project\folderindex"
codex resume --last
```

注意：`codex resume --last` 必须在 PowerShell 里输入，不是在 Codex 对话框里输入。

### 14.3 在 Codex 里面恢复会话

如果你已经看到：

```text
›
```

说明已经在 Codex 里面。此时不要输入 `codex resume --last`，可以尝试 slash command：

```text
/resume
```

---

## 15. 如果恢复错了目录怎么办？

如果你在这里执行：

```powershell
PS C:\Users\Admin> codex resume --last
```

Codex 会恢复用户目录 `C:\Users\Admin` 下的会话，界面显示：

```text
directory: ~
```

这不是你的项目目录。

正确做法是先进入项目目录：

```powershell
cd "D:\AI Project\folderindex"
codex resume --last
```

---

## 16. 在 VS Code 里使用 Codex

不需要先在 PowerShell 里执行 `codex`。

### 正确逻辑

```text
PowerShell 里执行 codex = 终端版 Codex
VS Code 里打开 Codex 面板 = VS Code 版 Codex
```

二者是两个入口，不需要同时开。

### VS Code 使用方法

打开 VS Code，然后：

```text
文件 → 打开文件夹 → 选择你的项目文件夹
```

例如：

```text
D:\AI Project\folderindex
```

然后打开左侧 Codex 面板。

VS Code 里的 Codex 也会读取同一个配置：

```text
C:\Users\Admin\.codex\config.toml
```

所以模型仍然应该是：

```text
qwen3.6-plus
```

---

## 17. 从 PowerShell 打开 VS Code

如果你已经确认要打开某个项目，可以执行：

```powershell
cd "D:\AI Project\你的项目"
code .
```

但是要特别小心：

```text
不要误打开原始项目。
不要在错误项目里让 Codex 改代码。
```

---

## 18. 保护原项目：强烈建议先复制副本

如果你原来的项目还能用，不要直接让 Codex 在原项目上改。

比如原项目是：

```text
D:\AI Project\folderindex
```

可以先复制一个测试副本：

```powershell
cd "D:\AI Project"
Copy-Item -Recurse -Force ".\folderindex" ".\folderindex_fileindex_test"
code ".\folderindex_fileindex_test"
```

然后只在副本里让 Codex 修改。

---

## 19. 让 Codex 先读项目，不要马上改

进入 Codex 后，先让它只读：

```text
请先只读取项目结构，不要修改文件。告诉我这个项目当前的入口文件、主要模块和运行方式。
```

确认它读的是正确目录，再让它给方案：

```text
请先不要修改代码，先分析当前架构，并给出最小改造方案。
```

最后才让它执行：

```text
按刚才的最小方案执行第一阶段，只修改 database.py，不要修改 main.py。
```

---

## 20. 复杂任务要拆开

不要一次让 Codex 同时改数据库、GUI、测试、文档。

推荐拆成：

```text
第一阶段：只改 database.py
第二阶段：只改 main.py
第三阶段：运行测试
第四阶段：整理文档
```

这样更安全，也更容易回滚。

---

## 21. 让 Codex 停止当前任务

如果 Codex 一直运行，或者你发现目录不对：

先按：

```text
Esc
```

如果还不停，再按：

```text
Ctrl + C
```

然后让它只检查状态：

```text
暂停执行，不要再修改任何文件。请只告诉我目前是否已经实际修改了哪些文件。只检查，不要修复。
```

---

## 22. 检查项目是否被改动

如果项目是 Git 仓库，执行：

```powershell
cd "D:\AI Project\folderindex"
git status
```

如果不是 Git 仓库，可以查最近修改文件：

```powershell
cd "D:\AI Project\folderindex"
Get-ChildItem -Recurse | Sort-Object LastWriteTime -Descending | Select-Object -First 20 FullName, LastWriteTime
```

重点看有没有：

```text
database.py
main.py
folder_index.db
```

---

## 23. 切换到 qwen3-coder-plus

确认 `qwen3.6-plus` 能正常工作后，可以尝试代码模型。

打开配置文件：

```powershell
notepad $env:USERPROFILE\.codex\config.toml
```

把：

```toml
model = "qwen3.6-plus"
```

改成：

```toml
model = "qwen3-coder-plus"
```

保存后重新启动 Codex。

如果不稳定，再切回：

```toml
model = "qwen3.6-plus"
```

---

## 24. 切回 OpenAI / ChatGPT 大模型

打开配置文件：

```powershell
notepad $env:USERPROFILE\.codex\config.toml
```

把 Qwen 配置改成最简 OpenAI 配置：

```toml
model = "gpt-5.5"

[windows]
sandbox = "elevated"

[plugins."github@openai-curated"]
enabled = true
```

保存后重新启动 Codex。

如果你的账号暂时没有 `gpt-5.5`，可以换成你能用的 OpenAI Codex 模型。

---

## 25. 建议做两个配置文件，一键切换

可以准备两个文件：

```text
C:\Users\Admin\.codex\config.qwen.toml
C:\Users\Admin\.codex\config.openai.toml
```

### 切到 Qwen

```powershell
Copy-Item $env:USERPROFILE\.codex\config.qwen.toml $env:USERPROFILE\.codex\config.toml -Force
```

### 切到 OpenAI

```powershell
Copy-Item $env:USERPROFILE\.codex\config.openai.toml $env:USERPROFILE\.codex\config.toml -Force
```

切换后重新打开 Codex。

---

## 26. 今天踩过的坑总结

### 坑 1：API Key 设置了但 echo 为空

原因：

```text
setx 对当前 PowerShell 窗口不生效。
```

解决：

```powershell
$env:DASHSCOPE_API_KEY="你的百炼API Key"
```

或重新打开 PowerShell。

---

### 坑 2：Invoke-RestMethod 一直卡住

可以换成：

```powershell
curl.exe -4 -sS -m 30 `
  -o NUL `
  -w "HTTP_CODE=%{http_code} TIME=%{time_total}`n" `
  -H "Authorization: Bearer $env:DASHSCOPE_API_KEY" `
  "https://dashscope.aliyuncs.com/compatible-mode/v1/models"
```

---

### 坑 3：中文 curl 输出乱码

换成英文输出：

```text
HTTP_CODE
TIME
```

---

### 坑 4：进入 Codex 后误以为 resume --last 可以恢复

看到：

```text
›
```

说明你已经在 Codex 里面。

这时不要输入：

```text
codex
codex resume --last
resume --last
cd ...
```

正确区分：

```text
PowerShell 里：codex resume --last
Codex 里面：/resume
自然语言任务：继续刚才的分析 / 请检查当前项目状态
```

如果你在 `›` 下输入 `codex resume --last`，就会变成“让 Codex 去执行 Codex”，容易卡住或嵌套。

如果你在 `›` 下输入 `resume --last`，它也不会等同于恢复命令，只会被当成普通输入。

### 坑 5：在错误目录恢复会话

如果在：

```powershell
PS C:\Users\Admin>
```

执行：

```powershell
codex resume --last
```

恢复的是用户目录，不是项目目录。

正确：

```powershell
cd "D:\AI Project\folderindex"
codex resume --last
```

---

### 坑 6：误让 Codex 在原项目里改代码

如果原项目已经能用，先复制副本：

```powershell
cd "D:\AI Project"
Copy-Item -Recurse -Force ".\folderindex" ".\folderindex_fileindex_test"
```

然后在副本里改。

---

### 坑 7：config.toml 被写乱

如果出现明显残缺内容，直接重写最小配置：

```powershell
@'
model_provider = "dashscope"
model = "qwen3.6-plus"

[model_providers.dashscope]
name = "Alibaba Cloud Model Studio / DashScope"
base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
env_key = "DASHSCOPE_API_KEY"
wire_api = "responses"

[windows]
sandbox = "elevated"

[plugins."github@openai-curated"]
enabled = true
'@ | Set-Content -Encoding UTF8 $env:USERPROFILE\.codex\config.toml
```

---

## 27. 最小成功流程

如果只想照抄最短流程：

```powershell
setx DASHSCOPE_API_KEY "你的百炼API Key"
```

重新打开 PowerShell，或当前窗口执行：

```powershell
$env:DASHSCOPE_API_KEY="你的百炼API Key"
```

测试：

```powershell
curl.exe -4 -sS -m 30 `
  -o NUL `
  -w "HTTP_CODE=%{http_code} TIME=%{time_total}`n" `
  -H "Authorization: Bearer $env:DASHSCOPE_API_KEY" `
  "https://dashscope.aliyuncs.com/compatible-mode/v1/models"
```

写入配置：

```powershell
@'
model_provider = "dashscope"
model = "qwen3.6-plus"

[model_providers.dashscope]
name = "Alibaba Cloud Model Studio / DashScope"
base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
env_key = "DASHSCOPE_API_KEY"
wire_api = "responses"

[windows]
sandbox = "elevated"

[plugins."github@openai-curated"]
enabled = true
'@ | Set-Content -Encoding UTF8 $env:USERPROFILE\.codex\config.toml
```

进入项目：

```powershell
cd "D:\AI Project\你的项目"
codex
```

测试：

```text
请只回答一句话：你现在是否可以正常工作？
```

看到模型显示：

```text
qwen3.6-plus
```

就成功了。

---

## 28. 最后提醒

1. 不要把 API Key 发给别人；
2. 不要在原项目上直接做大改；
3. 看到 `PS` 才能输入 PowerShell 命令；
4. 看到 `›` 就只输入自然语言任务；
5. Codex 进入项目后，先让它只读项目结构，再让它给方案，最后才让它改代码；
6. 复杂任务一定拆阶段执行。
