from numpy import number
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

def Waip_AI_DRN(user, data):

    msg = []

    def printf(message):
        #msg.append(message)
        yield {"type":"调试","message": message}

    def printf_reply(message):
        yield {"type":"回复","message": message}

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
        reply = reply_layer(Text, data, associative_tree)
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
                for k in data[IP_database]:
                    if data[IP_database][k]["IP"] == this_IP:
                        if (i == data[IP_database][k]["content"]) or (i in data[IP_database][k]["content"]):
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
        list_of_added_edges = []
        while True:
            stop_index += 1
            copy_associative_tree = copy.deepcopy(associative_tree)

            for i in data["associative network"]:
                associative_unit = {}

                if "two-way line" == data["associative network"][i]["type"]:
                    for j in range(len(data["associative network"][i]["content"])):
                        associative_unit[j] = {"IP":data["associative network"][i]["content"][j], "type":"two-way head"}
                elif "one-way line" == data["associative network"][i]["type"]:
                    for j in range(len(data["associative network"][i]["content"])):
                        associative_unit[j] = {"IP":data["associative network"][i]["content"][j], "type":"one-way head"}

                matching_number = 0
                copy_associative_tree_list = []

                for p in associative_tree:
                    if "Undetermined unit" in associative_tree[p]["IP"]:
                        continue
                    copy_associative_tree_list.append(data[associative_tree[p]["correspond to"][0]][associative_tree[p]["correspond to"][-1]]["IP"])

                if "two-way line" == data["associative network"][i]["type"]:
                    associative_unit_processed = []
                    for w in associative_unit:
                        associative_unit_processed.append(associative_unit[w]["IP"])
                elif "one-way line" == data["associative network"][i]["type"]:
                    associative_unit_processed = []
                    for w in associative_unit:
                        associative_unit_processed.append(associative_unit[w]["IP"]["IP"])

                for q in associative_unit_processed:
                    if q in copy_associative_tree_list:
                        matching_number += 1

                if matching_number == 0 or matching_number == len(associative_unit):
                    continue

                for o in associative_unit:
                    for p in associative_tree:
                        if "Undetermined unit" in associative_tree[p]["IP"]:
                            continue
                        if associative_unit[o]["type"] == "two-way head":
                            if associative_unit[o]["IP"] == data[associative_tree[p]["correspond to"][0]][associative_tree[p]["correspond to"][-1]]["IP"]:
                                if i not in list_of_added_edges:
                                    copy_associative_tree[str(index["main_index"])] = {"IP": ["Confirmed unit", "Subunit", index["Confirmed_Subunit_index"]], "correspond to": associative_tree[p]["correspond to"], "superior unit": [p]}
                                    index["main_index"] += 1
                                    index["Confirmed_Subunit_index"] += 1
                                    list_of_added_edges.append(i)
                                    yield from printf(f"添加成功:{copy_associative_tree[str(index['main_index'] - 1)]}")
                        elif associative_unit[o]["type"] == "one-way head":
                            if associative_unit[o]["IP"]["IP"] == data[associative_tree[p]["correspond to"][0]][associative_tree[p]["correspond to"][-1]]["IP"]:
                                if i not in list_of_added_edges:
                                    copy_associative_tree[str(index["main_index"])] = {"IP": ["Confirmed unit", "Subunit", index["Confirmed_Subunit_index"]], "correspond to": associative_tree[p]["correspond to"], "superior unit": [p]}
                                    index["main_index"] += 1
                                    index["Confirmed_Subunit_index"] += 1
                                    list_of_added_edges.append(i)
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
        
        for i in associative_tree:
            if "Confirmed unit" in associative_tree[i]["IP"]:
                IP = data["activated memory"][associative_tree[i]["correspond to"][-1]]["IP"]
                if (IP[0] == "short-term memory") or (IP[0] == "long-term memory"):
                    continue
                this_database_IP = copy.deepcopy(IP)
                del this_database_IP[0]
                for j in data[IP[0]]:
                    if data[IP[0]][j]["IP"] == this_database_IP:
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
            Weight_neurotransmitter_calculation_formula_when_storing_IP_input_from_short_term_memory_users_into_activation_memory = round((dopamine_processing + acetylcholine_processing + serotonin_processing + endorphin_processing + substance_P_processing + epinephrine_processing + Noradrenaline_processing + GABA_processing + Glamic_acid_processing) / 10 + Activation_threshold)
            yield from printf(f"用户输入计入激活记忆数据库时的初始权重：{Weight_neurotransmitter_calculation_formula_when_storing_IP_input_from_short_term_memory_users_into_activation_memory}")
            return Weight_neurotransmitter_calculation_formula_when_storing_IP_input_from_short_term_memory_users_into_activation_memory
        
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
            Weight_neurotransmitter_calculation_formula_when_storing_IP_input_from_short_term_memory_ai_into_activation_memory = round((dopamine_processing + acetylcholine_processing + serotonin_processing + endorphin_processing + substance_P_processing + epinephrine_processing + Noradrenaline_processing + GABA_processing + Glamic_acid_processing) / 9 + Activation_threshold)
            yield from printf(f"AI输入计入激活记忆数据库时的初始权重：{Weight_neurotransmitter_calculation_formula_when_storing_IP_input_from_short_term_memory_ai_into_activation_memory}")
            return Weight_neurotransmitter_calculation_formula_when_storing_IP_input_from_short_term_memory_ai_into_activation_memory

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


        number_occurrences_activated_delivery_elements_in_association_tree = {}

        for i in data["activated memory"]:
            number_occurrences_activated_delivery_elements_in_association_tree[i] = 0

        for i in data["activated memory"]:
            for j in associative_tree:
                if "Undetermined unit" in associative_tree[j]["IP"]:
                    continue
                if associative_tree[j]["correspond to"][1] == i:
                    number_occurrences_activated_delivery_elements_in_association_tree[i] += 1


        yield from printf(number_occurrences_activated_delivery_elements_in_association_tree)

        if len(data["other database"]["激活记忆标记数据库activate_memory_tag_database"]) == 0:
            data["other database"]["激活记忆标记数据库activate_memory_tag_database"] = number_occurrences_activated_delivery_elements_in_association_tree
        else:
            for i in data["activated memory"]:
                difference = number_occurrences_activated_delivery_elements_in_association_tree[i] - data["other database"]["激活记忆标记数据库activate_memory_tag_database"][i]
                increment = yield from Neurotransmitter_calculation_activates_memory_increment_and_decrement_values(data["status database"])
                data["activated memory"][i]["权重"] += (difference - 2) * increment
            data["other database"]["激活记忆标记数据库activate_memory_tag_database"] = number_occurrences_activated_delivery_elements_in_association_tree

        copy_activated_memory = copy.deepcopy(data["activated memory"])
        threshold = yield from Neurotransmitter_computational_activation_memory_erasure_threshold(data["status database"])
        for i in data["activated memory"]:
            if int(data["activated memory"][i]["权重"]) < threshold:
                del copy_activated_memory[i]
                del data["other database"]["激活记忆标记数据库activate_memory_tag_database"][i]
                yield from printf(f"激活记忆{i}已擦除")
        data["activated memory"] = copy_activated_memory

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
        Weight_neurotransmitter_calculation_formula_when_storing_IP_input_from_short_term_memory_users_into_activation_memory = yield from Weight_neurotransmitter_calculation_formula_when_storing_IP_input_from_short_term_memory_users_into_activation_memory(data["status database"], activate_valve)

        data["activated memory"][str(this_activatad_memory_number)] = {
            "权重": Weight_neurotransmitter_calculation_formula_when_storing_IP_input_from_short_term_memory_users_into_activation_memory,
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
        Weight_neurotransmitter_calculation_formula_when_storing_IP_input_from_short_term_memory_ai_into_activation_memory = yield from Weight_neurotransmitter_calculation_formula_when_storing_IP_input_from_short_term_memory_ai_into_activation_memory(data["status database"], activate_valve)

        data["activated memory"][str(this_activatad_memory_number)] = {
            "权重": Weight_neurotransmitter_calculation_formula_when_storing_IP_input_from_short_term_memory_ai_into_activation_memory,
            "IP": ["short-term memory", "ai", this_short_term_memory_number_ai]
        }

        data["other database"]["激活记忆标记数据库activate_memory_tag_database"][str(this_activatad_memory_number)] = 0

        Undetermined_Unit_dictionary = {}

        for i in associative_tree:
            if "Undetermined unit" in associative_tree[i]["IP"]:
                Undetermined_Unit_dictionary[i] = associative_tree[i]["content"]

        Unrecorded_undetermined_units = []

        for i in Undetermined_Unit_dictionary:
            Unrecorded_undetermined_units.append(i)

        for i in data["cognitive database"]:
            if "basic" in data["cognitive database"][i]["IP"]:
                for j in Undetermined_Unit_dictionary:
                    if associative_tree[j]["content"] == data["cognitive database"][i]["content"]:
                        Unrecorded_undetermined_units.remove(j)
                        yield from printf(j)

        for i in Unrecorded_undetermined_units:
            cognitive_database_number = []

            for j in data["cognitive database"]:
                cognitive_database_number.append(int(j))

            if len(cognitive_database_number) == 0:
                this_cognitive_database_number = 0
            else:
                this_cognitive_database_number = max(cognitive_database_number) + 1
            
            cognitive_database_basic_number = []

            for j in data["cognitive database"]:
                if "basic" in data["cognitive database"][j]["IP"]:
                    cognitive_database_basic_number.append(int(j))

            if len(cognitive_database_basic_number) == 0:
                this_cognitive_database_basic_number = 0
            else:
                this_cognitive_database_basic_number = max(cognitive_database_basic_number) + 1

            yield from printf(f"未录入的未确定单元：{Unrecorded_undetermined_units}")

            data["cognitive database"][str(this_cognitive_database_number)] = {
                "content": associative_tree[i]["content"],
                "IP": ["basic", str(this_cognitive_database_basic_number)]
            }

            activatad_memory_number = []

            for j in data["activated memory"]:
                activatad_memory_number.append(int(j))

            if len(activatad_memory_number) == 0:
                this_activatad_memory_number = 0
            else:
                this_activatad_memory_number = max(activatad_memory_number) + 1

            activate_valve = yield from calculate_activation_valve(data["status database"])
            Weight_number = yield from Initial_weights_when_new_units_are_added_to_activate_the_memory_database(data["status database"], activate_valve)

            data["activated memory"][str(this_activatad_memory_number)] = {
                "权重": Weight_number,
                "IP": ["cognitive database", "basic", str(this_cognitive_database_basic_number)]
            }
            data["other database"]["激活记忆标记数据库activate_memory_tag_database"][str(this_activatad_memory_number)] = 0

        yield from printf(f"未录入的未确定单元：{Unrecorded_undetermined_units}")

        yield from update_neurotransmitters(data,Text,reply,associative_tree)
        yield from printf("神经递质已更新")
        yield from printf(data["status database"])

        yield from printf("激活记忆数据库已更新")
        yield from printf("短时记忆数据库已更新")

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
        if index >= len(user):
            TF = False
    
    return ai_reply, data#, msg