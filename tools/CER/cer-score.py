from cer import CER_line
import numpy as np
import matplotlib.pyplot as plt

l_cer = []
l_score = []
dirs = ["/home/omasa/pbl/0915/", "data/outputs/0922/"]
files = ["small", "medium", "large-v2"]
for dir in dirs:
    for file in files:
        path_score = dir + file + ".txt"
        path_label = dir + file + ".label.txt"
        with open(path_score, "r") as f:
            data = f.read().rstrip().split("\n")
            pred_text = [line.split(",")[0] for line in data]
            score = [float(line.split(",")[1]) for line in data]
        with open(path_label, "r") as f:
            label = f.read().rstrip().split("\n")

        cers = [CER_line(text, lb)
                for text, lb, sc in zip(pred_text, label, score) if sc < 1]
        cers = [min(cer, 1) for cer in cers]
        score = [sc/(len(text)) for sc, text in zip(score, label) if sc < 1]

        l_cer.extend(cers)
        l_score.extend(score)


print(np.corrcoef(np.array([cers, score])))
print(np.array(score).mean())
plt.scatter(l_score, l_cer)
plt.xlabel("score")
plt.ylabel("CER")
plt.savefig("data/out.png")
