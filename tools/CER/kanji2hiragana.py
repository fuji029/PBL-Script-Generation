from pykakasi import kakasi

kakasi = kakasi()
kakasi.setMode('J', 'H')

conv = kakasi.getConverter()

out = list()
with open("./data/test1.txt", "r") as f:
    data = f.read().rstrip().split("\n")
for line in data:
    if (len(line)):
        out.append(conv.do(line))
    else:
        out.append("")

with open("data/test2-hiragana.txt", "w") as f:
    for line in out:
        f.write(line + "\n")
