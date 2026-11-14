# ©2026 何蓝田 保留所有权利
# 训练终端：手动填入问题与回答，把问答对、分词结果写入认知库与联想网络。

import json
import os
import sys

import entity_layer

ENTITY_NAME = "默认意识体"
WORKSPACE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "意识体")
CORPUS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "语料数据库.json")


def load_corpus():
    """读取语料数据库，返回问答对列表。"""
    if not os.path.isfile(CORPUS_FILE):
        return []
    with open(CORPUS_FILE, "r", encoding="utf-8") as f:
        raw = f.read().strip()
    if not raw:
        return []
    data = json.loads(raw)
    pairs = []
    for item in data:
        q = item.get("question") or item.get("问题")
        a = item.get("answer") or item.get("回答")
        if q and a:
            pairs.append((str(q).strip(), str(a).strip()))
    return pairs


def import_corpus(data):
    """把语料库里所有问答对批量训练进意识体。"""
    pairs = load_corpus()
    if not pairs:
        print("语料库为空。")
        return 0
    print(f"语料库共 {len(pairs)} 条问答对，开始训练...")
    for i, (q, a) in enumerate(pairs, 1):
        train_one(data, q, a)
        if i % 10 == 0 or i == len(pairs):
            print(f"  已训练 {i}/{len(pairs)}")
    print(f"完成。认知库 {len(data['cognitive database'])} 条，联想线 {len(data['associative network'])} 条")
    return len(pairs)


def basic_map(data):
    return {tuple(e["IP"]): e["content"] for e in data["cognitive database"].values() if "basic" in e["IP"]}


def combination_map(data):
    basic = basic_map(data)
    result = {}
    for e in data["cognitive database"].values():
        if "combination" not in e["IP"]:
            continue
        word = "".join(basic.get(tuple(ref), "") for ref in e["content"])
        if word:
            result[word] = tuple(e["IP"])
    return result


def ip_by_content(data):
    ip_by_content = {}
    for word, ip in combination_map(data).items():
        ip_by_content[word] = ip
    for ip, char in basic_map(data).items():
        if char not in ip_by_content:
            ip_by_content[char] = ip
    return ip_by_content


def next_basic_number(data):
    nums = [int(e["IP"][1]) for e in data["cognitive database"].values() if "basic" in e["IP"]]
    return max(nums) + 1 if nums else 0


def next_combination_number(data):
    nums = [int(e["IP"][1]) for e in data["cognitive database"].values() if "combination" in e["IP"]]
    return max(nums) + 1 if nums else 0


def ensure_basic(data, char):
    """确保单字在认知库里，返回其 IP 元组。"""
    for e in data["cognitive database"].values():
        if "basic" in e["IP"] and e["content"] == char:
            return tuple(e["IP"])
    key = entity_layer.next_key(data["cognitive database"])
    ip = ["basic", str(next_basic_number(data))]
    data["cognitive database"][key] = {"content": char, "IP": ip}
    return tuple(ip)


def add_combination(data, word, weight=12000):
    """把一句话作为组合词存入认知库，返回 IP 元组。"""
    combo = combination_map(data)
    if word in combo:
        return combo[word]
    refs = [list(ensure_basic(data, ch)) for ch in word]
    key = entity_layer.next_key(data["cognitive database"])
    ip = ["combination", str(next_combination_number(data))]
    data["cognitive database"][key] = {
        "content": refs,
        "IP": ip,
        "权重": weight,
    }
    return tuple(ip)


def next_line_number(data, line_type):
    return sum(1 for e in data["associative network"].values() if e.get("type") == line_type)


def add_two_way_line(data, left_ip, right_ip, weight=1):
    left, right = list(left_ip), list(right_ip)
    if left == right:
        return
    for e in data["associative network"].values():
        if e.get("type") != "two-way line":
            continue
        heads = e.get("content", [])
        if len(heads) != 2:
            continue
        if (heads[0] == left and heads[1] == right) or (heads[0] == right and heads[1] == left):
            e["权重"] = int(e.get("权重", 1)) + weight
            return
    key = entity_layer.next_key(data["associative network"])
    data["associative network"][key] = {
        "IP": ["associative network", "two-way line", next_line_number(data, "two-way line")],
        "type": "two-way line",
        "content": [left, right],
        "权重": weight,
    }


