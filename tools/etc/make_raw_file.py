import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-src', help='エクセルデータへのパス')
parser.add_argument('-dst', help='rawファイルのパス')

args = parser.parse_args()

with open(args.src, "r") as f:
    data = f.read().rstrip().split("\n")
with open(args.dst, "w") as f:
    f.write("".join(data) + "\n")
