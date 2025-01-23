from difflib import SequenceMatcher
import argparse


def CER(pred, label):

    pred = pred.replace("、", "").replace(
        "。", "").replace("！", "").replace("!", "").replace("・", "").replace(" ", "")
    label = label.replace("、", "").replace(
        "。", "").replace("！", "").replace("!", "").replace("・", "").replace(" ", "")
    s1 = list(pred)
    s2 = list(label)

    if (not len(s1)):
        return -1

    matcher = SequenceMatcher(None, s2, s1)

    # 正解文字数
    num_char = len(s2)
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

    cer = (num_delete + num_replace + num_insert) / num_char
    print(f"総数:{num_char}, 削除:{num_delete}, 置換:{num_replace}, 挿入:{num_insert}")
    return cer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-pred", help="path to pred data")
    parser.add_argument("-label", help="path to label data")

    args = parser.parse_args()

    with open(args.pred, "r") as f:
        preds = f.read().rstrip().split("\n")
        preds = [item.split(",")[0] for item in preds]
        pred = "".join(preds)
    with open(args.label, "r") as f:
        label = f.read().rstrip().replace("\n", "")

    cer = CER(pred, label)
    print(f"CER = {cer}")


if __name__ == "__main__":
    main()
