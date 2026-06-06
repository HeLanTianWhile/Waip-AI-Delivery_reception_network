import psutil
import copy
# import random # 你为什么导入了random模

def Waip_AGI(user, data):

    msg = []

    def printf(message):
        #msg.append(message)
        yield message

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
        output_layer(reply)
        executive = Executive_level(Text, data, associative_tree)
        connection = Connection_layer(Text, data, associative_tree, reply, executive)
    
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
        index = {"main_index": 0,"Undetermined_Root_unit_index": 0, "Confirmed_Root_unit_index": 0}
        
        for i in list(Text):
            if index["main_index"] == number_branches_associative_tree:
                break
            associative_tree[str(index["main_index"])] = {"IP": ["Undetermined unit", "Root unit", index["Undetermined_Root_unit_index"]], "content": i}
            index["main_index"] += 1
            index["Undetermined_Root_unit_index"] += 1
        for i in activated_Delivery_reception_unit:
            if index["main_index"] == number_branches_associative_tree:
                break
            associative_tree[str(index["main_index"])] = {"IP": ["Confirmed unit", "Root unit", index["Confirmed_Root_unit_index"]], "correspond to": ["activated memory", i]}
            index["main_index"] += 1
            index["Confirmed_Root_unit_index"] += 1

        临时index = 0
        临时associative_tree = copy.deepcopy(associative_tree)
        while True:

            临时index += 1

            for i in data["associative network"]:
                Receive_pass_the_parent_unit_dictionary={}
                associative_unit = {}

                if "two-way line" == data["associative network"][i]["type"]:
                    pass

                    #########
                    if index["main_index"] == number_branches_associative_tree:
                        break


                associative_tree = copy.deepcopy(临时associative_tree)

                if index["main_index"] == number_branches_associative_tree:
                        break
            if index["main_index"] == number_branches_associative_tree:
                break

            if 临时index == number_branches_associative_tree:
                yield from printf(f"此临时循环已执行{临时index}次，未完成关联树的构建所以将会无限循环，此临时变量将会制止程序")
                break


        return associative_tree

    def reply_layer(Text, data, associative_tree):
        ai_reply = ""
        
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

    def Executive_level(Text, data, associative_tree):
        executive = {}
        return executive

    def Connection_layer(Text, data, associative_tree, reply, executive):
        pass

    ai_reply = ""
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
        yield from call(Text, data, data_processed)
        index += Text_Range
        if index >= len(user):
            TF = False
    
    return ai_reply, data#, msg