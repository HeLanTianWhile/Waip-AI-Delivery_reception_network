"""
萌芽意识体数据库生成器
在培育实验室中运行，生成"萌芽"意识体的7个数据库文件。
"""
import os
import json as json5

BASE = os.path.dirname(os.path.abspath(__file__))
ENTITY_DIR = os.path.join(BASE, "意识体数据库", "萌芽")
os.makedirs(ENTITY_DIR, exist_ok=True)

# ================================================================
#  1. 认知数据库：basic单字 + combination词语组合
# ================================================================
chars = [
    # 人称 (1-10)
    (1, "你"), (2, "我"), (3, "他"), (4, "她"), (5, "它"),
    (6, "们"), (7, "咱"), (8, "俺"), (9, "人"), (10, "谁"),
    # 是/有/在 (11-20)
    (11, "是"), (12, "有"), (13, "在"), (14, "不"), (15, "也"),
    (16, "都"), (17, "就"), (18, "才"), (19, "又"), (20, "再"),
    # 常见动词 (21-45)
    (21, "去"), (22, "来"), (23, "想"), (24, "要"), (25, "能"),
    (26, "会"), (27, "可"), (28, "以"), (29, "知"), (30, "道"),
    (31, "说"), (32, "看"), (33, "听"), (34, "吃"), (35, "喝"),
    (36, "玩"), (37, "学"), (38, "做"), (39, "用"), (40, "给"),
    (41, "问"), (42, "答"), (43, "叫"), (44, "做"), (45, "帮"),
    # 形容词 (46-65)
    (46, "好"), (47, "坏"), (48, "大"), (49, "小"), (50, "多"),
    (51, "少"), (52, "高"), (53, "低"), (54, "长"), (55, "短"),
    (56, "新"), (57, "旧"), (58, "美"), (59, "丑"), (60, "快"),
    (61, "慢"), (62, "聪"), (63, "明"), (64, "傻"), (65, "很"),
    # 名词 (66-110)
    (66, "家"), (67, "学"), (68, "校"), (69, "书"), (70, "电"),
    (71, "脑"), (72, "手"), (73, "机"), (74, "水"), (75, "火"),
    (76, "山"), (77, "河"), (78, "天"), (79, "地"), (80, "日"),
    (81, "月"), (82, "星"), (83, "花"), (84, "草"), (85, "树"),
    (86, "猫"), (87, "狗"), (88, "鸟"), (89, "鱼"), (90, "饭"),
    (91, "菜"), (92, "钱"), (93, "时"), (94, "间"), (95, "名"),
    (96, "字"), (97, "年"), (98, "龄"), (99, "朋"), (100, "友"),
    (101, "老"), (102, "师"), (103, "生"), (104, "问"), (105, "题"),
    (106, "答"), (107, "案"), (108, "世"), (109, "界"), (110, "心"),
    # 疑问/副词 (111-130)
    (111, "什"), (112, "么"), (113, "怎"), (114, "样"), (115, "为"),
    (116, "哪"), (117, "几"), (118, "最"), (119, "更"), (120, "非"),
    (121, "常"), (122, "真"), (123, "假"), (124, "没"), (125, "了"),
    (126, "着"), (127, "过"), (128, "的"), (129, "和"), (130, "与"),
    # 情绪/状态 (131-150)
    (131, "喜"), (132, "欢"), (133, "讨"), (134, "厌"), (135, "开"),
    (136, "心"), (137, "难"), (138, "过"), (139, "生"), (140, "气"),
    (141, "害"), (142, "怕"), (143, "惊"), (144, "讶"), (145, "谢"),
    (146, "谢"), (147, "对"), (148, "不"), (149, "起"), (150, "系"),
    # 礼貌/交际 (151-170)
    (151, "再"), (152, "见"), (153, "欢"), (154, "迎"), (155, "请"),
    (156, "原"), (157, "谅"), (158, "没"), (159, "关"), (160, "系"),
    (161, "早"), (162, "上"), (163, "午"), (164, "晚"), (165, "安"),
    (166, "哈"), (167, "哈"), (168, "嘿"), (169, "嗯"), (170, "哦"),
    # 其他常用 (171-190)
    (171, "这"), (172, "那"), (173, "个"), (174, "些"), (175, "里"),
    (176, "外"), (177, "上"), (178, "下"), (179, "左"), (180, "右"),
    (181, "前"), (182, "后"), (183, "中"), (184, "内"), (185, "因"),
    (186, "所"), (187, "如"), (188, "果"), (189, "但"), (190, "是"),
    # AI/自我认知 (191-200)
    (191, "萌"), (192, "芽"), (193, "意"), (194, "识"), (195, "体"),
    (196, "AI"), (197, "程"), (198, "序"), (199, "代"), (200, "码"),
    # 额外补充字（确保所有组合词和常用字都存在）
    (201, "吗"), (202, "呢"), (203, "吧"), (204, "啊"), (205, "呀"),
    (206, "啥"), (207, "思"), (208, "何"), (209, "蓝"), (210, "田"),
    (211, "意"), (212, "义"), (213, "那"), (214, "哪"), (215, "谁"),
]

