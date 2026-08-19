import copy


def printf(message):
    #msg.append(message)
    yield {"type":"调试","message": message}

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
                                yield from printf(f"添加成功")

            if index["main_index"] == number_branches_associative_tree:
                    break
        if index["main_index"] == number_branches_associative_tree:
            break

        associative_tree = copy.deepcopy(copy_associative_tree)

        if stop_index == number_branches_associative_tree:
            break


    return associative_tree