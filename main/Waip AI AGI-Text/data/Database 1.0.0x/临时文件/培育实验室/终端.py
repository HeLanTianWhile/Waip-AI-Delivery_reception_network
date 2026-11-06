# -*- coding: utf-8 -*-
"""
培育实验室终端 —— Waip AI DRN 0.3.6 意识体入口
参考 Database 11.0/Waip AI DRN Receiver.p.py 简化版
固定加载 0.3.6 模块 + "萌芽"意识体
"""
import os
import sys
import json
import copy
import traceback
from importlib.machinery import SourceFileLoader

BASE = os.path.dirname(os.path.abspath(__file__))
ENTITY_NAME = "萌芽"
TF_DEBUG = False  # 是否显示调试信息
ORIGINAL_ACTIVATED = None  # 原始激活记忆备份

# 颜色输出
def printf(msg):
    print("\033[92m" + str(msg) + "\033[0m")

def printf_debug(msg):
    if TF_DEBUG:
        print("\033[36m" + str(msg) + "\033[0m")

def inputf(msg):
    return input("\033[92m" + msg + "\033[0m")

def load_data():
    """加载意识体的7个数据库"""
    entity_dir = os.path.join(BASE, "意识体数据库", ENTITY_NAME)
    data = {
        "short-term memory": {},
        "long-term memory": {},
        "associative network": {},
        "cognitive database": {},
        "activated memory": {},
        "status database": {},
        "other database": {},
    }
    files = {
        "short-term memory": "短期记忆数据库.txt",
        "long-term memory": "长期记忆数据库.txt",
        "associative network": "联想知识网络.txt",
        "cognitive database": "认知数据库.txt",
        "activated memory": "已激活记忆.txt",
        "status database": "状态数据库.txt",
        "other database": "其他数据库.txt",
    }
    for key, fname in files.items():
        fpath = os.path.join(entity_dir, fname)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                data[key] = json.load(f)
            printf_debug(f"已加载: {fname}")
        else:
            printf(f"警告: {fname} 不存在，使用空字典")
    return data

def prune_activated_memory(data, max_entries=15):
    """每轮对话后恢复激活记忆：认知类重置为原始条目，短期记忆保留最近10条"""
    global ORIGINAL_ACTIVATED
    am = data["activated memory"]
    # 分离短期记忆
    stm = {k: v for k, v in am.items() if v["IP"][0] == "short-term memory"}
    # 用原始认知条目重建
    new_am = {}
    if ORIGINAL_ACTIVATED:
        for k, v in ORIGINAL_ACTIVATED.items():
            new_am[k] = copy.deepcopy(v)
    # 保留最近10条短期记忆
    stm_sorted = sorted(stm.keys(), key=lambda k: int(k), reverse=True)[:10]
    for k in stm_sorted:
        new_am[k] = stm[k]
    data["activated memory"] = new_am
    return len(new_am)

def save_data(data):
    """保存意识体的7个数据库"""
    entity_dir = os.path.join(BASE, "意识体数据库", ENTITY_NAME)
    os.makedirs(entity_dir, exist_ok=True)
    files = {
        "short-term memory": "短期记忆数据库.txt",
        "long-term memory": "长期记忆数据库.txt",
        "associative network": "联想知识网络.txt",
        "cognitive database": "认知数据库.txt",
        "activated memory": "已激活记忆.txt",
        "status database": "状态数据库.txt",
        "other database": "其他数据库.txt",
    }
    for key, fname in files.items():
        fpath = os.path.join(entity_dir, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data[key], f, ensure_ascii=False, indent=4)

def load_drn():
    """加载 Waip AI DRN 0.3.6 模块"""
    module_path = os.path.join(BASE, "Waip AI DRN 0.3.6", "main.py")
    module_dir = os.path.dirname(module_path)
    if module_dir not in sys.path:
        sys.path.insert(0, module_dir)
    module = SourceFileLoader("Waip_AI_DRN_036", module_path).load_module()
    return module

