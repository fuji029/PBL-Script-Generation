import matplotlib.pyplot as plt
import argparse
import numpy as np

parser = argparse.ArgumentParser()

parser.add_argument('-src', help='scoreデータへのパス')
parser.add_argument('-dst', help='matplotlibの画像出力のパス')

args = parser.parse_args()

with open(args.src, "r") as f:
    data = f.read().rstrip().split("\n")

scores = np.array([float(line.split(",")[1]) for line in data])
# plt.hist(scores, bins=255)
# plt.savefig(args.dst)

threshold = [0.8, 0.85, 0.9] + [0.01 * i +
                                0.9 for i in range(1, 10)] + [0.001 * i + 0.99 for i in range(1, 11)]
for t in threshold:
    print(f"{t}, {np.count_nonzero(scores < t)}")
