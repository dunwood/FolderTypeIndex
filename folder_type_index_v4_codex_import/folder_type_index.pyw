# -*- coding: utf-8 -*-
"""
FolderTypeIndex - 按类型重组的项目文件超链接索引树

运行方式：
    python folder_type_index.py

数据文件：
    默认保存在本脚本同目录下的 index_data.json

说明：
    这是一个本地 GUI 工具，用“索引树”重新组织真实项目文件。
    它不会移动、复制、删除你的真实文件；删除节点只删除索引记录。
"""

import json
import os
import sys
import ctypes
import uuid
import webbrowser
from pathlib import Path
from tkinter import Tk, StringVar, Text, END, BOTH, LEFT, RIGHT, X, Y, N, S, E, W, filedialog, messagebox, simpledialog
from tkinter import ttk

APP_TITLE = "FolderTypeIndex - 类型索引树"
DATA_FILE = Path(__file__).with_name("index_data.json")
NODE_TYPES = ["分类", "文件夹链接", "文件链接", "网址", "备注"]


def enable_high_dpi_awareness():
    """避免 Windows 高缩放下 Tkinter 界面被系统位图拉伸而变模糊。"""
    if sys.platform != "win32":
        return
    try:
        # Windows 10+: Per-monitor DPI aware，最清晰。
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
        return
    except Exception:
        pass
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass


def apply_readable_fonts(root):
    """统一字体，避免默认 Tk 字体在中文界面里发虚或太小。"""
    base_font = ("Microsoft YaHei UI", 10)
    title_font = ("Microsoft YaHei UI", 16, "bold")
    heading_font = ("Microsoft YaHei UI", 10, "bold")
    root.option_add("*Font", base_font)
    try:
        style = ttk.Style(root)
        if "vista" in style.theme_names():
            style.theme_use("vista")
        style.configure(".", font=base_font)
        style.configure("TLabel", font=base_font)
        style.configure("TButton", font=base_font, padding=(8, 4))
        style.configure("TEntry", font=base_font)
        style.configure("TCombobox", font=base_font)
        style.configure("Treeview", font=base_font, rowheight=28)
        style.configure("Treeview.Heading", font=heading_font)
        style.configure("Title.TLabel", font=title_font)
    except Exception:
        pass

TYPE_ICON = {
    "分类": "📁",
    "文件夹链接": "🗂",
    "文件链接": "📄",
    "网址": "🔗",
    "备注": "📝",
}


def new_id() -> str:
    return uuid.uuid4().hex[:12]


def default_data():
    root_id = "root"
    nodes = {
        root_id: {
            "id": root_id,
            "name": "索引根目录",
            "type": "分类",
            "path": "",
            "url": "",
            "note": "",
            "children": [],
        }
    }
    for name in ["操作指南", "文献资料", "部署资料", "实验数据", "Prompt资料"]:
        nid = new_id()
        nodes[nid] = {
            "id": nid,
            "name": name,
            "type": "分类",
            "path": "",
            "url": "",
            "note": "",
            "children": [],
        }
        nodes[root_id]["children"].append(nid)
    return {"version": 1, "root_id": root_id, "nodes": nodes}


