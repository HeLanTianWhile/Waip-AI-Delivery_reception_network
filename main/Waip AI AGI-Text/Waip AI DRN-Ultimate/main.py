# ©2026 何蓝田 个人保留所有权利
# DRN-Ultimate 主入口（单文件核心）。
# 本模块只做协议适配：把 Waip_AI_DRN_Ultimate 的生成器包装成 receiver 期望的接口。

import Waip_AI_DRN_Ultimate as core


def main(user, data, entity_dir=None, explain=False, enable_context_input=True, enable_knowledge_learning=True):
    """生成器：yield 调试/回复事件，最后 return (回复字符串, data)。"""
    generator = core.Waip_AI_DRN(
        user,
        data,
        enable_context_input=enable_context_input,
        enable_knowledge_learning=enable_knowledge_learning,
    )
    while True:
        try:
            event = next(generator)
        except StopIteration as stop:
            ai_reply, new_data = stop.value
            # 核心返回每个片段的回复列表，这里拼成一句话
            reply = "".join(str(p) for p in ai_reply)
            return reply, new_data
        if event.get("type") == "调试":
            # 核心的调试消息是字符串，包装成 receiver 的 {"阶段","内容"} 格式
            msg = event["message"]
            if isinstance(msg, dict) and "阶段" in msg and "内容" in msg:
                yield event
            else:
                yield {"type": "调试", "message": {"阶段": "Ultimate", "内容": msg}}
        else:
            yield event
