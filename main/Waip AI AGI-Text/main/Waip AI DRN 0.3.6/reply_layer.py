import copy


def printf(message):
    #msg.append(message)
    yield {"type":"调试","message": message}

def reply_layer(Text, data, associative_tree):
    ai_reply = ""
    """
    for i in associative_tree:
        if "Confirmed unit" in associative_tree[i]["IP"]:
            IP = data["activated memory"][associative_tree[i]["correspond to"][-1]]["IP"]
            if (IP[0] == "short-term memory") or (IP[0] == "long-term memory"):
                continue
            this_database_IP = copy.deepcopy(IP)
            del this_database_IP[0]
            for j in data[IP[0]]:
                if data[IP[0]][j]["IP"] == this_database_IP:
                    if "combination" in data[IP[0]][j]["IP"]:
                        content = ""
                        for k in data[IP[0]][j]["content"]:
                            for l in data[IP[0]]:
                                if data[IP[0]][l]["IP"] == k:
                                    yield from printf(data[IP[0]][l]["IP"])
                                    yield from printf(k)
                                    content += data[IP[0]][l]["content"]
                        ai_reply += content
                    else:
                        ai_reply += data[IP[0]][j]["content"]
        elif "Undetermined unit" in associative_tree[i]["IP"]:
            ai_reply += associative_tree[i]["content"]
        ai_reply += " "
    """
    
    Determine_cell_coefficient_values_of_root_grown_cells = 0.618
    Undetermined_cell_coefficient_values_grown_root_cell = 1

    The_coefficient_values_of_each_unit = {}
    index = 0

    for i in associative_tree:
        if "Confirmed unit" in associative_tree[i]["IP"]:
            root_unit_type = None
            if "Root unit" in associative_tree[i]["IP"]:
                root_unit_type = "Confirmed unit"
            else:
                The_parent_unit_for_this_time = associative_tree[i]["superior unit"]
                while True:
                    print(associative_tree[i])
                    if "Root unit" in associative_tree[The_parent_unit_for_this_time]["IP"]:
                        root_unit_type = associative_tree[The_parent_unit_for_this_time]["IP"][0]
                        break
                    The_parent_unit_for_this_time = associative_tree[The_parent_unit_for_this_time]["superior unit"]
            TF = False
            for j in The_coefficient_values_of_each_unit:
                if "Undetermined unit" in The_coefficient_values_of_each_unit[j]:
                    continue
                if associative_tree[i]["IP"] == The_coefficient_values_of_each_unit[j]["IP"]:
                    TF = True
                    break
            if TF:
                if root_unit_type == "Confirmed unit":
                    The_coefficient_values_of_each_unit[j]["Confirmed number"] += 1
                else:
                    The_coefficient_values_of_each_unit[j]["Undetermined number"] += 1
            else:
                if root_unit_type == "Confirmed unit":
                    The_coefficient_values_of_each_unit[index] = {
                        "type": "Confirmed unit",
                        "index": i,
                        "IP": associative_tree[i]["IP"],
                        "Confirmed number": 1,
                        "Undetermined number": 0,
                    } 
                else:
                    The_coefficient_values_of_each_unit[index] = {
                        "type": "Undetermined unit",
                        "index": i,
                        "IP": associative_tree[i]["IP"],
                        "Confirmed number": 0,
                        "Undetermined number": 1,
                    }
                index += 1
        elif "Undetermined unit" in associative_tree[i]["IP"]:
            TF = False
            for j in The_coefficient_values_of_each_unit:
                if "Confirmed unit" in The_coefficient_values_of_each_unit[j]:
                    continue
                if associative_tree[i]["IP"] == The_coefficient_values_of_each_unit[j]["IP"]:
                    TF = True
                    break
            if TF:
                The_coefficient_values_of_each_unit[j]["Undetermined number"] += 1
            else:
                The_coefficient_values_of_each_unit[index] = {
                    "type": "Undetermined unit",
                    "index": i,
                    "content": associative_tree[i]["content"],
                    "Confirmed number": 0,
                    "Undetermined number": 1,
                }
                index += 1

    weight_unit = {}

    for i in The_coefficient_values_of_each_unit:
        weight_unit[i] = (The_coefficient_values_of_each_unit[i]["Confirmed number"] * Determine_cell_coefficient_values_of_root_grown_cells) + (The_coefficient_values_of_each_unit[i]["Undetermined number"] * Undetermined_cell_coefficient_values_grown_root_cell)

    ai_reply = weight_unit

    if ai_reply == "":
        ai_reply = "系统错误，无法理解问题。"

    return ai_reply