# ©2026 何蓝田 个人保留所有权利

import input_layer
import association_layer
import reply_layer
import output_layer
import Connection_layer


def main(user, data):

    msg = []

    def printf(message):
        #msg.append(message)
        yield {"type":"调试","message": message}

    def printf_reply(message):
        yield {"type":"回复","message": message}


    def call(Text, data, data_processed):
        associative_tree = yield from association_layer.association_layer(Text, data, data_processed)
        yield from printf(f"关联树：{associative_tree}")
        reply = yield from reply_layer.reply_layer(Text, data, associative_tree)
        yield from printf(reply)

        output_layer.output_layer(reply)
        yield from Connection_layer.Connection_layer(Text, data, associative_tree, reply)
        return reply

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
        Text, Text_Range = yield from input_layer.input_layer(user, data, index)
        this_reply = yield from call(Text, data, data_processed)
        ai_reply.append(this_reply)
        yield from printf_reply(this_reply)
        index += Text_Range
        if index >= len(user):
            TF = False
    
    return ai_reply, data#, msg