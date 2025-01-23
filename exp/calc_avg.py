from difflib import SequenceMatcher

dates = ["0908", "0915", "0922", "0929", "1006"]
models = ["small", "medium", "large-v2"]


def CER(pred, label):

    pred = pred.replace("、", "").replace(
        "。", "").replace("！", "").replace("!", "").replace("・", "").replace(" ", "")
    label = label.replace("、", "").replace(
        "。", "").replace("！", "").replace("!", "").replace("・", "").replace(" ", "")
    s2 = list(pred)
    s1 = list(label)

    if (not len(s1)):
        return -1

    matcher = SequenceMatcher(None, s1, s2)

    # 正解文字数
    num_char = len(s1)
    # 削除文字数
    num_delete = 0
    # 挿入文字数
    num_insert = 0
    # 置換文字数
    num_replace = 0

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if (tag == "insert"):
            num_insert += j2 - j1
            # print('insert', s2[j1:j2], j1, j2, i1)

        if (tag == "delete"):
            num_delete += i2 - i1

        if (tag == "replace"):
            num_replace += i2 - i1

    # print(f"総数:{num_char}, 削除:{num_delete}, 置換:{num_replace}, 挿入:{num_insert}")
    cer = (num_insert + num_delete + num_replace) / num_char
    return cer, [num_insert, num_replace, num_delete]


s = []
result = []
for date in dates:
    res = {}
    with open(f"exp/outputs/{date}/result.csv", "r") as f:
        data = f.read().rstrip().split("\n")[1:]
        for line in data:
            model, time, cer = line.split(",")
            res[model] = [float(time), float(cer)]
    with open(f"exp/outputs/{date}/raw.txt", "r") as f:
        label = f.read().replace("\n", "")
    for model in models:
        with open(f"exp/outputs/{date}/{model}.pred.txt", "r") as f:
            pred = f.read().replace("\n", "")
            cer, items = CER(pred, label)
            res[model].extend(items)
            res[model][1] = float(cer)
    result.append(res)

for model in models:
    time = []
    cer = []
    insert = []
    replace = []
    delete = []
    for res in result:
        time.append(res[model][0])
        cer.append(res[model][1])
        insert.append(res[model][2])
        replace.append(res[model][3])
        delete.append(res[model][4])
    print(f"{model}\n\ttime:{sum(time)/len(time)/3600}\n\tcer:{sum(cer)/len(cer)}\n\tinsert:{sum(insert)}\n\treplace:{sum(replace)}\n\tdelete:{sum(delete)}")
