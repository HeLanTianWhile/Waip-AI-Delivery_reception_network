import copy


def printf(message):
    #msg.append(message)
    yield {"type":"调试","message": message}

def reply_layer(Text, data, associative_tree):
    # 三级优先级：输入匹配(superior是int) > 网络扩展(superior是list) > 背景Root(无superior)
    input_matched = {}
    network_expanded = {}
    background = {}

    for i in associative_tree:
        if "Confirmed unit" not in associative_tree[i]["IP"]:
            continue
        IP = data["activated memory"][associative_tree[i]["correspond to"][-1]]["IP"]
        if (IP[0] == "short-term memory") or (IP[0] == "long-term memory"):
            continue
        this_database_IP = copy.deepcopy(IP)
        del this_database_IP[0]
        for j in data[IP[0]]:
            if data[IP[0]][j]["IP"] == this_database_IP:
                if "combination" not in data[IP[0]][j]["IP"]:
                    continue
                content = ""
                for k in data[IP[0]][j]["content"]:
                    for l in data[IP[0]]:
                        if data[IP[0]][l]["IP"] == k:
                            content += data[IP[0]][l]["content"]
                w = data["activated memory"][associative_tree[i]["correspond to"][-1]]["权重"]
                sup = associative_tree[i].get("superior unit")
                if isinstance(sup, int):
                    target = input_matched
                    tag = "输入匹配"
                elif isinstance(sup, list):
                    target = network_expanded
                    tag = "网络扩展"
                else:
                    target = background
                    tag = "背景"
                if content not in target or w > target[content]:
                    target[content] = w
                yield from printf(f"{tag}词：{content} (权重{w})")

    # 按优先级选取，最多3个
    selected = []
    for pool in [input_matched, network_expanded, background]:
        sorted_pool = sorted(pool.items(), key=lambda x: x[1], reverse=True)
        for w, _ in sorted_pool:
            if w not in selected:
                selected.append(w)
            if len(selected) >= 3:
                break
        if len(selected) >= 3:
            break

    if len(selected) == 0:
        ai_reply = Text + " "
        yield from printf(f"无词语激活，兜底回复：{ai_reply}")
    else:
        ai_reply = "".join(selected) + " "
        yield from printf(f"最终回复：{ai_reply}")

    return ai_reply