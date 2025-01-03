from difflib import SequenceMatcher
from sys import argv


def CER_line(line1, line2):

    line1 = line1.replace("、", "").replace(
        "。", "").replace("！", "").replace("!", "").replace("・", "").replace(" ", "")
    line2 = line2.replace("、", "").replace(
        "。", "").replace("！", "").replace("!", "").replace("・", "").replace(" ", "")
    s1 = list(line1)
    s2 = list(line2)

    if (not len(s1)):
        return -1

    matcher = SequenceMatcher(None, s1, s2)

    # s2の中で、s1と比較して異なる語のリスト
    diffs = []
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
            diffs.append(f"挿入: {s2[j1:j2]}")
            num_insert += j2 - j1

        if (tag == "delete"):
            diffs.append(f"削除: {s1[i1:i2]}")
            num_delete += i2 - i1

        if (tag == "replace"):
            diffs.append(f"置換: {s1[i1:i2]} -> {s2[j1:j2]}")
            num_replace += i2 - i1

    cer = (num_delete + num_replace + num_insert) / num_char
    if (cer > 0):
        print(f"原文：{line1}")
        print(f"予測：{line2}")
        print("差分：" + " / ".join(diffs))
        print(f"CER:{cer}")
    # print(line2 + "\t" + str(cer))
    return cer


def main():
    if (len(argv) < 3):
        print("Error! 読み込みファイルを指定してください。")
        exit(1)

    path1 = argv[1]
    path2 = argv[2]
    with open(path1, "r") as f:
        data1 = f.read().rstrip().split("\n")
    with open(path2, "r") as f:
        data2 = f.read().rstrip().split("\n")

    cers = []

    for line1, line2 in zip(data1, data2):
        cer = CER_line(line1, line2)
        if (cer != -1):
            cers.append(cer)

    print()
    print("="*20)
    print()
    print(min(cers), max(cers))
    print(f"total CER: {sum(cers)/len(cers)}")


if __name__ == "__main__":
    main()
