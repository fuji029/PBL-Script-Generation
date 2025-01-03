import argparse

paser = argparse.ArgumentParser()

paser.add_argument("-src")

args = paser.parse_args()

with open(args.src, "r") as f:
    data = f.read().rstrip().split("\n")
with open(args.src, "w") as f:
    for line in data:
        line = line.replace(",", "\t")
        f.write(line + "\n")