def into():
    """初始化"""
    printf("=" * 50)
    printf("  培育实验室终端 · Waip AI DRN 0.3.6")
    printf("=" * 50)
    printf(f"意识体: {ENTITY_NAME}")
    printf("输入 && help 查看命令，&& exit 退出")
    printf("=" * 50)

    # 加载DRN模块
    global Waip_AI_DRN
    Waip_AI_DRN = load_drn()
    printf("DRN 0.3.6 模块已加载")

    # 加载数据
    global data, ORIGINAL_ACTIVATED
    data = load_data()
    # 备份原始激活记忆（每轮对话后恢复，防止Connection_layer洪水）
    ORIGINAL_ACTIVATED = copy.deepcopy(data["activated memory"])
    cog_count = len(data["cognitive database"])
    assoc_count = len(data["associative network"])
    printf(f"认知数据库: {cog_count} 条 | 联想网络: {assoc_count} 条")
    printf("意识体已就绪\n")

def handle_command(cmd):
    """处理 && 开头的命令"""
    global TF_DEBUG
    if cmd == "&& help":
        printf("命令列表:")
        printf("  && help   - 显示帮助")
        printf("  && debug  - 切换调试信息")
        printf("  && save   - 手动保存数据库")
        printf("  && clean  - 清理激活记忆（去重限量）")
        printf("  && reset  - 重置意识体为初始状态")
        printf("  && status - 查看意识体状态")
        printf("  && exit   - 退出")
    elif cmd == "&& debug":
        TF_DEBUG = not TF_DEBUG
        printf(f"调试信息: {'开' if TF_DEBUG else '关'}")
    elif cmd == "&& save":
        save_data(data)
        printf("数据库已保存")
    elif cmd == "&& status":
        printf(f"意识体: {ENTITY_NAME}")
        printf(f"认知条目: {len(data['cognitive database'])}")
        printf(f"联想条目: {len(data['associative network'])}")
        printf(f"激活记忆: {len(data['activated memory'])}")
        printf(f"短期记忆: {len(data['short-term memory'])}")
        status = data["status database"]
        printf(f"多巴胺: {status.get('多巴胺dopamine', '?')}")
        printf(f"血清素: {status.get('血清素serotonin', '?')}")
    elif cmd == "&& clean":
        n = prune_activated_memory(data)
        save_data(data)
        printf(f"激活记忆已清理，剩余{n}条")
    elif cmd == "&& reset":
        # 重新运行gen_entity.py生成干净的数据库
        gen_script = os.path.join(BASE, "gen_entity.py")
        if os.path.exists(gen_script):
            import subprocess
            r = subprocess.run([sys.executable, gen_script], capture_output=True, text=True, encoding='utf-8')
            printf(r.stdout)
            if r.returncode != 0:
                printf(f"生成失败: {r.stderr}")
            else:
                data = load_data()
                ORIGINAL_ACTIVATED = copy.deepcopy(data["activated memory"])
                printf("意识体已重置为初始状态")
        else:
            printf("找不到gen_entity.py")
    elif cmd == "&& exit":
        printf("再见！")
        sys.exit(0)
    else:
        printf(f"未知命令: {cmd}，输入 && help 查看帮助")

def main():
    global data, ORIGINAL_ACTIVATED
    user = inputf("你：")

    if user.startswith("&&"):
        handle_command(user.strip())
        return

    printf("")
    # 调用DRN生成器
    gen = Waip_AI_DRN.main(user, data)
    try:
        while True:
            message = next(gen)
            if message["type"] == "调试":
                printf_debug("【调试】" + str(message["message"]))
            elif message["type"] == "回复":
                printf("【思考】" + str(message["message"]))
    except StopIteration as e:
        ai_reply, data = e.value

    # ai_reply 是列表，拼接成字符串
    if isinstance(ai_reply, list):
        reply_text = "".join(str(x) for x in ai_reply)
    else:
        reply_text = str(ai_reply)

    printf("")
    printf(f"{ENTITY_NAME}：{reply_text}")
    # 每轮对话后重载干净数据，禁用自动学习（防止Connection_layer洪水导致回复退化）
    # 如需培育意识体，可手动编辑数据库文件后用 && reset 重新加载
    data = load_data()
    ORIGINAL_ACTIVATED = copy.deepcopy(data["activated memory"])
    printf_debug("数据已重置为初始状态")

if __name__ == "__main__":
    try:
        into()
        while True:
            main()
    except Exception as e:
        printf(f"\n错误：{e}")
        printf(f"错误类型：{type(e).__name__}")
        printf(f"错误详情：\n{traceback.format_exc()}")
        try:
            save_data(data)
            printf("数据已尝试保存")
        except:
            pass