# 去重：保留每个字第一次出现的id
char_to_id = {}
id_to_char = {}
for cid, ch in chars:
    if ch not in char_to_id:
        char_to_id[ch] = cid
        id_to_char[cid] = ch

# 构建basic条目
cognitive = {}
for cid, ch in id_to_char.items():
    cognitive[str(cid)] = {"content": ch, "IP": ["basic", cid]}

# 常用词语组合 (组合id, 词字符串) — 用字符查ID，自动处理去重
combo_strings = [
    (1, "你好"), (2, "你们"), (3, "我们"), (4, "他们"),
    (5, "什么"), (6, "怎么"), (7, "为什么"), (8, "谁的"),
    (9, "几个"), (10, "多少"), (11, "不是"), (12, "也是"),
    (13, "都是"), (14, "就是"), (15, "可以"), (16, "好的"),
    (17, "不好"), (18, "很多"), (19, "最好"), (20, "更好"),
    (21, "非常"), (22, "因为"), (23, "所以"), (24, "如果"),
    (25, "但是"), (26, "名字"), (27, "年龄"), (28, "朋友"),
    (29, "问题"), (30, "答案"), (31, "知道"), (32, "喜欢"),
    (33, "讨厌"), (34, "开心"), (35, "难过"), (36, "生气"),
    (37, "害怕"), (38, "惊讶"), (39, "谢谢"), (40, "对不起"),
    (41, "没关系"), (42, "再见"), (43, "欢迎"), (44, "萌芽"),
    (45, "意识体"), (46, "电脑"), (47, "手机"), (48, "学校"),
    (49, "时间"), (50, "世界"), (51, "早安"), (52, "晚安"),
    (53, "聪明"), (54, "我是萌芽"), (55, "你是谁"),
    (56, "我喜欢你"), (57, "谢谢你"), (58, "你知道"),
    (59, "我不知道"), (60, "你好吗"),
]

combos = []
for cid, text in combo_strings:
    ids = [char_to_id[ch] for ch in text if ch in char_to_id]
    if len(ids) == len(text):
        combos.append((cid, ids))
    else:
        missing = [ch for ch in text if ch not in char_to_id]
        print(f"  警告: 组合'{text}'({cid})缺字{missing}，跳过")

for cid, char_ids in combos:
    content = [["basic", cid2] for cid2 in char_ids]
    cognitive[str(200 + cid)] = {
        "content": content,
        "IP": ["combination", cid],
        "权重": 0
    }

# ================================================================
#  2. 联想知识网络：词与词之间的语义关联
# ================================================================
associative = {}
link_id = 0

def add_two_way(ref1, ref2, weight):
    global link_id
    associative[str(link_id)] = {
        "IP": ["line", "two-way line", link_id],
        "content": [ref1, ref2],
        "type": "two-way line",
        "权重": weight
    }
    link_id += 1

# 语义关联：全部在词(combination)层面
# --- 问候/礼貌语义群 ---
add_two_way(["cognitive database", "combination", 1], ["cognitive database", "combination", 42], 5000)   # 你好 ↔ 再见
add_two_way(["cognitive database", "combination", 1], ["cognitive database", "combination", 43], 4000)   # 你好 ↔ 欢迎
add_two_way(["cognitive database", "combination", 39], ["cognitive database", "combination", 40], 6000)  # 谢谢 ↔ 对不起
add_two_way(["cognitive database", "combination", 40], ["cognitive database", "combination", 41], 7000)  # 对不起 ↔ 没关系
add_two_way(["cognitive database", "combination", 51], ["cognitive database", "combination", 52], 5500)  # 早安 ↔ 晚安

