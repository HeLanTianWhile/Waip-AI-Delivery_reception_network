import psutil
import copy
import time
from datetime import datetime

# ©2026 何蓝田 保留所有权利

# import random # 你为什么导入了random模块



def into_database():
    data = {
        "short-term memory": {},
        "long-term memory": {},
        "associative network": {},
        "cognitive database": {},
        "activated memory": {},
        "status database": {"多巴胺dopamine": 35000,"乙酰胆碱acetylcholine": 25000,"血清素serotonin": 50000,"内啡肽endorphin": 40000,"P物质substance P": 15000,"肾上腺素epinephrine": 20000,"GABA": 30000,"去肾上腺素Noradrenaline": 22000,"谷氨酸Glutamic acid": 25000},
        "other database": {},
    }
    return data

def Waip_AI_DRN(user, data, enable_context_input=True, enable_knowledge_learning=True):
    """核心生成器。

    开关参数（用于调节输出稳定性）：
      enable_context_input   —— 是否开启上下文知识输入。关闭后，本轮的输入与回复不再写入
                                短期记忆数据库；激活记忆数据库也不写入新条目、不调整权重、
                                不擦除旧记忆，即不从当前上下文里学习。
      enable_knowledge_learning —— 是否开启知识学习。关闭后不再修改认知数据库与联想知识网络
                                （不新增单元、不调整权重、不建立联想线），应答与激活照常运行。
    """

    msg = []

    def printf(message):
        #msg.append(message)
        yield {"type":"调试","message": message}

    def printf_reply(message):
        yield {"type":"回复","message": message}

    yield from printf(f"上下文知识输入：{'开' if enable_context_input else '关'}")
    yield from printf(f"知识学习：{'开' if enable_knowledge_learning else '关'}")

    # 定义文字注意力算法
    def Text_Attention_Algorithm(text, data):
        dopamine = data["status database"]["多巴胺dopamine"]
        acetylcholine = data["status database"]["乙酰胆碱acetylcholine"]
        serotonin = data["status database"]["血清素serotonin"]
        endorphin = data["status database"]["内啡肽endorphin"]
        substance_P = data["status database"]["P物质substance P"]
        epinephrine = data["status database"]["肾上腺素epinephrine"]
        Noradrenaline = data["status database"]["去肾上腺素Noradrenaline"]
        GABA = data["status database"]["GABA"]
        Glamic_acid = data["status database"]["谷氨酸Glutamic acid"]
        ##########
        dopamine_processing = float(100000 - dopamine) / 10000
        acetylcholine_processing = float(100000 - acetylcholine) / 10000
        serotonin_processing = float(100000 - serotonin) / 10000
        endorphin_processing = float(100000 - endorphin) / 10000
        substance_P_processing = float(substance_P) / 10000
        epinephrine_processing = float(epinephrine) / 10000# 比较复杂先不管
        Noradrenaline_processing = float(Noradrenaline) / 10000# 比较复杂先不管
        GABA_processing = float(GABA) / 10000# 比较复杂先不管
        Glamic_acid_processing = float(Glamic_acid) / 10000# 比较复杂先不管
        ##########
        text_range = round((dopamine_processing + acetylcholine_processing + serotonin_processing + endorphin_processing + substance_P_processing + epinephrine_processing + Noradrenaline_processing + GABA_processing + Glamic_acid_processing) / 10)
        yield from printf(f"文字注意力范围：{text_range}")
        return text_range
    
    # 定义输入层
    def input_layer(user, data, index):
        text_range = yield from Text_Attention_Algorithm(user, data)
        Text = user[index:index+text_range]
        yield from printf(f"文字注意力内容：{Text}")
        yield from printf(f"当前截止：{index+text_range}")
        return Text, text_range

    def call(Text, data, data_processed):
        associative_tree = yield from association_layer(Text, data, data_processed)
        yield from printf(f"关联树：{associative_tree}")
        reply = yield from reply_layer(Text, data, associative_tree)
        yield from printf(reply)

        output_layer(reply)
        yield from Connection_layer(Text, data, associative_tree, reply)
        return reply

    def association_layer(Text, data, data_processed):

        def Calculation_formula_number_branches_associative_tree(text, data):
            dopamine_processing = float(data["status database"]["多巴胺dopamine"]) / 1000
            acetylcholine_processing = float(data["status database"]["乙酰胆碱acetylcholine"]) / 1000
            serotonin_processing = float(data["status database"]["血清素serotonin"]) / 1000
            endorphin_processing = float(data["status database"]["内啡肽endorphin"]) / 1000
            substance_P_processing = float(100000 - data["status database"]["P物质substance P"]) / 1000
            epinephrine_processing = float(100000 - data["status database"]["肾上腺素epinephrine"]) / 1000
            Noradrenaline_processing = float(100000 - data["status database"]["去肾上腺素Noradrenaline"]) / 1000
            GABA_processing = float(100000 - data["status database"]["GABA"]) / 1000
            Glamic_acid_processing = float(100000 - data["status database"]["谷氨酸Glutamic acid"]) / 1000
            ##########
            number_branches_associative_tree = round((dopamine_processing + acetylcholine_processing + serotonin_processing + endorphin_processing + substance_P_processing + epinephrine_processing + Noradrenaline_processing + GABA_processing + Glamic_acid_processing) / 9)
            yield from printf(f"关联树分支数：{number_branches_associative_tree}")
            return number_branches_associative_tree 
            

        associative_tree = {}
        activated_Delivery_reception_unit = []

        for i in data_processed["activated memory"]:
            if "associative network" not in data["activated memory"][i]["IP"]:
                activated_Delivery_reception_unit.append(i)
        
        yield from printf(f"激活递接元：{activated_Delivery_reception_unit}")
        
        number_branches_associative_tree = yield from Calculation_formula_number_branches_associative_tree(Text, data)
        index = {"main_index": 0,"Undetermined_Root_unit_index": 0, "Confirmed_Root_unit_index": 0, "Confirmed_Subunit_index": 0}

        # 性能索引：IP -> 条目键列表（等价替换逐字符全库扫描，解析结果按 IP 缓存）
        association_db_index = {}

        def _association_db_index(db_name):
            if db_name not in association_db_index:
                raw = {}
                for k in data[db_name]:
                    raw.setdefault(tuple(data[db_name][k]["IP"]), []).append(k)
                association_db_index[db_name] = {"raw": raw, "resolved": {}}
            return association_db_index[db_name]

        def _association_entry_contents(db_name, this_IP):
            idx = _association_db_index(db_name)
            ip_key = tuple(this_IP)
            if ip_key not in idx["resolved"]:
                contents = []
                for k in idx["raw"].get(ip_key, []):
                    k_content = data[db_name][k]["content"]
                    if not isinstance(k_content, str):
                        resolved_k_content = ""
                        for ref in k_content:
                            for l in idx["raw"].get(tuple(ref), []):
                                resolved_k_content += data[db_name][l]["content"]
                        k_content = resolved_k_content
                    contents.append(k_content)
                idx["resolved"][ip_key] = contents
            return idx["resolved"][ip_key]

        for i in list(Text):
            if index["main_index"] == number_branches_associative_tree:
                break
            associative_tree[str(index["main_index"])] = {"IP": ["Undetermined unit", "Root unit", index["Undetermined_Root_unit_index"]], "content": i}
            index["main_index"] += 1
            index["Undetermined_Root_unit_index"] += 1
            for j in activated_Delivery_reception_unit:
                IP = data["activated memory"][j]["IP"]
                IP_database = IP[0]
                this_IP = copy.deepcopy(IP)
                del this_IP[0]
                for k_content in _association_entry_contents(IP_database, this_IP):
                    if (i == k_content) or (i in k_content):
                        associative_tree[str(index["main_index"])] = {"IP": ["Confirmed unit", "Subunit", index["Confirmed_Subunit_index"]], "correspond to": ["activated memory", j], "superior unit": index["main_index"] - 1}
                        index["main_index"] += 1
                        index["Confirmed_Subunit_index"] += 1
        for i in activated_Delivery_reception_unit:
            if index["main_index"] == number_branches_associative_tree:
                break
            associative_tree[str(index["main_index"])] = {"IP": ["Confirmed unit", "Root unit", index["Confirmed_Root_unit_index"]], "correspond to": ["activated memory", i]}
            index["main_index"] += 1
            index["Confirmed_Root_unit_index"] += 1

        stop_index = 0
        copy_associative_tree = copy.deepcopy(associative_tree)
        added_edges = set()
        while True:
            stop_index += 1
            copy_associative_tree = copy.deepcopy(associative_tree)

            # 本轮 while 迭代内 associative_tree 不变，树中确认单元的 IP 映射只算一次
            # （等价替换原来每条联想线都重建一次的 copy_associative_tree_list）
            tree_ip_to_nodes = {}
            for p in associative_tree:
                if "Undetermined unit" in associative_tree[p]["IP"]:
                    continue
                node_ip = tuple(data[associative_tree[p]["correspond to"][0]][associative_tree[p]["correspond to"][-1]]["IP"])
                tree_ip_to_nodes.setdefault(node_ip, []).append(p)

            # 性能：联想库在本层执行期间不变, 网络条目结构先预解析一次
            # （等价替换 while 每轮都重建的 associative_unit 字典，条目顺序与判定完全一致）
            if stop_index == 1:
                network_edges = []
                edge_pos_by_ip = {}
                for i in data["associative network"]:
                    edge_entry = data["associative network"][i]
                    if edge_entry["type"] == "two-way line":
                        edge_type = "two-way head"
                    elif edge_entry["type"] == "one-way line":
                        edge_type = "one-way head"
                    else:
                        continue
                    member_ipts = [tuple(c) for c in edge_entry["content"]]
                    pos = len(network_edges)
                    network_edges.append((i, edge_type, member_ipts))
                    for ip in member_ipts:
                        edge_pos_by_ip.setdefault(ip, []).append(pos)

            # 只处理"至少有一条线头落在联想树上"的边（其余边在循环里必定 continue），
            # 并按联想库原有顺序处理，break 时机与结果完全一致
            candidate_positions = set()
            for ip in tree_ip_to_nodes:
                positions = edge_pos_by_ip.get(ip)
                if positions:
                    candidate_positions.update(positions)

            for pos in sorted(candidate_positions):
                i, edge_type, member_ipts = network_edges[pos]
                matching_number = 0

                for ip in member_ipts:
                    if ip in tree_ip_to_nodes:
                        matching_number += 1

                if matching_number == 0 or matching_number == len(member_ipts):
                    continue

                for ip in member_ipts:
                    for p in tree_ip_to_nodes.get(ip, []):
                        if edge_type == "two-way head":
                            if i not in added_edges:
                                copy_associative_tree[str(index["main_index"])] = {"IP": ["Confirmed unit", "Subunit", index["Confirmed_Subunit_index"]], "correspond to": associative_tree[p]["correspond to"], "superior unit": [p]}
                                index["main_index"] += 1
                                index["Confirmed_Subunit_index"] += 1
                                added_edges.add(i)
                                yield from printf(f"添加成功:{copy_associative_tree[str(index['main_index'] - 1)]}")
                        elif edge_type == "one-way head":
                            if i not in added_edges:
                                copy_associative_tree[str(index["main_index"])] = {"IP": ["Confirmed unit", "Subunit", index["Confirmed_Subunit_index"]], "correspond to": associative_tree[p]["correspond to"], "superior unit": [p]}
                                index["main_index"] += 1
                                index["Confirmed_Subunit_index"] += 1
                                added_edges.add(i)
                                yield from printf("添加成功")

                if index["main_index"] == number_branches_associative_tree:
                        break
            if index["main_index"] == number_branches_associative_tree:
                break

            associative_tree = copy.deepcopy(copy_associative_tree)

            if stop_index == number_branches_associative_tree:
                yield from printf(f"此临时循环已执行{stop_index}次，未完成关联树的构建所以将会无限循环，此临时变量将会制止程序")
                break


        return associative_tree

    def reply_layer(Text, data, associative_tree):
        ai_reply = ""

        # 性能索引：IP -> 条目键列表（等价替换逐节点全库扫描）
        reply_db_index = {}

        def _reply_db_index(db_name):
            if db_name not in reply_db_index:
                raw = {}
                for j in data[db_name]:
                    raw.setdefault(tuple(data[db_name][j]["IP"]), []).append(j)
                reply_db_index[db_name] = raw
            return reply_db_index[db_name]

        for i in associative_tree:
            if "Confirmed unit" in associative_tree[i]["IP"]:
                IP = data["activated memory"][associative_tree[i]["correspond to"][-1]]["IP"]
                if (IP[0] == "short-term memory") or (IP[0] == "long-term memory"):
                    continue
                this_database_IP = copy.deepcopy(IP)
                del this_database_IP[0]
                for j in _reply_db_index(IP[0]).get(tuple(this_database_IP), []):
                    if "combination" in data[IP[0]][j]["IP"]:
                        content = ""
                        for k in data[IP[0]][j]["content"]:
                            for l in _reply_db_index(IP[0]).get(tuple(k), []):
                                yield from printf(data[IP[0]][l]["IP"])
                                yield from printf(k)
                                content += data[IP[0]][l]["content"]
                        ai_reply += content
                    else:
                        ai_reply += data[IP[0]][j]["content"]
            elif "Undetermined unit" in associative_tree[i]["IP"]:
                ai_reply += associative_tree[i]["content"]
            ai_reply += " "

        if ai_reply == "":
            ai_reply = "系统错误，无法理解问题。"

        return ai_reply

    def calculate_activation_valve(data):
        dopamine_processing = float((100000 - data["多巴胺dopamine"]) / 5)
        acetylcholine_processing = float((100000 - data["乙酰胆碱acetylcholine"]) / 5)
        serotonin_processing = float((100000 - data["血清素serotonin"]) / 5)
        endorphin_processing = float((100000 - data["内啡肽endorphin"]) / 5)
        substance_P_processing = float((data["P物质substance P"]) / 5)
        epinephrine_processing = float((100000 - data["肾上腺素epinephrine"]) / 5)
        Noradrenaline_processing = float((100000 - data["去肾上腺素Noradrenaline"]) / 5)
        GABA_processing = float((100000 - data["GABA"]) / 5)
        Glamic_acid_processing = float((100000 - data["谷氨酸Glutamic acid"]) / 5)

        activate_valve = round((dopamine_processing + acetylcholine_processing + serotonin_processing + endorphin_processing + substance_P_processing + epinephrine_processing + Noradrenaline_processing + GABA_processing + Glamic_acid_processing) / 10)
        yield from printf(f"激活阀值：{activate_valve}")
        return activate_valve

    def output_layer(reply):
        pass

    def Connection_layer(Text, data, associative_tree, reply):

        def Weight_neurotransmitter_calculation_formula_when_storing_IP_input_from_short_term_memory_users_into_activation_memory(data, Activation_threshold):
            # 除以100
            dopamine_processing = float((data["多巴胺dopamine"]) / 100)
            acetylcholine_processing = float((data["乙酰胆碱acetylcholine"]) / 100)
            serotonin_processing = float((data["血清素serotonin"]) / 100)
            endorphin_processing = float((data["内啡肽endorphin"]) / 100)
            substance_P_processing = float((100000 - data["P物质substance P"]) / 100)
            epinephrine_processing = float((data["肾上腺素epinephrine"]) / 100)
            Noradrenaline_processing = float((data["去肾上腺素Noradrenaline"]) / 100)
            GABA_processing = float((data["GABA"]) / 100)
            Glamic_acid_processing = float((data["谷氨酸Glutamic acid"]) / 100)

            # 计算激活阀值
            Weight_neurotransmitter_calculation_formula_when_storing_IP_input_from_short_term_memory_users_into_activation_memory_c = round((dopamine_processing + acetylcholine_processing + serotonin_processing + endorphin_processing + substance_P_processing + epinephrine_processing + Noradrenaline_processing + GABA_processing + Glamic_acid_processing) / 10 + Activation_threshold)
            yield from printf(f"用户输入计入激活记忆数据库时的初始权重：{Weight_neurotransmitter_calculation_formula_when_storing_IP_input_from_short_term_memory_users_into_activation_memory_c}")
            return Weight_neurotransmitter_calculation_formula_when_storing_IP_input_from_short_term_memory_users_into_activation_memory_c
        
        def Weight_neurotransmitter_calculation_formula_when_storing_IP_input_from_short_term_memory_ai_into_activation_memory(data, Activation_threshold):
            # 除以100
            dopamine_processing = float((data["多巴胺dopamine"]) / 100)
            acetylcholine_processing = float((data["乙酰胆碱acetylcholine"]) / 100)
            serotonin_processing = float((data["血清素serotonin"]) / 100)
            endorphin_processing = float((data["内啡肽endorphin"]) / 100)
            substance_P_processing = float((100000 - data["P物质substance P"]) / 100)
            epinephrine_processing = float((data["肾上腺素epinephrine"]) / 100)
            Noradrenaline_processing = float((data["去肾上腺素Noradrenaline"]) / 100)
            GABA_processing = float((data["GABA"]) / 100)
            Glamic_acid_processing = float((data["谷氨酸Glutamic acid"]) / 100)

            # 计算激活阀值
            Weight_neurotransmitter_calculation_formula_when_storing_IP_input_from_short_term_memory_ai_into_activation_memory_c = round((dopamine_processing + acetylcholine_processing + serotonin_processing + endorphin_processing + substance_P_processing + epinephrine_processing + Noradrenaline_processing + GABA_processing + Glamic_acid_processing) / 9 + Activation_threshold)
            yield from printf(f"AI输入计入激活记忆数据库时的初始权重：{Weight_neurotransmitter_calculation_formula_when_storing_IP_input_from_short_term_memory_ai_into_activation_memory_c}")
            return Weight_neurotransmitter_calculation_formula_when_storing_IP_input_from_short_term_memory_ai_into_activation_memory_c

        def update_neurotransmitters(data,Text,reply,associative_tree):
            battery_level = 100
            battery_info = psutil.sensors_battery()
            if battery_info is not None:
                battery_level = battery_info.percent
            
            data["status database"]["乙酰胆碱acetylcholine"] = round(battery_level *1000 * 0.25)
            data["status database"]["血清素serotonin"] = round(100000 - battery_level *1000 * 0.5)
            data["status database"]["多巴胺dopamine"] = round(battery_level *1000 * 0.35)

            yield from printf(f"电池电量：{battery_level}")

        def Neurotransmitter_calculation_activates_memory_increment_and_decrement_values(data):
            # 除以100
            dopamine_processing = float((data["多巴胺dopamine"]) / 100)
            acetylcholine_processing = float((data["乙酰胆碱acetylcholine"]) / 100)
            serotonin_processing = float((data["血清素serotonin"]) / 100)
            endorphin_processing = float((data["内啡肽endorphin"]) / 100)
            substance_P_processing = float((100000 - data["P物质substance P"]) / 100)
            epinephrine_processing = float((data["肾上腺素epinephrine"]) / 100)
            Noradrenaline_processing = float((data["去肾上腺素Noradrenaline"]) / 100)
            GABA_processing = float((data["GABA"]) / 100)
            Glamic_acid_processing = float((data["谷氨酸Glutamic acid"]) / 100)

            Neurotransmitter_calculation_activates_memory_increment_and_decrement_values = round((dopamine_processing + acetylcholine_processing + serotonin_processing + endorphin_processing + substance_P_processing + epinephrine_processing + Noradrenaline_processing + GABA_processing + Glamic_acid_processing) / 8)
            yield from printf(f"激活记忆数据库的增加或减少值：{Neurotransmitter_calculation_activates_memory_increment_and_decrement_values}")
            return Neurotransmitter_calculation_activates_memory_increment_and_decrement_values

        def Neurotransmitter_computational_activation_memory_erasure_threshold(data):
            # 除以100
            dopamine_processing = float((100000 - data["多巴胺dopamine"]) / 100)
            acetylcholine_processing = float((100000 - data["乙酰胆碱acetylcholine"]) / 100)
            serotonin_processing = float((100000 - data["血清素serotonin"]) / 100)
            endorphin_processing = float((100000 - data["内啡肽endorphin"]) / 100)
            substance_P_processing = float((data["P物质substance P"]) / 100)
            epinephrine_processing = float((100000 - data["肾上腺素epinephrine"]) / 100)
            Noradrenaline_processing = float((100000 - data["去肾上腺素Noradrenaline"]) / 100)
            GABA_processing = float((100000 - data["GABA"]) / 100)
            Glamic_acid_processing = float((100000 - data["谷氨酸Glutamic acid"]) / 100)

            value = round((dopamine_processing + acetylcholine_processing + serotonin_processing + endorphin_processing + substance_P_processing + epinephrine_processing + Noradrenaline_processing + GABA_processing + Glamic_acid_processing) / 8)
            yield from printf(f"激活记忆数据库的擦除阈值：{value}")
            return value

        def Initial_weights_when_new_units_are_added_to_activate_the_memory_database(data, Activation_threshold):
            # 除以100
            dopamine_processing = float((data["多巴胺dopamine"]) / 100)
            acetylcholine_processing = float((data["乙酰胆碱acetylcholine"]) / 100)
            serotonin_processing = float((data["血清素serotonin"]) / 100)
            endorphin_processing = float((data["内啡肽endorphin"]) / 100)
            substance_P_processing = float((100000 - data["P物质substance P"]) / 100)
            epinephrine_processing = float((data["肾上腺素epinephrine"]) / 100)
            Noradrenaline_processing = float((data["去肾上腺素Noradrenaline"]) / 100)
            GABA_processing = float((data["GABA"]) / 100)
            Glamic_acid_processing = float((data["谷氨酸Glutamic acid"]) / 100)

            # 计算激活阀值
            number = round((dopamine_processing + acetylcholine_processing + serotonin_processing + endorphin_processing + substance_P_processing + epinephrine_processing + Noradrenaline_processing + GABA_processing + Glamic_acid_processing) / 7 + Activation_threshold)
            yield from printf(f"新知识计入激活记忆数据库时的初始权重：{number}")
            return number

        def Initial_weights_when_combined_units_are_added_to_the_activated_memory_database(data, len_of_combined_units):
            # 除以100
            dopamine_processing = float((data["多巴胺dopamine"]) / 100)
            acetylcholine_processing = float((data["乙酰胆碱acetylcholine"]) / 100)
            serotonin_processing = float((data["血清素serotonin"]) / 100)
            endorphin_processing = float((data["内啡肽endorphin"]) / 100)
            substance_P_processing = float((100000 - data["P物质substance P"]) / 100)
            epinephrine_processing = float((data["肾上腺素epinephrine"]) / 100)
            Noradrenaline_processing = float((data["去肾上腺素Noradrenaline"]) / 100)
            GABA_processing = float((data["GABA"]) / 100)
            Glamic_acid_processing = float((data["谷氨酸Glutamic acid"]) / 100)

            # 计算组合单元计入激活记忆数据库时的初始权重
            number = round((dopamine_processing + acetylcholine_processing + serotonin_processing + endorphin_processing + substance_P_processing + epinephrine_processing + Noradrenaline_processing + GABA_processing + Glamic_acid_processing) / 9 * (3.1 - (len_of_combined_units) / 10))
            yield from printf(f"组合单元计入激活记忆数据库时的初始权重：{number}")
            return number

        def Initial_weight_when_combined_memory_is_not_entered_into_cognitive_database(data, len_of_combined_units):
            # 除以10
            dopamine_processing = float((100000 - data["多巴胺dopamine"]) / 10)
            acetylcholine_processing = float((data["乙酰胆碱acetylcholine"]) / 10)
            serotonin_processing = float((data["血清素serotonin"]) / 10)
            endorphin_processing = float((data["内啡肽endorphin"]) / 10)
            substance_P_processing = float((100000 - data["P物质substance P"]) / 10)
            epinephrine_processing = float((data["肾上腺素epinephrine"]) / 10)
            Noradrenaline_processing = float((data["去肾上腺素Noradrenaline"]) / 10)
            GABA_processing = float((data["GABA"]) / 10)
            Glamic_acid_processing = float((data["谷氨酸Glutamic acid"]) / 10)

            # 计算组合单元计入认知记忆数据库时的初始权重
            number = round((dopamine_processing + acetylcholine_processing + serotonin_processing + endorphin_processing + substance_P_processing + epinephrine_processing + Noradrenaline_processing + GABA_processing + Glamic_acid_processing) / 9 * (2.1 - (len_of_combined_units) / 10))
            yield from printf(f"组合单元计入认知记忆数据库时的初始权重：{number}")
            return number
        
        def calculate_the_appreciation_of_the_combined_unit(data):
            # 除以10
            dopamine_processing = float((100000 - data["多巴胺dopamine"]) / 10)
            acetylcholine_processing = float((data["乙酰胆碱acetylcholine"]) / 10)
            serotonin_processing = float((data["血清素serotonin"]) / 10)
            endorphin_processing = float((data["内啡肽endorphin"]) / 10)
            substance_P_processing = float((100000 - data["P物质substance P"]) / 10)
            epinephrine_processing = float((data["肾上腺素epinephrine"]) / 10)
            Noradrenaline_processing = float((data["去肾上腺素Noradrenaline"]) / 10)
            GABA_processing = float((data["GABA"]) / 10)
            Glamic_acid_processing = float((data["谷氨酸Glutamic acid"]) / 10)

            # 计算组合单元的增值
            number = round((dopamine_processing + acetylcholine_processing + serotonin_processing + endorphin_processing + substance_P_processing + epinephrine_processing + Noradrenaline_processing + GABA_processing + Glamic_acid_processing) / 9)
            yield from printf(f"组合单元的增值：{number}")
            return number

        def Impairment_calculation_of_combined_units(data, percentage):
            # 除以100
            dopamine_processing = float((100000 - data["多巴胺dopamine"]) / 100)
            acetylcholine_processing = float((data["乙酰胆碱acetylcholine"]) / 100)
            serotonin_processing = float((data["血清素serotonin"]) / 100)
            endorphin_processing = float((data["内啡肽endorphin"]) / 100)
            substance_P_processing = float((100000 - data["P物质substance P"]) / 100)
            epinephrine_processing = float((data["肾上腺素epinephrine"]) / 100)
            Noradrenaline_processing = float((data["去肾上腺素Noradrenaline"]) / 100)
            GABA_processing = float((data["GABA"]) / 100)
            Glamic_acid_processing = float((data["谷氨酸Glutamic acid"]) / 100)

            # 计算组合单元的减值
            number = round((dopamine_processing + acetylcholine_processing + serotonin_processing + endorphin_processing + substance_P_processing + epinephrine_processing + Noradrenaline_processing + GABA_processing + Glamic_acid_processing) / 9 * percentage)
            yield from printf(f"组合单元的减值：{number}")
            return number

        def Calculation_for_Valve_Reduction_of_Combined_Units(data):
            # 除以100
            dopamine_processing = float((100000 - data["多巴胺dopamine"]) / 100)
            acetylcholine_processing = float((data["乙酰胆碱acetylcholine"]) / 100)
            serotonin_processing = float((data["血清素serotonin"]) / 100)
            endorphin_processing = float((data["内啡肽endorphin"]) / 100)
            substance_P_processing = float((100000 - data["P物质substance P"]) / 100)
            epinephrine_processing = float((data["肾上腺素epinephrine"]) / 100)
            Noradrenaline_processing = float((data["去肾上腺素Noradrenaline"]) / 100)
            GABA_processing = float((data["GABA"]) / 100)
            Glamic_acid_processing = float((data["谷氨酸Glutamic acid"]) / 100)

            # 计算组合单元的删除阀门
            number = round((dopamine_processing + acetylcholine_processing + serotonin_processing + endorphin_processing + substance_P_processing + epinephrine_processing + Noradrenaline_processing + GABA_processing + Glamic_acid_processing) / 11)
            yield from printf(f"组合单元的删除阀门：{number}")
            return number




        number_occurrences_activated_delivery_elements_in_association_tree = {}

        for i in data["activated memory"]:
            number_occurrences_activated_delivery_elements_in_association_tree[i] = 0

        for j in associative_tree:
            if "Undetermined unit" in associative_tree[j]["IP"]:
                continue
            correspond_key = associative_tree[j]["correspond to"][1]
            if correspond_key in number_occurrences_activated_delivery_elements_in_association_tree:
                number_occurrences_activated_delivery_elements_in_association_tree[correspond_key] += 1


        yield from printf(number_occurrences_activated_delivery_elements_in_association_tree)

        if "激活记忆标记数据库activate_memory_tag_database" not in data["other database"]:
            data["other database"]["激活记忆标记数据库activate_memory_tag_database"] = {}

        if enable_context_input:
            if len(data["other database"]["激活记忆标记数据库activate_memory_tag_database"]) == 0:
                data["other database"]["激活记忆标记数据库activate_memory_tag_database"] = number_occurrences_activated_delivery_elements_in_association_tree
            else:
                for i in data["activated memory"]:
                    difference = number_occurrences_activated_delivery_elements_in_association_tree[i] - data["other database"]["激活记忆标记数据库activate_memory_tag_database"].get(i, 0)
                    increment = yield from Neurotransmitter_calculation_activates_memory_increment_and_decrement_values(data["status database"])
                    data["activated memory"][i]["权重"] += (difference - 2) * increment
                data["other database"]["激活记忆标记数据库activate_memory_tag_database"] = number_occurrences_activated_delivery_elements_in_association_tree

            # 性能：此处只做删键、不修改条目内部, 浅拷贝与深拷贝结果一致
            copy_activated_memory = dict(data["activated memory"])
            threshold = yield from Neurotransmitter_computational_activation_memory_erasure_threshold(data["status database"])
            for i in data["activated memory"]:
                if int(data["activated memory"][i]["权重"]) < threshold:
                    del copy_activated_memory[i]
                    data["other database"]["激活记忆标记数据库activate_memory_tag_database"].pop(i, None)
                    yield from printf(f"激活记忆{i}已擦除")
            data["activated memory"] = copy_activated_memory

        # 计算组合单元的删除阀门
        valve_reduction = yield from Calculation_for_Valve_Reduction_of_Combined_Units(data["status database"])
        Combination_Unit_to_Be_Deleted = []

        for i in data["cognitive database"]:
            if "combination" not in data["cognitive database"][i]["IP"]:
                continue
            if data["cognitive database"][i]["权重"] < valve_reduction:
                Combination_Unit_to_Be_Deleted.append(i)
        yield from printf(f"需要删除的组合单元：{Combination_Unit_to_Be_Deleted}")

        if not enable_knowledge_learning:
            Combination_Unit_to_Be_Deleted = []

        for i in Combination_Unit_to_Be_Deleted:
            IP = data["cognitive database"][i]["IP"]
            del data["cognitive database"][i]
            yield from printf(f"组合单元{i}已删除，IP为{IP}")
            # 性能：此处同样只做删键, 浅拷贝即可, 结果与深拷贝一致
            copy_activated_memory = dict(data["activated memory"])
            TF = False
            for j in data["activated memory"]:
                if data["activated memory"][j]["IP"] == IP:
                    TF = True
                    activated_memory_IP = j
                    del copy_activated_memory[j]
                    yield from printf(f"激活记忆{j}已删除，IP为{IP}")
            if TF:
                data["activated memory"] = copy_activated_memory
                data["other database"]["激活记忆标记数据库activate_memory_tag_database"].pop(activated_memory_IP, None)
                yield from printf(f"激活记忆{activated_memory_IP}的IP为{IP}已除")


        # 性能索引：认知库 IP -> 条目键列表（等价替换逐组合单元全库扫描）
        alt_cog_index = {}
        for k in data["cognitive database"]:
            alt_cog_index.setdefault(tuple(data["cognitive database"][k]["IP"]), []).append(k)

        Alternative_combination_units = {}

        for i in data["cognitive database"]:
            if "combination" in data["cognitive database"][i]["IP"]:
                content = ""
                for j in data["cognitive database"][i]["content"]:
                    for k in alt_cog_index.get(tuple(j), []):
                        content += data["cognitive database"][k]["content"]
                Alternative_combination_units[i] = content

        if not enable_knowledge_learning:
            Alternative_combination_units = {}

        for i in Alternative_combination_units:
            if Alternative_combination_units[i] in Text:
                yield from printf(f"组合单元{Alternative_combination_units[i]}为增值对象")
                weight_plus = yield from calculate_the_appreciation_of_the_combined_unit(data["status database"])
                data["cognitive database"][i]["权重"] += weight_plus
            else:
                yield from printf(f"组合单元{Alternative_combination_units[i]}为减值对象")
                Existing_quantity = 0
                for j in Alternative_combination_units[i]:
                    if j in Text:
                        Existing_quantity += 1
                # does_not_exist_in = len(Alternative_combination_units[i]) - Existing_quantity
                weight_minus = yield from Impairment_calculation_of_combined_units(data["status database"], Existing_quantity / len(Alternative_combination_units[i]))
                data["cognitive database"][i]["权重"] -= weight_minus


        now = datetime.now()
        current_time = [now.year, now.month, now.day, now.hour, now.minute, now.second]
        
        short_term_memory_number = []

        for i in data["short-term memory"]:
            short_term_memory_number.append(int(i))

        if len(short_term_memory_number) == 0:
            this_short_term_memory_number = 0
        else:
            this_short_term_memory_number = max(short_term_memory_number) + 1

        short_term_memory_number_user = []

        for i in data["short-term memory"]:
            if data["short-term memory"][i]["IP"][0] == "user":
                short_term_memory_number_user.append(data["short-term memory"][i]["IP"][-1])

        if len(short_term_memory_number_user) == 0:
            this_short_term_memory_number_user = 0
        else:
            this_short_term_memory_number_user = max(short_term_memory_number_user) + 1

        if enable_context_input:
            data["short-term memory"][str(this_short_term_memory_number)] = {
                "content": Text,
                "IP": [
                    "user",
                    this_short_term_memory_number_user
                ],
                "time": current_time
            }

        


        activatad_memory_number = []
        for i in data["activated memory"]:
            activatad_memory_number.append(int(i))

        if len(activatad_memory_number) == 0:
            this_activatad_memory_number = 0
        else:
            this_activatad_memory_number = max(activatad_memory_number) + 1
        
        activate_valve = yield from calculate_activation_valve(data["status database"])
        Weight_neurotransmitter_calculation_formula_when_storing_IP_input_from_short_term_memory_users_into_activation_memory_n = yield from Weight_neurotransmitter_calculation_formula_when_storing_IP_input_from_short_term_memory_users_into_activation_memory(data["status database"], activate_valve)

        if enable_context_input:
            data["activated memory"][str(this_activatad_memory_number)] = {
                "权重": Weight_neurotransmitter_calculation_formula_when_storing_IP_input_from_short_term_memory_users_into_activation_memory_n,
                "IP": ["short-term memory", "user", this_short_term_memory_number_user]
            }

            data["other database"]["激活记忆标记数据库activate_memory_tag_database"][str(this_activatad_memory_number)] = 0

        short_term_memory_number = []
        for i in data["short-term memory"]:
            short_term_memory_number.append(int(i))

        if len(short_term_memory_number) == 0:
            this_short_term_memory_number = 0
        else:
            this_short_term_memory_number = max(short_term_memory_number) + 1

        short_term_memory_number_ai = []

        for i in data["short-term memory"]:
            if data["short-term memory"][i]["IP"][0] == "ai":
                short_term_memory_number_ai.append(data["short-term memory"][i]["IP"][-1])

        if len(short_term_memory_number_ai) == 0:
            this_short_term_memory_number_ai = 0
        else:
            this_short_term_memory_number_ai = max(short_term_memory_number_ai) + 1
        
        if enable_context_input:
            data["short-term memory"][str(this_short_term_memory_number)] = {
                "content": reply,
                "IP": [
                    "ai",
                    this_short_term_memory_number_ai
                ],
                "time": current_time
            }

        activatad_memory_number = []
        for i in data["activated memory"]:
            activatad_memory_number.append(int(i))

        if len(activatad_memory_number) == 0:
            this_activatad_memory_number = 0
        else:
            this_activatad_memory_number = max(activatad_memory_number) + 1
        
        activate_valve = yield from calculate_activation_valve(data["status database"])
        Weight_neurotransmitter_calculation_formula_when_storing_IP_input_from_short_term_memory_ai_into = yield from Weight_neurotransmitter_calculation_formula_when_storing_IP_input_from_short_term_memory_ai_into_activation_memory(data["status database"], activate_valve)

        if enable_context_input:
            data["activated memory"][str(this_activatad_memory_number)] = {
                "权重": Weight_neurotransmitter_calculation_formula_when_storing_IP_input_from_short_term_memory_ai_into,
                "IP": ["short-term memory", "ai", this_short_term_memory_number_ai]
            }

            data["other database"]["激活记忆标记数据库activate_memory_tag_database"][str(this_activatad_memory_number)] = 0

        Undetermined_Unit_dictionary = {}

        for i in associative_tree:
            if "Undetermined unit" in associative_tree[i]["IP"]:
                if associative_tree[i]["content"] not in Undetermined_Unit_dictionary.values():
                    Undetermined_Unit_dictionary[i] = associative_tree[i]["content"]

        Unrecorded_undetermined_units = []

        for i in Undetermined_Unit_dictionary:
            Unrecorded_undetermined_units.append(i)

        for i in data["cognitive database"]:
            if "basic" in data["cognitive database"][i]["IP"]:
                for j in Undetermined_Unit_dictionary:
                    if associative_tree[j]["content"] == data["cognitive database"][i]["content"]:
                        if j in Unrecorded_undetermined_units:
                            Unrecorded_undetermined_units.remove(j)
                            yield from printf(j)

        if not enable_knowledge_learning:
            Unrecorded_undetermined_units = []

        # 性能：循环内每轮都会插入一条, 键号只需在进入循环前取一次 max, 之后逐轮 +1
        # （与每轮重新搜全库求 max 的结果完全一致）
        _cog_keys = [int(j) for j in data["cognitive database"]]
        this_cognitive_database_number = (max(_cog_keys) + 1) if _cog_keys else 0
        _cog_basic_keys = [int(j) for j in data["cognitive database"] if "basic" in data["cognitive database"][j]["IP"]]
        this_cognitive_database_basic_number = (max(_cog_basic_keys) + 1) if _cog_basic_keys else 0
        _act_keys = [int(j) for j in data["activated memory"]]
        this_activatad_memory_number = (max(_act_keys) + 1) if _act_keys else 0

        for i in Unrecorded_undetermined_units:
            yield from printf(f"未录入的未确定单元：{Unrecorded_undetermined_units}")

            _basic_no = this_cognitive_database_basic_number
            _cog_key = this_cognitive_database_number
            data["cognitive database"][str(_cog_key)] = {
                "content": associative_tree[i]["content"],
                "IP": ["basic", str(_basic_no)]
            }
            # 原逻辑下一轮重算的是"基础单元的实际键号+1"（而非编号+1），这里等价推进
            this_cognitive_database_number = _cog_key + 1
            this_cognitive_database_basic_number = _cog_key + 1

            activate_valve = yield from calculate_activation_valve(data["status database"])
            Weight_number = yield from Initial_weights_when_new_units_are_added_to_activate_the_memory_database(data["status database"], activate_valve)

            if enable_context_input:
                data["activated memory"][str(this_activatad_memory_number)] = {
                    "权重": Weight_number,
                    "IP": ["cognitive database", "basic", str(_basic_no)]
                }
                data["other database"]["激活记忆标记数据库activate_memory_tag_database"][str(this_activatad_memory_number)] = 0
                this_activatad_memory_number += 1

        yield from printf(f"未录入的未确定单元：{Unrecorded_undetermined_units}")

        Combination_units = []

        for i in range(len(Text)):
            for j in range(i + 2, len(Text) + 1):
                if Text[i:j] not in Combination_units:
                    Combination_units.append(Text[i:j])

        Unrecorded_combined_units = copy.deepcopy(Combination_units)

        # 性能索引：认知库 IP -> 条目键列表（含本层刚录入的新基础字，等价替换全库扫描）
        cog_ip_index = {}
        for k in data["cognitive database"]:
            cog_ip_index.setdefault(tuple(data["cognitive database"][k]["IP"]), []).append(k)

        Entered_combined_units = []

        for i in data["cognitive database"]:
            value_of_content_for_index_at_this_moment = ""
            for j in data["cognitive database"][i]["content"]:
                if isinstance(j, list):
                    for k in cog_ip_index.get(tuple(j), []):
                        value_of_content_for_index_at_this_moment += data["cognitive database"][k]["content"]
            Entered_combined_units.append(value_of_content_for_index_at_this_moment)

        yield from printf("666666:" + str(Entered_combined_units))
        yield from printf("777777:" + str(Unrecorded_combined_units))

        copy_Unrecorded_combined_units = copy.deepcopy(Unrecorded_combined_units)

        for i in Unrecorded_combined_units:
            if i in Entered_combined_units:
                yield from printf("888888:" + i)
                copy_Unrecorded_combined_units.remove(i)

        Unrecorded_combined_units = copy.deepcopy(copy_Unrecorded_combined_units)

        if not enable_knowledge_learning:
            Unrecorded_combined_units = []

        # 性能索引：内容 -> 条目键列表（保持插入顺序, 等价替换逐字符全库扫描取首个命中）
        # 循环内新增的组合单元 content 是列表, 与字符比较永不相等, 故索引对本循环全程有效
        cog_content_index = {}
        for k in data["cognitive database"]:
            _c = data["cognitive database"][k]["content"]
            if isinstance(_c, str):
                cog_content_index.setdefault(_c, []).append(k)

        # 性能：键号只取一次 max, 循环内逐条 +1（结果与每轮全库求 max 完全一致）
        _cog_keys = [int(j) for j in data["cognitive database"]]
        this_cognitive_database_number = (max(_cog_keys) + 1) if _cog_keys else 0
        _cog_comb_keys = [int(data["cognitive database"][j]["IP"][-1]) for j in data["cognitive database"] if "combination" in data["cognitive database"][j]["IP"]]
        this_cognitive_database_combined_number = (max(_cog_comb_keys) + 1) if _cog_comb_keys else 0
        _act_keys = [int(j) for j in data["activated memory"]]
        this_activatad_memory_number = (max(_act_keys) + 1) if _act_keys else 0

        for i in Unrecorded_combined_units:
            cognitive_database_combined_content = []

            for k in i:
                for j in cog_content_index.get(k, []):
                    cognitive_database_combined_content.append(data["cognitive database"][j]["IP"])
                    break

            yield from printf(this_cognitive_database_combined_number)

            # 计算组合单元计入认知记忆数据库时的初始权重
            combined_weight_number = yield from Initial_weight_when_combined_memory_is_not_entered_into_cognitive_database(data["status database"], len(i))

            data["cognitive database"][str(this_cognitive_database_number)] = {
                "content": cognitive_database_combined_content,
                "IP": ["combination", str(this_cognitive_database_combined_number)],
                "权重": combined_weight_number,
            }   
            this_cognitive_database_number += 1
            this_cognitive_database_combined_number += 1

            combined_weight_number = yield from Initial_weights_when_combined_units_are_added_to_the_activated_memory_database(data["status database"], len(i))

            if enable_context_input:
                data["activated memory"][str(this_activatad_memory_number)] = {
                    "权重": combined_weight_number,
                    "IP": ["cognitive database", "combination", str(this_cognitive_database_combined_number - 1)],
                }
                data["other database"]["激活记忆标记数据库activate_memory_tag_database"][str(this_activatad_memory_number)] = 0
                this_activatad_memory_number += 1

        Short_term_memory_added_to_activated_memory_database = []
        Cognitive_Unit_added_to_Activated = {}

        # 性能索引：激活库 IP 集合 + 认知库 IP -> 条目键列表
        # （循环内只新增带库名前缀的激活条目，与未加前缀的比对目标永不相等，故索引全程有效）
        activated_ip_set = set()
        for k in data["activated memory"]:
            activated_ip_set.add(tuple(data["activated memory"][k]["IP"]))

        cog_react_index = {}
        for k in data["cognitive database"]:
            cog_react_index.setdefault(tuple(data["cognitive database"][k]["IP"]), []).append(k)

        # 性能：激活库键号只取一次 max, 每次插入后 +1（等价于每轮重扫全库求 max）
        _act_keys = [int(k) for k in data["activated memory"]]
        this_activatad_memory_number = (max(_act_keys) + 1) if _act_keys else 0

        for i in (Text if enable_context_input else ""):
            Pending_Activation_Short_term_Memory_Database = []
            for j in data["short-term memory"]:
                if tuple(data["short-term memory"][j]["IP"]) in activated_ip_set:
                    continue
                if ((data["short-term memory"][j]["content"] == i) or (i in data["short-term memory"][j]["content"])) and (j not in Short_term_memory_added_to_activated_memory_database):
                    yield from printf(f"{data['short-term memory'][j]['content']}内容因输入被激活了，键为{j}")
                    Pending_Activation_Short_term_Memory_Database.append(j)
                    Short_term_memory_added_to_activated_memory_database.append(j)

            for j in Pending_Activation_Short_term_Memory_Database:
                if "ai" in data["short-term memory"][j]["IP"]:
                    activate_valve = yield from calculate_activation_valve(data["status database"])
                    into_weight = yield from Weight_neurotransmitter_calculation_formula_when_storing_IP_input_from_short_term_memory_ai_into_activation_memory(data["status database"], activate_valve)
                elif "user" in data["short-term memory"][j]["IP"]:
                    activate_valve = yield from calculate_activation_valve(data["status database"])
                    into_weight = yield from Weight_neurotransmitter_calculation_formula_when_storing_IP_input_from_short_term_memory_users_into_activation_memory(data["status database"], activate_valve)


                data["activated memory"][str(this_activatad_memory_number)] = {
                    "权重": into_weight,
                    "IP": ["short-term memory"] + data["short-term memory"][j]["IP"],
                }
                data["other database"]["激活记忆标记数据库activate_memory_tag_database"][str(this_activatad_memory_number)] = 0
                this_activatad_memory_number += 1

            Cognitive_Unit_to_Activated = {}
            for j in data["cognitive database"]:
                if tuple(data["cognitive database"][j]["IP"]) in activated_ip_set:
                    continue
                if "combination" in data["cognitive database"][j]["IP"]:    
                    content2 = ""
                    for k in data["cognitive database"][j]["content"]:
                        for l in cog_react_index.get(tuple(k), []):
                            content2 += data["cognitive database"][l]["content"]
                    
                    if ((content2 == i) or (i in content2)):
                        Cognitive_Unit_to_Activated[j] = {"type": "combination", "content": content2}
                        Cognitive_Unit_added_to_Activated[j] = {"type": "combination", "content": content2}
                elif "basic" in data["cognitive database"][j]["IP"]:
                    if ((data["cognitive database"][j]["content"] == i) or (i in data["cognitive database"][j]["content"])):
                        Cognitive_Unit_to_Activated[j] = {"type": "basic", "content": data["cognitive database"][j]["content"]}
                        Cognitive_Unit_added_to_Activated[j] = {"type": "basic", "content": data["cognitive database"][j]["content"]}
            
            for j in Cognitive_Unit_to_Activated:
                if Cognitive_Unit_to_Activated[j]["type"] == "combination":
                    weight = yield from Initial_weight_when_combined_memory_is_not_entered_into_cognitive_database(data["status database"], len(Cognitive_Unit_to_Activated[j]["content"]))
                elif Cognitive_Unit_to_Activated[j]["type"] == "basic":
                    Activation_valve = yield from calculate_activation_valve(data["status database"])
                    weight = yield from Initial_weights_when_new_units_are_added_to_activate_the_memory_database(data["status database"], Activation_valve)

                data["activated memory"][str(this_activatad_memory_number)] = {
                    "权重": weight,
                    "IP": ["cognitive database"] + data["cognitive database"][j]["IP"],
                }
                data["other database"]["激活记忆标记数据库activate_memory_tag_database"][str(this_activatad_memory_number)] = 0
                this_activatad_memory_number += 1


        yield from printf(f"未录入的组合单元：{Unrecorded_combined_units}")

        # ===== 联想知识网络连接线构建 =====
        # 输入里出现的词，相邻建单向线，共现建双向线。
        # 这样"苹果→水果→香蕉"这种多跳联想才能走出来。

        def _basic_content_map(data):
            return {
                tuple(entry["IP"]): entry["content"]
                for entry in data["cognitive database"].values()
                if "basic" in entry["IP"]
            }

        def _combination_content_map(data):
            basic = _basic_content_map(data)
            result = {}
            for entry in data["cognitive database"].values():
                if "combination" not in entry["IP"]:
                    continue
                word = "".join(basic.get(tuple(ref), "") for ref in entry["content"])
                if word:
                    result.setdefault(word, tuple(entry["IP"]))
            return result

        def _ip_by_content(data):
            ip_by_content = {}
            basic = _basic_content_map(data)
            combo = _combination_content_map(data)
            for word, ip in combo.items():
                ip_by_content[word] = ip
            for ip, char in basic.items():
                if char not in ip_by_content:
                    ip_by_content[char] = ip
            return ip_by_content

        def _tokenize(data, text):
            ip_by_content = _ip_by_content(data)
            tokens = []
            pos = 0
            while pos < len(text):
                matched = None
                for size in range(min(4, len(text) - pos), 0, -1):
                    piece = text[pos:pos + size]
                    if piece in ip_by_content:
                        matched = (ip_by_content[piece], piece)
                        pos += size
                        break
                if matched is None:
                    tokens.append((None, text[pos]))
                    pos += 1
                else:
                    tokens.append(matched)
            return tokens

        def _next_line_number(data, line_type):
            return sum(1 for e in data["associative network"].values() if e.get("type") == line_type)

        def _add_line(data, left_ip, right_ip, line_type, weight=1):
            left, right = list(left_ip), list(right_ip)
            if left == right:
                return None
            for entry in data["associative network"].values():
                if entry.get("type") != line_type:
                    continue
                heads = entry.get("content", [])
                if len(heads) != 2:
                    continue
                if line_type == "two-way line":
                    if (heads[0] == left and heads[1] == right) or (heads[0] == right and heads[1] == left):
                        entry["权重"] = int(entry.get("权重", 1)) + weight
                        return None
                else:
                    if heads[0] == left and heads[1] == right:
                        entry["权重"] = int(entry.get("权重", 1)) + weight
                        return None
            number = _next_line_number(data, line_type)
            key = str(max([int(k) for k in data["associative network"]] or [0]) + 1)
            data["associative network"][key] = {
                "IP": ["associative network", line_type, number],
                "type": line_type,
                "content": [left, right],
                "权重": weight,
            }
            return key

        def connect_knowledge_network(data, Text):
            tokens = _tokenize(data, Text)
            words = [ip for ip, _ in tokens if ip is not None]
            if len(words) < 1:
                return
            # 相邻词建单向线（顺序）
            for i in range(len(words) - 1):
                _add_line(data, words[i], words[i + 1], "one-way line", weight=1)
            # 共现词建双向线
            unique = []
            for w in words:
                if w not in unique:
                    unique.append(w)
            for i in range(len(unique)):
                for j in range(i + 1, len(unique)):
                    _add_line(data, unique[i], unique[j], "two-way line", weight=1)

        if enable_knowledge_learning:
            connect_knowledge_network(data, Text)
            yield from printf(f"联想线已构建：{len(data['associative network'])} 条")
        else:
            yield from printf("知识学习已关闭，本轮不构建联想线")

        yield from update_neurotransmitters(data,Text,reply,associative_tree)
        yield from printf("神经递质已更新")
        yield from printf(data["status database"])

        yield from printf("激活记忆数据库已更新")
        yield from printf("短时记忆数据库已更新" if enable_context_input else "上下文知识输入已关闭，本轮未写入短期记忆")

    ai_reply = []
    data_processed = {"activated memory": {}}

    activatad = []
    activate_valve = yield from calculate_activation_valve(data["status database"])
    for i in data["activated memory"]:
        if int(data["activated memory"][i]["权重"]) > activate_valve:
            activatad.append(i)
    data_processed["activated memory"] = activatad
    yield from printf(f"激活记忆：{activatad}")

    TF = True
    index = 0
    while TF:
        Text, Text_Range = yield from input_layer(user, data, index)
        this_reply = yield from call(Text, data, data_processed)
        ai_reply.append(this_reply)
        yield from printf_reply(this_reply)
        index += Text_Range
        if Text_Range <= 0:
            yield from printf("文字注意力范围为零，无法继续推进，已终止输入循环")
            TF = False
        if index >= len(user):
            TF = False
    
    return ai_reply, data#, msg