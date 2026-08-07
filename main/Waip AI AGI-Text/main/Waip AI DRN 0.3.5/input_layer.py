
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
    yield f"文字注意力范围：{text_range}"
    return text_range

def input_layer(user, data, index):
    text_range = yield from Text_Attention_Algorithm(user, data)
    Text = user[index:index+text_range]
    yield f"文字注意力内容：{Text}"
    yield f"当前截止：{index+text_range}"
    return Text, text_range