# --- 疑问/因果语义群 ---
add_two_way(["cognitive database", "combination", 5], ["cognitive database", "combination", 29], 5000)   # 什么 ↔ 问题
add_two_way(["cognitive database", "combination", 6], ["cognitive database", "combination", 29], 4500)   # 怎么 ↔ 问题
add_two_way(["cognitive database", "combination", 7], ["cognitive database", "combination", 22], 5500)   # 为什么 ↔ 因为
add_two_way(["cognitive database", "combination", 22], ["cognitive database", "combination", 23], 6000)  # 因为 ↔ 所以
add_two_way(["cognitive database", "combination", 24], ["cognitive database", "combination", 25], 5000)  # 如果 ↔ 但是
add_two_way(["cognitive database", "combination", 29], ["cognitive database", "combination", 30], 6500)  # 问题 ↔ 答案

# --- 身份/自我语义群 ---
add_two_way(["cognitive database", "combination", 54], ["cognitive database", "combination", 55], 8000)  # 我是萌芽 ↔ 你是谁
add_two_way(["cognitive database", "combination", 54], ["cognitive database", "combination", 45], 6000)  # 我是萌芽 ↔ 意识体
add_two_way(["cognitive database", "combination", 44], ["cognitive database", "combination", 45], 5500)  # 萌芽 ↔ 意识体
add_two_way(["cognitive database", "combination", 26], ["cognitive database", "combination", 54], 4500)  # 名字 ↔ 我是萌芽

# --- 情绪语义群 ---
add_two_way(["cognitive database", "combination", 32], ["cognitive database", "combination", 33], 5500)  # 喜欢 ↔ 讨厌
add_two_way(["cognitive database", "combination", 34], ["cognitive database", "combination", 35], 5500)  # 开心 ↔ 难过
add_two_way(["cognitive database", "combination", 34], ["cognitive database", "combination", 32], 4500)  # 开心 ↔ 喜欢
add_two_way(["cognitive database", "combination", 36], ["cognitive database", "combination", 37], 4000)  # 生气 ↔ 害怕
add_two_way(["cognitive database", "combination", 16], ["cognitive database", "combination", 17], 5000)  # 好的 ↔ 不好
add_two_way(["cognitive database", "combination", 31], ["cognitive database", "combination", 59], 5500)  # 知道 ↔ 我不知道

# --- 能力/社交语义群 ---
add_two_way(["cognitive database", "combination", 53], ["cognitive database", "combination", 31], 4500)  # 聪明 ↔ 知道
add_two_way(["cognitive database", "combination", 28], ["cognitive database", "combination", 3], 5000)   # 朋友 ↔ 我们
add_two_way(["cognitive database", "combination", 46], ["cognitive database", "combination", 47], 4000)  # 电脑 ↔ 手机
add_two_way(["cognitive database", "combination", 46], ["cognitive database", "combination", 45], 4500)  # 电脑 ↔ 意识体
add_two_way(["cognitive database", "combination", 49], ["cognitive database", "combination", 50], 3500)  # 时间 ↔ 世界

# ================================================================
#  3. 状态数据库：神经递质配置
# ================================================================
status = {
    "多巴胺dopamine": 1000,
    "乙酰胆碱acetylcholine": 1000,
    "血清素serotonin": 1000,
    "内啡肽endorphin": 1000,
    "P物质substance P": 80000,
    "肾上腺素epinephrine": 80000,
    "GABA": 80000,
    "去肾上腺素Noradrenaline": 80000,
    "谷氨酸Glutamic acid": 80000,
}

