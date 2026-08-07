import copy


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
                    if "combination" in data[IP[0]][j]["IP"]:
                        content = ""
                        for k in data[IP[0]][j]["content"]:
                            for l in data[IP[0]]:
                                if data[IP[0]][l]["IP"] == k:
                                    yield data[IP[0]][l]["IP"]
                                    yield k
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