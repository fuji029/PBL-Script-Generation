with open("data/cers.txt", "r") as f:
    data = [item.split("\t") for item in f.read().rstrip().split("\n")]
    cers = [float(item[1]) for item in data]
    texts = [item[0] for item in data]
with open("data/cers.swallow.txt", "r") as f:
    data = [item.split("\t") for item in f.read().rstrip().split("\n")]
    cers_s = [float(item[1]) for item in data]
    texts_s = [item[0] for item in data]
idx = [True if cer > cer_s else False for cer, cer_s in zip(cers, cers_s)]
for i in range(len(cers)):
    if cers[i] > cers_s[i]:
        print(texts[i], "→", texts_s[i])
