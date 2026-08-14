import copy
import psutil
from datetime import datetime


def printf(message):
    #msg.append(message)
    yield {"type":"调试","message": message}

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

    for i in data["activated memory"]:
        for j in associative_tree:
            if "Undetermined unit" in associative_tree[j]["IP"]:
                continue
            if associative_tree[j]["correspond to"][1] == i:
                number_occurrences_activated_delivery_elements_in_association_tree[i] += 1


    yield from printf(f"{number_occurrences_activated_delivery_elements_in_association_tree}")

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

    # 计算组合单元的删除阀门
    valve_reduction = yield from Calculation_for_Valve_Reduction_of_Combined_Units(data["status database"])
    Combination_Unit_to_Be_Deleted = []

    for i in data["cognitive database"]:
        if "combination" not in data["cognitive database"][i]["IP"]:
            continue
        if data["cognitive database"][i]["权重"] < valve_reduction:
            Combination_Unit_to_Be_Deleted.append(i)
    yield from printf(f"需要删除的组合单元：{Combination_Unit_to_Be_Deleted}")

    for i in Combination_Unit_to_Be_Deleted:
        IP = data["cognitive database"][i]["IP"]
        del data["cognitive database"][i]
        yield from printf(f"组合单元{i}已删除，IP为{IP}")
        copy_activated_memory = copy.deepcopy(data["activated memory"])
        TF = False
        for j in data["activated memory"]:
            if data["activated memory"][j]["IP"] == IP:
                TF = True
                activated_memory_IP = j
                del copy_activated_memory[j]
                yield from printf(f"激活记忆{j}已删除，IP为{IP}")
        if TF:
            data["activated memory"] = copy_activated_memory
            del data["other database"]["激活记忆标记数据库activate_memory_tag_database"][activated_memory_IP]
            yield from printf(f"激活记忆{activated_memory_IP}的IP为{IP}已除")


    Alternative_combination_units = {}

    for i in data["cognitive database"]:
        if "combination" in data["cognitive database"][i]["IP"]:
            content = ""
            for j in data["cognitive database"][i]["content"]:
                for k in data["cognitive database"]:
                    if data["cognitive database"][k]["IP"] == j:
                        content += data["cognitive database"][k]["content"]
            Alternative_combination_units[i] = content

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

    Combination_units = []

    for i in range(len(Text)):
        for j in range(i + 2, len(Text) + 1):
            if Text[i:j] not in Combination_units:
                Combination_units.append(Text[i:j])

    Unrecorded_combined_units = copy.deepcopy(Combination_units)

    Entered_combined_units = []

    for i in data["cognitive database"]:
        value_of_content_for_index_at_this_moment = ""
        for j in data["cognitive database"][i]["content"]:
            for k in data["cognitive database"]:
                if data["cognitive database"][k]["IP"] == j:
                    value_of_content_for_index_at_this_moment += data["cognitive database"][k]["content"]
        Entered_combined_units.append(value_of_content_for_index_at_this_moment)

    yield from printf(f"666666:" + str(Entered_combined_units))
    yield from printf(f"777777:" + str(Unrecorded_combined_units))

    copy_Unrecorded_combined_units = copy.deepcopy(Unrecorded_combined_units)

    for i in Unrecorded_combined_units:
        if i in Entered_combined_units:
            yield from printf(f"888888:" + i)
            copy_Unrecorded_combined_units.remove(i)

    Unrecorded_combined_units = copy.deepcopy(copy_Unrecorded_combined_units)

    for i in Unrecorded_combined_units:
        cognitive_database_number = []
        for j in data["cognitive database"]:
            cognitive_database_number.append(int(j))

        if len(cognitive_database_number) == 0:
            this_cognitive_database_number = 0
        else:
            this_cognitive_database_number = max(cognitive_database_number) + 1 

        cognitive_database_combined_number = []
        for j in data["cognitive database"]:
            if "combination" in data["cognitive database"][j]["IP"]:
                cognitive_database_combined_number.append(int(data["cognitive database"][j]["IP"][-1]))

        if len(cognitive_database_combined_number) == 0:
            this_cognitive_database_combined_number = 0
        else:
            this_cognitive_database_combined_number = max(cognitive_database_combined_number) + 1

        cognitive_database_combined_content = []

        for j in data["cognitive database"]:
            for k in i:
                if data["cognitive database"][j]["content"] == k:
                    cognitive_database_combined_content.append(data["cognitive database"][j]["IP"])

        yield from printf(f"组合单元编号：{this_cognitive_database_combined_number}")    

        # 计算组合单元计入认知记忆数据库时的初始权重
        combined_weight_number = yield from Initial_weight_when_combined_memory_is_not_entered_into_cognitive_database(data["status database"], len(i))

        data["cognitive database"][str(this_cognitive_database_number)] = {
            "content": cognitive_database_combined_content,
            "IP": ["combination", str(this_cognitive_database_combined_number)],
            "权重": combined_weight_number,
        }   

        activatad_memory_number = []
        for j in data["activated memory"]:
            activatad_memory_number.append(int(j))  

        if len(activatad_memory_number) == 0:
            this_activatad_memory_number = 0
        else:
            this_activatad_memory_number = max(activatad_memory_number) + 1 

        combined_weight_number = yield from Initial_weights_when_combined_units_are_added_to_the_activated_memory_database(data["status database"], len(i))

        data["activated memory"][str(this_activatad_memory_number)] = {
            "权重": combined_weight_number,
            "IP": ["cognitive database", "combination", str(this_cognitive_database_combined_number)],
        }
        data["other database"]["激活记忆标记数据库activate_memory_tag_database"][str(this_activatad_memory_number)] = 0

    Short_term_memory_added_to_activated_memory_database = []
    Cognitive_Unit_added_to_Activated = {}

    for i in Text:
        Pending_Activation_Short_term_Memory_Database = []
        for j in data["short-term memory"]:
            TF = False
            for k in data["activated memory"]:
                if data["activated memory"][k]["IP"] == data["short-term memory"][j]["IP"]:
                    TF = True
            if TF:
                continue
            if ((data["short-term memory"][j]["content"] == i) or (i in data["short-term memory"][j]["content"])) and (j not in Short_term_memory_added_to_activated_memory_database):
                yield from printf(f"{data['short-term memory'][j]['content']}内容因输入被激活了，键为{j}")
                Pending_Activation_Short_term_Memory_Database.append(j)
                Short_term_memory_added_to_activated_memory_database.append(j)

        for j in Pending_Activation_Short_term_Memory_Database:
            activatad_memory_number = []

            for k in data["activated memory"]:
                activatad_memory_number.append(int(k))

            if len(activatad_memory_number) == 0:
                this_activatad_memory_number = 0
            else:
                this_activatad_memory_number = max(activatad_memory_number) + 1

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

        Cognitive_Unit_to_Activated = {}
        for j in data["cognitive database"]:
            TF = False
            for k in data["activated memory"]:
                if data["activated memory"][k]["IP"] == data["cognitive database"][j]["IP"]:
                    TF = True
            if TF:
                continue
            if "combination" in data["cognitive database"][j]["IP"]:    
                content2 = ""
                for k in data["cognitive database"][j]["content"]:
                    for l in data["cognitive database"]:
                        if data["cognitive database"][l]["IP"] == k:
                            content2 += data["cognitive database"][l]["content"]
                
                if ((data["cognitive database"][j]["content"] == content2) or (content2 in data["cognitive database"][j]["content"])):
                    Cognitive_Unit_to_Activated[j] = {"type": "combination", "content": content2}
                    Cognitive_Unit_added_to_Activated[j] = {"type": "combination", "content": content2}
            elif "basic" in data["cognitive database"][j]["IP"]:
                if ((data["cognitive database"][j]["content"] == data["cognitive database"][j]["content"])):
                    Cognitive_Unit_to_Activated[j] = {"type": "basic", "content": data["cognitive database"][j]["content"]}
                    Cognitive_Unit_added_to_Activated[j] = {"type": "basic", "content": data["cognitive database"][j]["content"]}
            
        for j in Cognitive_Unit_to_Activated:
            activated_memory_number = []
            for k in data["activated memory"]:
                activated_memory_number.append(int(k))
            if len(activated_memory_number) == 0:
                this_activatad_memory_number = 0
            else:
                this_activatad_memory_number = max(activated_memory_number) + 1

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

    for i in associative_tree:
        if "Root unit" in associative_tree[i]["IP"]:
            continue
        superior_unit = associative_tree[i]["superior unit"]
        yield from printf(f"{i}的上级单元：{associative_tree[str(superior_unit)]}")
        if "Undetermined unit" in associative_tree[str(superior_unit)]["IP"]:
            pass
        else:
            superior_unit_all_IP = associative_tree[str(superior_unit)]["correspond to"]
            superior_unit_IP = copy.deepcopy(superior_unit_all_IP)
            del superior_unit_IP[0]
            for j in data["associative network"]:
                pass


    yield from printf(f"未录入的组合单元：{Unrecorded_combined_units}")

        

    yield from update_neurotransmitters(data,Text,reply,associative_tree)
    yield from printf(f"神经递质已更新")
    yield from printf(data["status database"])

    yield from printf(f"激活记忆数据库已更新")
    yield from printf(f"短时记忆数据库已更新")
