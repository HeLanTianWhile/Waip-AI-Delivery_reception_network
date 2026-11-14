# ©2026 何蓝田 保留所有权利
# 意识体 IO 层（Ultimate 核心适配版）。
# 只负责意识体的新建、装载、保存；联想/学习逻辑全部在 Waip_AI_DRN_Ultimate.py 内部完成。

import json
import os
import sys

from Waip_AI_DRN_Ultimate import into_database

# 七库文件名映射（与历史版本保持一致，便于旧意识体直接读取）
DB_FILES = {
    "short-term memory": "短期记忆数据库.txt",
    "long-term memory": "长期记忆数据库.txt",
    "associative network": "联想知识网络.txt",
    "cognitive database": "认知数据库.txt",
    "activated memory": "激活记忆数据库.txt",
    "status database": "状态数据库.txt",
    "other database": "其他数据库.txt",
}

# 核心连接层会读写这个标记库，缺了会 KeyError
MARKER_DB = "激活记忆标记数据库activate_memory_tag_database"


def entity_root(workspace=None):
    if workspace:
        return workspace
    if getattr(sys, "frozen", False):
        return os.path.join(os.path.dirname(os.path.abspath(sys.executable)), "意识体")
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "意识体")


def entity_path(name, workspace=None):
    return os.path.join(entity_root(workspace), name)


def list_entities(workspace=None):
    root = entity_root(workspace)
    if not os.path.isdir(root):
        return []
    return sorted(
        item for item in os.listdir(root)
        if os.path.isdir(os.path.join(root, item))
    )


def ensure_database(data):
    """补齐缺失的库与标记库，保证 Ultimate 运行时不会 KeyError。"""
    for key in DB_FILES:
        data.setdefault(key, {})
    data["other database"].setdefault(MARKER_DB, {})
    return data


def next_key(database):
    numbers = []
    for k in database:
        try:
            numbers.append(int(k))
        except (TypeError, ValueError):
            pass
    return str(max(numbers) + 1) if numbers else "0"


def save_entity(data, path):
    """按七个 txt 文件落盘。"""
    os.makedirs(path, exist_ok=True)
    for key, filename in DB_FILES.items():
        target = os.path.join(path, filename)
        with open(target, "w", encoding="utf-8") as handle:
            json.dump(data.get(key, {}), handle, ensure_ascii=False, indent=1)


def load_entity(path):
    """读取意识体目录，缺文件用空表补齐。"""
    data = into_database()
    for key, filename in DB_FILES.items():
        target = os.path.join(path, filename)
        if not os.path.isfile(target):
            continue
        with open(target, "r", encoding="utf-8-sig") as handle:
            raw = handle.read().strip()
        data[key] = json.loads(raw) if raw else {}
    return ensure_database(data)


def new_entity(name, workspace=None):
    """新建并保存一个空意识体，返回 (data, 目录)。"""
    path = entity_path(name, workspace)
    data = ensure_database(into_database())
    save_entity(data, path)
    return data, path


def ensure_special_tokens(data, start_words=None):
    """Ultimate 不使用 <star>/<end>，此函数保留只为兼容 receiver 调用。"""
    return ensure_database(data)