class FolderTypeIndexApp:
    def __init__(self, master: Tk):
        self.master = master
        self.master.title(APP_TITLE)
        self.master.geometry("1280x760")
        self.data_path = DATA_FILE
        self.data = self.load_data()
        self.selected_id = None
        self.move_source_id = None
        self.search_var = StringVar()

        self.name_var = StringVar()
        self.type_var = StringVar(value="分类")
        self.path_var = StringVar()
        self.url_var = StringVar()
        self.status_var = StringVar(value=f"数据文件：{self.data_path}")

        self.build_ui()
        self.refresh_tree()

    def load_data(self):
        if DATA_FILE.exists():
            try:
                with DATA_FILE.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                if "root_id" in data and "nodes" in data:
                    return data
            except Exception as exc:
                messagebox.showwarning("读取失败", f"旧数据读取失败，将创建新索引。\n\n{exc}")
        return default_data()

    def save_data(self):
        with self.data_path.open("w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        self.status_var.set(f"已保存：{self.data_path}")

    def build_ui(self):
        self.master.columnconfigure(0, weight=3)
        self.master.columnconfigure(1, weight=2)
        self.master.rowconfigure(1, weight=1)

        top = ttk.Frame(self.master, padding=(10, 8))
        top.grid(row=0, column=0, columnspan=2, sticky=E + W)
        top.columnconfigure(1, weight=1)

        ttk.Label(top, text="FolderTypeIndex", style="Title.TLabel").grid(row=0, column=0, sticky=W, padx=(0, 16))
        search = ttk.Entry(top, textvariable=self.search_var)
        search.grid(row=0, column=1, sticky=E + W, padx=(0, 10))
        search.insert(0, "")
        search.bind("<KeyRelease>", lambda _e: self.refresh_tree())
        ttk.Button(top, text="新建一级分类", command=self.add_root_node).grid(row=0, column=2, padx=3)
        ttk.Button(top, text="导入 Codex JSON", command=self.import_codex_json).grid(row=0, column=3, padx=3)
        ttk.Button(top, text="生成导入模板", command=self.export_import_template).grid(row=0, column=4, padx=3)
        ttk.Button(top, text="导出 Markdown", command=self.export_markdown).grid(row=0, column=5, padx=3)

        left = ttk.Frame(self.master, padding=(10, 0, 5, 6))
        left.grid(row=1, column=0, sticky=N + S + E + W)
        left.columnconfigure(0, weight=1)
        left.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(left, columns=("type", "path", "url"), show="tree headings", selectmode="browse")
        self.tree.heading("#0", text="索引树")
        self.tree.heading("type", text="类型")
        self.tree.heading("path", text="本地路径")
        self.tree.heading("url", text="网址")
        self.tree.column("#0", width=360, stretch=True)
        self.tree.column("type", width=90, anchor="center")
        self.tree.column("path", width=320, stretch=True)
        self.tree.column("url", width=240, stretch=True)
        self.tree.grid(row=0, column=0, sticky=N + S + E + W)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.tree.bind("<Double-1>", lambda _e: self.open_selected())

        yscroll = ttk.Scrollbar(left, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=yscroll.set)
        yscroll.grid(row=0, column=1, sticky=N + S)

        actions = ttk.Frame(left)
        actions.grid(row=1, column=0, columnspan=2, sticky=E + W, pady=(8, 0))
        for idx in range(8):
            actions.columnconfigure(idx, weight=1)
        ttk.Button(actions, text="添加子节点", command=self.add_child_node).grid(row=0, column=0, sticky=E + W, padx=2)
        ttk.Button(actions, text="添加文件", command=self.add_file_node).grid(row=0, column=1, sticky=E + W, padx=2)
        ttk.Button(actions, text="添加文件夹", command=self.add_folder_node).grid(row=0, column=2, sticky=E + W, padx=2)
        ttk.Button(actions, text="添加网址", command=self.add_url_node).grid(row=0, column=3, sticky=E + W, padx=2)
        ttk.Button(actions, text="上移", command=lambda: self.move_sibling(-1)).grid(row=0, column=4, sticky=E + W, padx=2)
        ttk.Button(actions, text="下移", command=lambda: self.move_sibling(1)).grid(row=0, column=5, sticky=E + W, padx=2)
        ttk.Button(actions, text="标记移动", command=self.mark_move_source).grid(row=0, column=6, sticky=E + W, padx=2)
        ttk.Button(actions, text="移动到此处", command=self.move_to_selected_parent).grid(row=0, column=7, sticky=E + W, padx=2)

        right = ttk.Frame(self.master, padding=(8, 0, 10, 6))
        right.grid(row=1, column=1, sticky=N + S + E + W)
        right.columnconfigure(1, weight=1)
        right.rowconfigure(8, weight=1)

        ttk.Label(right, text="详情 / 编辑", font=("Microsoft YaHei UI", 13, "bold")).grid(row=0, column=0, columnspan=3, sticky=W, pady=(3, 8))

        ttk.Label(right, text="名称").grid(row=1, column=0, sticky=W, pady=4)
        ttk.Entry(right, textvariable=self.name_var).grid(row=1, column=1, columnspan=2, sticky=E + W, pady=4)

        ttk.Label(right, text="类型").grid(row=2, column=0, sticky=W, pady=4)
        ttk.Combobox(right, textvariable=self.type_var, values=NODE_TYPES, state="readonly").grid(row=2, column=1, columnspan=2, sticky=E + W, pady=4)

        ttk.Label(right, text="本地路径").grid(row=3, column=0, sticky=W, pady=4)
        ttk.Entry(right, textvariable=self.path_var).grid(row=3, column=1, sticky=E + W, pady=4)
        ttk.Button(right, text="浏览文件", command=self.browse_file_for_selected).grid(row=3, column=2, sticky=E + W, padx=(6, 0))
        ttk.Button(right, text="浏览文件夹", command=self.browse_folder_for_selected).grid(row=4, column=2, sticky=E + W, padx=(6, 0))

        ttk.Label(right, text="网址").grid(row=5, column=0, sticky=W, pady=4)
        ttk.Entry(right, textvariable=self.url_var).grid(row=5, column=1, columnspan=2, sticky=E + W, pady=4)

        ttk.Label(right, text="备注").grid(row=6, column=0, sticky=N + W, pady=4)
        self.note_text = Text(right, height=10, wrap="word", font=("Microsoft YaHei UI", 10))
        self.note_text.grid(row=6, column=1, columnspan=2, sticky=N + S + E + W, pady=4)

        btns = ttk.Frame(right)
        btns.grid(row=7, column=0, columnspan=3, sticky=E + W, pady=(8, 0))
        btns.columnconfigure(0, weight=1)
        btns.columnconfigure(1, weight=1)
        btns.columnconfigure(2, weight=1)
        ttk.Button(btns, text="保存修改", command=self.save_selected_detail).grid(row=0, column=0, sticky=E + W, padx=2)
        ttk.Button(btns, text="打开资源", command=self.open_selected).grid(row=0, column=1, sticky=E + W, padx=2)
        ttk.Button(btns, text="删除索引节点", command=self.delete_selected).grid(row=0, column=2, sticky=E + W, padx=2)

        tips = ttk.Label(
            right,
            text="说明：索引树只是超链接导航，不移动真实文件。删除节点只删除索引记录，不删除真实文件。双击左侧节点可打开绑定资源。",
            wraplength=430,
            foreground="#555",
        )
        tips.grid(row=8, column=0, columnspan=3, sticky=N + E + W, pady=(12, 0))

        bottom = ttk.Label(self.master, textvariable=self.status_var, anchor=W, padding=(10, 4))
        bottom.grid(row=2, column=0, columnspan=2, sticky=E + W)

    def get_node(self, node_id):
        return self.data["nodes"].get(node_id)

    def parent_of(self, child_id):
        for nid, node in self.data["nodes"].items():
            if child_id in node.get("children", []):
                return nid
        return None

    def display_name(self, node):
        icon = TYPE_ICON.get(node.get("type", "分类"), "•")
        return f"{icon} {node.get('name', '')}"

    def node_matches(self, node, keyword):
        if not keyword:
            return True
        text = " ".join([
            node.get("name", ""),
            node.get("type", ""),
            node.get("path", ""),
            node.get("url", ""),
            node.get("note", ""),
        ]).lower()
        return keyword.lower() in text

    def subtree_has_match(self, node_id, keyword):
        node = self.get_node(node_id)
        if not node:
            return False
        if self.node_matches(node, keyword):
            return True
        return any(self.subtree_has_match(cid, keyword) for cid in node.get("children", []))

    def refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        keyword = self.search_var.get().strip()
        root = self.get_node(self.data["root_id"])
        for child_id in root.get("children", []):
            self.insert_node("", child_id, keyword)
        if keyword:
            self.tree.heading("#0", text=f"索引树：搜索 {keyword}")
        else:
            self.tree.heading("#0", text="索引树")

    def insert_node(self, parent_item, node_id, keyword=""):
        if keyword and not self.subtree_has_match(node_id, keyword):
            return
        node = self.get_node(node_id)
        if not node:
            return
        item = self.tree.insert(
            parent_item,
            "end",
            iid=node_id,
            text=self.display_name(node),
            values=(node.get("type", ""), self.shorten(node.get("path", "")), self.shorten(node.get("url", ""))),
            open=True if keyword else False,
        )
        for cid in node.get("children", []):
            self.insert_node(item, cid, keyword)

    def shorten(self, text, limit=56):
        if not text:
            return ""
        return text if len(text) <= limit else text[: limit - 3] + "..."

    def on_select(self, _event=None):
        selected = self.tree.selection()
        if not selected:
            return
        self.selected_id = selected[0]
        node = self.get_node(self.selected_id)
        if not node:
            return
        self.name_var.set(node.get("name", ""))
        self.type_var.set(node.get("type", "分类"))
        self.path_var.set(node.get("path", ""))
        self.url_var.set(node.get("url", ""))
        self.note_text.delete("1.0", END)
        self.note_text.insert("1.0", node.get("note", ""))
        self.status_var.set(f"已选择：{node.get('name', '')}")

    def selected_or_root(self):
        return self.selected_id or self.data["root_id"]

    def create_node(self, parent_id, name, node_type="分类", path="", url="", note=""):
        nid = new_id()
        self.data["nodes"][nid] = {
            "id": nid,
            "name": name,
            "type": node_type,
            "path": path,
            "url": url,
            "note": note,
            "children": [],
        }
        self.data["nodes"][parent_id].setdefault("children", []).append(nid)
        self.save_data()
        self.refresh_tree()
        self.tree.selection_set(nid)
        self.tree.see(nid)
        self.on_select()
        return nid

    def add_root_node(self):
        name = simpledialog.askstring("新建一级分类", "请输入一级分类名称：", parent=self.master)
        if name:
            self.create_node(self.data["root_id"], name.strip(), "分类")

    def add_child_node(self):
        parent_id = self.selected_or_root()
        name = simpledialog.askstring("添加子节点", "请输入子节点名称：", parent=self.master)
        if name:
            self.create_node(parent_id, name.strip(), "分类")

    def add_file_node(self):
        parent_id = self.selected_or_root()
        path = filedialog.askopenfilename(title="选择要加入索引的文件")
        if path:
            name = Path(path).name
            self.create_node(parent_id, name, "文件链接", path=path)

    def add_folder_node(self):
        parent_id = self.selected_or_root()
        path = filedialog.askdirectory(title="选择要加入索引的文件夹")
        if path:
            name = Path(path).name or path
            self.create_node(parent_id, name, "文件夹链接", path=path)

    def add_url_node(self):
        parent_id = self.selected_or_root()
        url = simpledialog.askstring("添加网址", "请输入网址：", parent=self.master)
        if url:
            name = simpledialog.askstring("网址名称", "请输入显示名称：", parent=self.master) or url
            self.create_node(parent_id, name.strip(), "网址", url=url.strip())

    def save_selected_detail(self):
        if not self.selected_id:
            messagebox.showinfo("未选择", "请先在左侧选择一个节点。")
            return
        node = self.get_node(self.selected_id)
        if not node:
            return
        node["name"] = self.name_var.get().strip() or "未命名"
        node["type"] = self.type_var.get().strip() or "分类"
        node["path"] = self.path_var.get().strip()
        node["url"] = self.url_var.get().strip()
        node["note"] = self.note_text.get("1.0", END).rstrip()
        self.save_data()
        self.refresh_tree()
        try:
            self.tree.selection_set(self.selected_id)
            self.tree.see(self.selected_id)
        except Exception:
            pass

    def browse_file_for_selected(self):
        path = filedialog.askopenfilename(title="选择文件")
        if path:
            self.path_var.set(path)
            self.type_var.set("文件链接")
            if not self.name_var.get().strip():
                self.name_var.set(Path(path).name)

    def browse_folder_for_selected(self):
        path = filedialog.askdirectory(title="选择文件夹")
        if path:
            self.path_var.set(path)
            self.type_var.set("文件夹链接")
            if not self.name_var.get().strip():
                self.name_var.set(Path(path).name or path)

    def open_selected(self):
        if not self.selected_id:
            return
        node = self.get_node(self.selected_id)
        if not node:
            return
        path = node.get("path", "").strip()
        url = node.get("url", "").strip()
        try:
            if path:
                if os.path.exists(path):
                    if sys.platform.startswith("win"):
                        os.startfile(path)  # type: ignore[attr-defined]
                    elif sys.platform == "darwin":
                        os.system(f'open "{path}"')
                    else:
                        os.system(f'xdg-open "{path}"')
                    return
                messagebox.showwarning("路径不存在", f"这个路径不存在：\n{path}")
                return
            if url:
                webbrowser.open(url)
                return
            messagebox.showinfo("没有绑定资源", "这个节点没有绑定本地路径或网址。")
        except Exception as exc:
            messagebox.showerror("打开失败", str(exc))

    def delete_selected(self):
        if not self.selected_id:
            return
        if self.selected_id == self.data["root_id"]:
            return
        node = self.get_node(self.selected_id)
        if not node:
            return
        ok = messagebox.askyesno(
            "删除索引节点",
            f"确定删除索引节点“{node.get('name', '')}”及其子节点吗？\n\n注意：这只删除索引记录，不删除真实文件。",
        )
        if not ok:
            return
        parent_id = self.parent_of(self.selected_id)
        if parent_id:
            children = self.data["nodes"][parent_id].get("children", [])
            self.data["nodes"][parent_id]["children"] = [cid for cid in children if cid != self.selected_id]
        self.delete_subtree(self.selected_id)
        self.selected_id = None
        self.save_data()
        self.refresh_tree()
        self.clear_detail()

    def delete_subtree(self, node_id):
        node = self.get_node(node_id)
        if not node:
            return
        for cid in list(node.get("children", [])):
            self.delete_subtree(cid)
        if node_id != self.data["root_id"]:
            self.data["nodes"].pop(node_id, None)

    def clear_detail(self):
        self.name_var.set("")
        self.type_var.set("分类")
        self.path_var.set("")
        self.url_var.set("")
        self.note_text.delete("1.0", END)

    def move_sibling(self, direction):
        if not self.selected_id:
            return
        parent_id = self.parent_of(self.selected_id)
        if not parent_id:
            return
        children = self.data["nodes"][parent_id].get("children", [])
        idx = children.index(self.selected_id)
        new_idx = idx + direction
        if new_idx < 0 or new_idx >= len(children):
            return
        children[idx], children[new_idx] = children[new_idx], children[idx]
        self.save_data()
        self.refresh_tree()
        self.tree.selection_set(self.selected_id)
        self.tree.see(self.selected_id)

    def mark_move_source(self):
        if not self.selected_id:
            messagebox.showinfo("未选择", "请先选择要移动的节点。")
            return
        self.move_source_id = self.selected_id
        node = self.get_node(self.move_source_id)
        self.status_var.set(f"已标记待移动节点：{node.get('name', '')}。请选择目标父节点，再点“移动到此处”。")

    def is_descendant(self, maybe_child_id, maybe_parent_id):
        node = self.get_node(maybe_parent_id)
        if not node:
            return False
        for cid in node.get("children", []):
            if cid == maybe_child_id or self.is_descendant(maybe_child_id, cid):
                return True
        return False

    def move_to_selected_parent(self):
        if not self.move_source_id:
            messagebox.showinfo("没有待移动节点", "请先点“标记移动”。")
            return
        target_parent_id = self.selected_or_root()
        if target_parent_id == self.move_source_id or self.is_descendant(target_parent_id, self.move_source_id):
            messagebox.showwarning("不能移动", "不能把节点移动到自己或自己的子节点下面。")
            return
        old_parent = self.parent_of(self.move_source_id)
        if old_parent:
            old_children = self.data["nodes"][old_parent].get("children", [])
            self.data["nodes"][old_parent]["children"] = [cid for cid in old_children if cid != self.move_source_id]
        self.data["nodes"][target_parent_id].setdefault("children", []).append(self.move_source_id)
        moved_id = self.move_source_id
        self.move_source_id = None
        self.save_data()
        self.refresh_tree()
        self.tree.selection_set(moved_id)
        self.tree.see(moved_id)

    def normalize_node_type(self, raw_type, path="", url=""):
        text = (raw_type or "").strip().lower()
        if text in ["分类", "category", "folder", "目录", "索引文件夹"] and not path and not url:
            return "分类"
        if text in ["文件夹链接", "folder_link", "folderlink", "dir", "directory", "本地文件夹", "文件夹"]:
            return "文件夹链接"
        if text in ["文件链接", "file_link", "filelink", "file", "本地文件", "文件"]:
            return "文件链接"
        if text in ["网址", "url", "web", "link", "网页"]:
            return "网址"
        if text in ["备注", "note", "memo"]:
            return "备注"
        if url:
            return "网址"
        if path:
            try:
                return "文件夹链接" if os.path.isdir(path) else "文件链接"
            except Exception:
                return "文件链接"
        return "分类"

    def split_tree_path(self, value):
        if not value:
            return []
        if isinstance(value, list):
            return [str(x).strip() for x in value if str(x).strip()]
        text = str(value).strip()
        # 允许 Codex 用 “操作指南/AI项目/部署” 或 “操作指南 > AI项目 > 部署”
        for sep in [">", "|", "/"]:
            if sep in text:
                return [x.strip() for x in text.split(sep) if x.strip()]
        return [text] if text else []

    def find_child(self, parent_id, name=None, node_type=None, path=None, url=None):
        parent = self.get_node(parent_id)
        if not parent:
            return None
        norm_path = os.path.normcase(os.path.normpath(path)) if path else ""
        for cid in parent.get("children", []):
            node = self.get_node(cid)
            if not node:
                continue
            if path and node.get("path"):
                try:
                    if os.path.normcase(os.path.normpath(node.get("path", ""))) == norm_path:
                        return cid
                except Exception:
                    pass
            if url and node.get("url", "").strip() == url:
                return cid
            if name and node.get("name") == name and (not node_type or node.get("type") == node_type):
                return cid
        return None

    def ensure_category_path(self, parts):
        parent_id = self.data["root_id"]
        for part in parts:
            existing = self.find_child(parent_id, name=part, node_type="分类")
            if existing:
                parent_id = existing
                continue
            nid = new_id()
            self.data["nodes"][nid] = {
                "id": nid,
                "name": part,
                "type": "分类",
                "path": "",
                "url": "",
                "note": "",
                "children": [],
            }
            self.data["nodes"][parent_id].setdefault("children", []).append(nid)
            parent_id = nid
        return parent_id

    def apply_import_items(self, items):
        added = 0
        updated = 0
        skipped = 0
        for item in items:
            if not isinstance(item, dict):
                skipped += 1
                continue

            tree_path = self.split_tree_path(
                item.get("tree_path") or item.get("index_path") or item.get("parent_path") or item.get("分类路径")
            )
            name = str(item.get("name") or item.get("title") or item.get("名称") or "").strip()
            path = str(item.get("path") or item.get("local_path") or item.get("本地路径") or "").strip()
            url = str(item.get("url") or item.get("网址") or "").strip()
            note = str(item.get("note") or item.get("备注") or item.get("description") or "").strip()
            node_type = self.normalize_node_type(item.get("type") or item.get("kind") or item.get("类型"), path, url)

            if not name:
                if path:
                    name = Path(path).name or path
                elif url:
                    name = url
                else:
                    skipped += 1
                    continue

            # 纯分类节点：把 name 当作 tree_path 的下一层。
            if node_type == "分类" and not path and not url:
                self.ensure_category_path(tree_path + [name])
                added += 1
                continue

            parent_id = self.ensure_category_path(tree_path)
            existing = self.find_child(parent_id, name=name, node_type=node_type, path=path, url=url)
            if existing:
                node = self.get_node(existing)
                node["name"] = name
                node["type"] = node_type
                node["path"] = path
                node["url"] = url
                if note:
                    node["note"] = note
                updated += 1
            else:
                nid = new_id()
                self.data["nodes"][nid] = {
                    "id": nid,
                    "name": name,
                    "type": node_type,
                    "path": path,
                    "url": url,
                    "note": note,
                    "children": [],
                }
                self.data["nodes"][parent_id].setdefault("children", []).append(nid)
                added += 1
        self.save_data()
        self.refresh_tree()
        return added, updated, skipped

    def import_codex_json(self):
        in_path = filedialog.askopenfilename(
            title="导入 Codex 生成的索引 JSON",
            filetypes=[("JSON", "*.json"), ("All files", "*.*")],
        )
        if not in_path:
            return
        try:
            raw = Path(in_path).read_text(encoding="utf-8")
            data = json.loads(raw)
            if isinstance(data, list):
                items = data
            elif isinstance(data, dict):
                items = data.get("items") or data.get("nodes") or data.get("records") or []
            else:
                items = []
            if not isinstance(items, list):
                raise ValueError("JSON 中没有 items 数组。")
            added, updated, skipped = self.apply_import_items(items)
            messagebox.showinfo("导入完成", f"已导入：{in_path}\n\n新增：{added}\n更新/去重：{updated}\n跳过：{skipped}")
        except Exception as exc:
            messagebox.showerror("导入失败", f"无法导入这个 JSON：\n{in_path}\n\n{exc}")

    def export_import_template(self):
        out_path = filedialog.asksaveasfilename(
            title="保存 Codex 导入模板",
            defaultextension=".json",
            filetypes=[("JSON", "*.json"), ("All files", "*.*")],
            initialfile="codex_import_template.json",
        )
        if not out_path:
            return
        template = {
            "version": 1,
            "items": [
                {
                    "tree_path": ["操作指南", "AI项目教练", "安装与环境"],
                    "name": "安装指南.md",
                    "type": "文件链接",
                    "path": r"D:\AI Project\AI项目教练\docs\安装指南.md",
                    "url": "",
                    "note": "安装与环境配置说明"
                },
                {
                    "tree_path": ["部署资料", "AI项目教练", "Cloudflare"],
                    "name": "Cloudflare 部署资料文件夹",
                    "type": "文件夹链接",
                    "path": r"D:\AI Project\AI项目教练\deploy\cloudflare",
                    "url": "",
                    "note": "部署配置、截图和记录"
                },
                {
                    "tree_path": ["文献资料", "ABKI-Med", "问诊方法论"],
                    "name": "参考网页",
                    "type": "网址",
                    "path": "",
                    "url": "https://example.com",
                    "note": "网页资料入口"
                }
            ]
        }
        Path(out_path).write_text(json.dumps(template, ensure_ascii=False, indent=2), encoding="utf-8")
        messagebox.showinfo("模板已生成", f"已保存：\n{out_path}")

    def export_markdown(self):
        out_path = filedialog.asksaveasfilename(
            title="导出 Markdown 索引",
            defaultextension=".md",
            filetypes=[("Markdown", "*.md"), ("All files", "*.*")],
            initialfile="FolderTypeIndex_导出索引.md",
        )
        if not out_path:
            return
        lines = ["# FolderTypeIndex 导出索引", ""]
        root = self.get_node(self.data["root_id"])
        for cid in root.get("children", []):
            self.export_node_lines(cid, 0, lines)
        Path(out_path).write_text("\n".join(lines), encoding="utf-8")
        messagebox.showinfo("导出完成", f"已导出：\n{out_path}")

    def markdown_link_for_node(self, node):
        name = node.get("name", "未命名")
        path = node.get("path", "").strip()
        url = node.get("url", "").strip()
        note = node.get("note", "").strip()
        if path:
            uri = Path(path).as_uri() if os.path.isabs(path) else path
            return f"[{name}](<{uri}>)"
        if url:
            return f"[{name}](<{url}>)"
        if note:
            return f"{name} — {note.splitlines()[0]}"
        return name

    def export_node_lines(self, node_id, level, lines):
        node = self.get_node(node_id)
        if not node:
            return
        indent = "  " * level
        icon = TYPE_ICON.get(node.get("type", "分类"), "•")
        lines.append(f"{indent}- {icon} {self.markdown_link_for_node(node)}")
        for cid in node.get("children", []):
            self.export_node_lines(cid, level + 1, lines)


if __name__ == "__main__":
    enable_high_dpi_awareness()
    root = Tk()
    apply_readable_fonts(root)
    app = FolderTypeIndexApp(root)
    root.mainloop()
