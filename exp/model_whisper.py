import csv
import argparse
import whisper
import numpy as np
import time
from cer_full_line import CER

parser = argparse.ArgumentParser()

parser.add_argument(
    '-model',
    help='Whisperのモデル[tiny, base, small, medium, large-v1, large-v2, large-v3, large, large-v3-turbo, turbo]')
parser.add_argument('-date', help='放送日')
parser.add_argument('-gpu', help='which gpu to use')

args = parser.parse_args()


# modelのロード（large-v2を選択する場合）
model = whisper.load_model(args.model, device=f'cuda:{args.gpu}')
# 文字起こし
start = time.time()
# options = whisper.DecodingOptions(task="transcribe", language="ja", best_of=10, beam_size=5)
# options = {"task": "transcribe", "language": "ja", "beam_size": 5}
# result = model.transcribe("data/001.mp3", temperature=0, **options)
result = model.transcribe(f"data/mogitate/{args.date}.mp4", temperature=0)
end = time.time()
print(f"processing time: {end - start} [s]")

with open(f"exp/outputs/{args.date}/raw.txt", "r") as f:
    label = f.read().replace("\n", "")

cer = CER(result["text"], label)
print(f"cer: {cer}")

with open(f"exp/outputs/{args.date}/result.csv", "a") as f:
    f.write(f"{args.model},{end-start},{cer}\n")

with open(f"exp/outputs/{args.date}/{args.model}.pred.txt", "w") as f:
    f.write(result["text"])
