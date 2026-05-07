# FolderTypeIndex v4 - Codex 导入版

这是一个 GUI 版“按类型重组的项目文件超链接索引树”。

## 运行

优先双击：

```text
启动 FolderTypeIndex.vbs
```

如果要看错误日志，双击：

```text
run_debug.bat
```

## 数据文件

索引数据保存在同目录：

```text
index_data.json
```

备份这个文件，就等于备份索引树。

## Codex 导入

本版新增：

```text
导入 Codex JSON
生成导入模板
```

Codex 只需要扫描你的项目目录，生成一个 JSON 文件，然后在软件里点“导入 Codex JSON”。

JSON 格式：

```json
{
  "version": 1,
  "items": [
    {
      "tree_path": ["操作指南", "AI项目教练", "安装与环境"],
      "name": "安装指南.md",
      "type": "文件链接",
      "path": "D:\\AI Project\\AI项目教练\\docs\\安装指南.md",
      "url": "",
      "note": "安装与环境配置说明"
    }
  ]
}
```

支持节点类型：

```text
分类
文件链接
文件夹链接
网址
备注
```

导入只会新增/更新索引，不会移动、复制或删除真实文件。
