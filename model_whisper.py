import csv
import argparse
import whisper
import torch
import numpy as np

parser = argparse.ArgumentParser()

parser.add_argument(
    '-model',
    help='Whisperのモデル[tiny, base, small, medium, large-v1, large-v2, large-v3, large, large-v3-turbo, turbo]')
parser.add_argument('-src', help='動画データへのパス')
parser.add_argument('-dst', help='csvファイルのパス')
parser.add_argument('-score', help='scoreファイルへのパス')

args = parser.parse_args()


# modelのロード（large-v2を選択する場合）
model = whisper.load_model(args.model)
# 文字起こし
result = model.transcribe(args.src, temperature=0)
# print(seq_logits)
print(result)
seq_logits_by_line = [seg["logits"] for seg in result["segments"]]


def std_sigmoid(logit):
    return 1/(1+np.exp(-logit))


seq_probs_by_line = []
for logits in seq_logits_by_line:
    seq_probs = []
    for i in range(len(logits)):
        # print("idx: {0}, logit: {1:.2f}, prob: {2:.2f}".format(
        #     torch.argmax(logits[i]).item(),
        #     logits[i].max().item(),
        #     std_sigmoid(logits[i].max().item())
        # ))
        seq_probs.append([std_sigmoid(logits[i].max().item())])
    seq_probs_by_line.append(seq_probs)

with open(args.score, "w") as f:
    for probs, res in zip(seq_probs_by_line, result["segments"]):
        text = res["text"]
        f.write(f"{text},{np.prod(np.array(probs))}\n")


with open(args.dst, 'w', newline='') as csvfile:

    writer = csv.writer(csvfile)

    for segment in result['segments']:
        start = round(segment['start'], 2)
        end = round(segment['end'], 2)
        text = segment['text']
        writer.writerows([[start, end, text]])
