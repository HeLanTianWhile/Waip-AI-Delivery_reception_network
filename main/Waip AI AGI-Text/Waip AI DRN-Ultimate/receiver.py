# ©2026 何蓝田 个人保留所有权利
# 接收端（DRN-Ultimate）。
# 与旧版 Receiver 的区别：不再把关联树的每个分支节点打出来。
# 主流程只上报"阶段摘要"，联想树的细节留在模块内部；最终回复由应答层给出候选、
# 输出层拼句，接收端只负责显示与持久化。

import os
import sys

import entity_layer
import main as drn


def base_dir():
    """源码运行时用文件所在目录；打包成 exe 后用执行文件所在目录。"""
    if getattr(sys, "frozen", False):
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


def run_turn(user, data, entity_dir, explain, enable_context_input=True, enable_knowledge_learning=True):
    """消费一次生成器，返回 (回复文本, data, 调试列表, 回复负载)。"""
    generator = drn.main(
        user,
        data,
        entity_dir=entity_dir,
        explain=explain,
        enable_context_input=enable_context_input,
        enable_knowledge_learning=enable_knowledge_learning,
    )
    debug = []
    payload = None
    while True:
        try:
            event = next(generator)
        except StopIteration as stop:
            reply, new_data = stop.value
            return reply, new_data, debug, payload
        if event["type"] == "调试":
            debug.append(event["message"])
        elif event["type"] == "回复":
            payload = event["message"]


def format_debug(messages):
    lines = []
    for item in messages:
        lines.append("  [%s] %s" % (item["阶段"], item["内容"]))
    return "\n".join(lines)


def choose_entity(name, workspace=None, create=False):
    path = entity_layer.entity_path(name, workspace)
    if os.path.isdir(path):
        data = entity_layer.load_entity(path)
        # 旧意识体可能没有 <star>/<end>，装载时补齐起句/收句 token 与连接线
        entity_layer.ensure_special_tokens(data)
        return data, path
    if not create:
        print("意识体不存在：%s" % path)
        print("可用意识体：%s" % ("、".join(entity_layer.list_entities(workspace)) or "无"))
        raise SystemExit(1)
    data, path = entity_layer.new_entity(name, workspace)
    print("已新建意识体：%s（基础字 %d，认知条目 %d）" % (
        path,
        sum(1 for e in data["cognitive database"].values() if "basic" in e["IP"]),
        len(data["cognitive database"]),
    ))
    return data, path


def chat(name="默认意识体", workspace=None, explain=False, create=True,
         enable_context_input=True, enable_knowledge_learning=True):
    data, path = choose_entity(name, workspace, create)
    print("DRN-Ultimate 已加载：%s" % name)
    print("命令：/explain 切换推理明细  /context 切换上下文输入  /learn 切换知识学习  /save 保存  /status 查看规模  /exit 退出")
    print("上下文知识输入：%s    知识学习：%s" % (
        "开" if enable_context_input else "关",
        "开" if enable_knowledge_learning else "关",
    ))
    while True:
        try:
            user = input("你：").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not user:
            continue
        if user == "/exit":
            break
        if user == "/explain":
            explain = not explain
            print("推理明细：%s" % ("开" if explain else "关"))
            continue
        if user == "/context":
            enable_context_input = not enable_context_input
            print("上下文知识输入：%s" % ("开" if enable_context_input else "关"))
            continue
        if user == "/learn":
            enable_knowledge_learning = not enable_knowledge_learning
            print("知识学习：%s" % ("开" if enable_knowledge_learning else "关"))
            continue
        if user == "/save":
            entity_layer.save_entity(data, path)
            print("已保存到 %s" % path)
            continue
        if user == "/status":
            print("短期记忆 %d  认知单元 %d  激活记忆 %d  联想线 %d" % (
                len(data["short-term memory"]),
                len(data["cognitive database"]),
                len(data["activated memory"]),
                len(data["associative network"]),
            ))
            continue

        reply, data, debug, payload = run_turn(
            user, data, path, explain,
            enable_context_input=enable_context_input,
            enable_knowledge_learning=enable_knowledge_learning,
        )
        if explain and debug:
            print(format_debug(debug))
        print("鹅：" + (reply or "……"))

    entity_layer.save_entity(data, path)
    print("意识体已保存。")


def main_entry(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    name = "默认意识体"
    workspace = None
    explain = False
    create = True
    enable_context_input = True
    enable_knowledge_learning = True
    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg == "--entity" and index + 1 < len(argv):
            name = argv[index + 1]
            index += 2
        elif arg == "--workspace" and index + 1 < len(argv):
            workspace = argv[index + 1]
            index += 2
        elif arg == "--explain":
            explain = True
            index += 1
        elif arg == "--no-context":
            enable_context_input = False
            index += 1
        elif arg == "--no-learn":
            enable_knowledge_learning = False
            index += 1
        elif arg == "--no-create":
            create = False
            index += 1
        else:
            name = arg
            index += 1
    chat(name, workspace, explain, create,
         enable_context_input=enable_context_input,
         enable_knowledge_learning=enable_knowledge_learning)


if __name__ == "__main__":
    main_entry()