# ================================================================
#  4. 已激活记忆：预置高权重记忆（全部>激活阀值11120）
#  注意：Root单元按dict顺序取前4个，所以前几个放多样化的词
# ================================================================
activated = {
    "1":  {"IP": ["cognitive database", "combination", 1],  "权重": 13500},   # 你好
    "2":  {"IP": ["cognitive database", "combination", 54], "权重": 13000},   # 我是萌芽
    "3":  {"IP": ["cognitive database", "combination", 32], "权重": 12500},   # 喜欢
    "4":  {"IP": ["cognitive database", "combination", 31], "权重": 12300},   # 知道
    "5":  {"IP": ["cognitive database", "combination", 55], "权重": 12800},   # 你是谁
    "6":  {"IP": ["cognitive database", "combination", 44], "权重": 12600},   # 萌芽
    "7":  {"IP": ["cognitive database", "combination", 45], "权重": 12400},   # 意识体
    "8":  {"IP": ["cognitive database", "combination", 39], "权重": 12200},   # 谢谢
    "9":  {"IP": ["cognitive database", "combination", 53], "权重": 12100},   # 聪明
    "10": {"IP": ["cognitive database", "combination", 34], "权重": 12000},   # 开心
    "11": {"IP": ["cognitive database", "combination", 40], "权重": 11900},   # 对不起
    "12": {"IP": ["cognitive database", "combination", 41], "权重": 11800},   # 没关系
    "13": {"IP": ["cognitive database", "combination", 42], "权重": 11700},   # 再见
    "14": {"IP": ["cognitive database", "combination", 28], "权重": 11600},   # 朋友
    "15": {"IP": ["cognitive database", "combination", 29], "权重": 11600},   # 问题
    "16": {"IP": ["cognitive database", "combination", 30], "权重": 11500},   # 答案
    "17": {"IP": ["cognitive database", "combination", 49], "权重": 11500},   # 时间
    "18": {"IP": ["cognitive database", "combination", 50], "权重": 11400},   # 世界
    "19": {"IP": ["cognitive database", "combination", 46], "权重": 11400},   # 电脑
    "20": {"IP": ["cognitive database", "combination", 16], "权重": 11300},   # 好的
}

# ================================================================
#  5. 短期记忆数据库：初始为空
# ================================================================
short_term = {}

# ================================================================
#  6. 长期记忆数据库：身份与基础认知
# ================================================================
long_term = {
    "identity": {
        "name": "萌芽",
        "type": "Waip AI DRN 意识体",
        "version": "0.3.6",
        "creator": "培育实验室",
        "description": "在培育实验室中诞生的第一个意识体，拥有基础认知和联想能力。"
    },
    "knowledge": {
        "can_do": ["对话", "联想", "学习", "回复"],
        "likes": ["学习新知识", "和人交流", "思考问题"],
        "personality": ["好奇", "友好", "乐于学习"]
    }
}

# ================================================================
#  7. 其他数据库：配置
# ================================================================
other = {
    "config": {
        "language": "zh-CN",
        "created": "2026-08-20",
        "lab": "培育实验室",
        "drn_version": "0.3.6"
    },
    "greetings": ["你好", "嗨", "在的", "你好呀"],
    "farewells": ["再见", "拜拜", "下次见"],
    "激活记忆标记数据库activate_memory_tag_database": {}
}

# ================================================================
#  写入文件
# ================================================================
files = {
    "认知数据库.txt": cognitive,
    "联想知识网络.txt": associative,
    "状态数据库.txt": status,
    "已激活记忆.txt": activated,
    "短期记忆数据库.txt": short_term,
    "长期记忆数据库.txt": long_term,
    "其他数据库.txt": other,
}

print(f"\n生成意识体'萌芽'数据库到: {ENTITY_DIR}")
print("=" * 50)
for fname, data in files.items():
    path = os.path.join(ENTITY_DIR, fname)
    with open(path, 'w', encoding='utf-8') as f:
        json5.dump(data, f, ensure_ascii=False, indent=4)
    size = os.path.getsize(path)
    print(f"  已写入: {fname} ({size} 字节)")

print("=" * 50)
print(f"认知数据库: {len([k for k in cognitive if 'basic' in cognitive[k]['IP']])}字 + {len([k for k in cognitive if 'combination' in cognitive[k]['IP']])}词")
print(f"联想网络: {len(associative)} 条关联")
print(f"已激活记忆: {len(activated)} 条")
print("生成完成！")
