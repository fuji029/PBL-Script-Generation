dates = ["0908", "0915", "0922", "0929", "1006"]

s = []
for date in dates:
    with open(f"exp/outputs/{date}/raw.txt", "r") as f:
        data = f.read().replace("\n", "")
        s.append(len(data))
print(s)
print(sum(s))