def tokenize(data, text):
    """贪心最长匹配分词，返回 (IP, token) 列表。"""
    ipbc = ip_by_content(data)
    tokens = []
    pos = 0
    while pos < len(text):
        matched = None
        for size in range(min(4, len(text) - pos), 0, -1):
            piece = text[pos:pos + size]
            if piece in ipbc:
                matched = (ipbc[piece], piece)
                pos += size
                break
        if matched is None:
            tokens.append((None, text[pos]))
            pos += 1
        else:
            tokens.append(matched)
    return tokens


def train_one(data, question, answer):
    """训练一条问答对。"""
    # 1. 问题、回答作为组合词存入认知库
    q_ip = add_combination(data, question)
    a_ip = add_combination(data, answer)

    # 2. 问题 ↔ 回答 双向线
    add_two_way_line(data, q_ip, a_ip, weight=3)

    # 3. 分词：确保每个字都在认知库里
    q_tokens = tokenize(data, question)
    a_tokens = tokenize(data, answer)

    # 把未识别的字（None）补成 basic
    def materialize(tokens):
        result = []
        for ip, tok in tokens:
            if ip is None:
                ip = ensure_basic(data, tok)
            result.append(ip)
        return result

    q_ips = materialize(q_tokens)
    a_ips = materialize(a_tokens)

    # 4. 共现连接：问题内部、回答内部、问题与回答之间都建双向线
    all_ips = []
    for ip in q_ips + a_ips:
        if ip not in all_ips:
            all_ips.append(ip)
    for i in range(len(all_ips)):
        for j in range(i + 1, len(all_ips)):
            add_two_way_line(data, all_ips[i], all_ips[j], weight=1)

    # 5. 组合词也和它的字连一下，方便扩散
    for ip in q_ips:
        add_two_way_line(data, q_ip, ip, weight=1)
    for ip in a_ips:
        add_two_way_line(data, a_ip, ip, weight=1)

    return q_ip, a_ip


def main():
    data = entity_layer.load_entity(entity_layer.entity_path(ENTITY_NAME, WORKSPACE))
    entity_layer.ensure_special_tokens(data)
    print(f"训练终端已加载：{ENTITY_NAME}")
    print(f"认知库 {len(data['cognitive database'])} 条，联想线 {len(data['associative network'])} 条")
    print("命令：/import 批量训练语料库  /save 保存  /status 查看规模  /exit 退出")
    print()

    while True:
        question = input("问题：").strip()
        if not question:
            continue
        if question == "/exit":
            break
        if question == "/save":
            entity_layer.save_entity(data, entity_layer.entity_path(ENTITY_NAME, WORKSPACE))
            print("已保存。")
            continue
        if question == "/status":
            print(f"认知库 {len(data['cognitive database'])} 条，联想线 {len(data['associative network'])} 条")
            continue
        if question == "/import":
            import_corpus(data)
            entity_layer.save_entity(data, entity_layer.entity_path(ENTITY_NAME, WORKSPACE))
            print("语料库训练完成并已保存。")
            continue

        answer = input("回答：").strip()
        if not answer:
            print("回答不能为空，跳过。")
            continue

        q_ip, a_ip = train_one(data, question, answer)
        print(f"  已训练：问题 IP={q_ip}  回答 IP={a_ip}")
        print(f"  当前：认知库 {len(data['cognitive database'])} 条，联想线 {len(data['associative network'])} 条")

    # 退出前自动保存
    entity_layer.save_entity(data, entity_layer.entity_path(ENTITY_NAME, WORKSPACE))
    print("意识体已保存。")


if __name__ == "__main__":
    main()
