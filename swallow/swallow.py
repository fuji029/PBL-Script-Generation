import os
import sys
import argparse
import torch
import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM
import bitsandbytes
import re
import time


# プロンプトを準備
PROMPT_DICT = {
    "prompt_input": (
        "以下に、あるタスクを説明する指示があり、それに付随する入力が更なる文脈を提供しています。"
        "リクエストを適切に完了するための回答を記述してください。\n\n"
        "### 指示:\n{instruction}\n\n### 入力:\n{input}\n\n### 応答:"

    ),
    "prompt_no_input": (
        "以下に、あるタスクを説明する指示があります。"
        "リクエストを適切に完了するための回答を記述してください。\n\n"
        "### 指示:\n{instruction}\n\n### 応答:"
    ),
}

# pip install openpyxl


def load_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, help="path/to/Excel_file")
    parser.add_argument("--output", required=True, help="path/to/output_file")
    parser.add_argument("--threshold", required=True,
                        help="float of score threshold")
    return parser.parse_args()


def main():
    args = load_args()

    # トークナイザとモデルの準備
    tokenizer = AutoTokenizer.from_pretrained(
        "tokyotech-llm/Llama-3.1-Swallow-8B-Instruct-v0.2")
    model = AutoModelForCausalLM.from_pretrained(
        "tokyotech-llm/Llama-3.1-Swallow-8B-Instruct-v0.2",
        torch_dtype=torch.bfloat16,
        device_map='auto',
    )
    model.generation_config.temperature = None
    model.generation_config.top_p = None

    # Excelからデータを読み込む
    with open(args.data, "r") as f:
        df = f.read().rstrip().split("\n")

    # Excelから取得したデータの確認

    # promptの定義
    DEFAULT_SYSTEM_PROMPT = "あなたは誠実で優秀な日本人のアシスタントです。"
    query = (
        "指示：以下の文章で音は合っているが文字が誤っている箇所を適切に修正してください。"
        "訂正した文章のみ出力し、それ以外の文章は出力しては行けません。\n"
        "入力：何でも予防を叶えてくださるんですか？\n"
        "出力：何でも要望を叶えてくださるんですか？\n"
        "入力：高速道路でシートベルトをつけていない人の血脂率は\n"
        "出力：高速道路でシートベルトをつけていない人の致死率は\n"
        "入力：夫婦愛も夜景も支柱も激アツ\n"
        "出力：夫婦愛も夜景もシチューも激アツ\n"
        "入力：ソウル風丼を食べる\n"
        "出力：ソウルフードを食べる\n"
        "入力：三黒の世界では\n"
        "出力：ミクロの世界では\n"
        "入力：修士過程を無事に終了した\n"
        "出力：修士課程を無事に修了した\n"
        "入力：このロゴマークは左右対照になっている\n"
        "出力：このロゴマークは左右対称になっている\n"
        "入力：ショート時刻は午後10時\n"
        "出力：消灯時刻は午後10時\n"
        "入力：果汁たっぷりの無しです\n"
        "出力：果汁たっぷりのナシです\n"
        "入力：{input}\n"
        "出力："  # ← ここをいろいろと変えて触ってみてください
    )
    # query = (
    #     "以下の文章のうち、おかしな箇所を修正して出力して。\n"
    #     "何でも予防を叶えてくださるんですか? → 何でも要望を叶えてくださるんですか?\n"
    #     "高速道路でシートベルトをつけていない人の血脂率は → 高速道路でシートベルトをつけていない人の致死率は\n"
    #     "夫婦愛も夜景も支柱も激アツ → 夫婦愛も夜景もシチューも激アツ\n"
    #     "ソウル風丼を食べる → ソウルフードを食べる\n"
    #     "{inputs} → " # ← ここをいろいろと変えて触ってみてください
    # )
    threshold = float(args.threshold)
    with open(args.output, "w") as fout:
        # 各データに対して推論 (校正)
        for i, text in enumerate(df):
            text, score = text.split(",")
            score = float(score)
            if (score > threshold):
                fout.write(text + "\n")
                continue
            start = time.time()
            messages = [
                {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
                {"role": "user", "content": query.format(inputs=text.strip())},
            ]

            # 入力をプロンプトに挿入してtokenize
            input_ids = tokenizer.apply_chat_template(
                messages,
                add_generation_prompt=True,
                return_tensors="pt"
            ).to(model.device)

            terminators = [
                tokenizer.convert_tokens_to_ids("<|end_of_text|>"),
                tokenizer.convert_tokens_to_ids("<|eot_id|>")
            ]

            # 推論を実行
            outputs = model.generate(
                input_ids,
                max_new_tokens=512,
                eos_token_id=terminators,
                pad_token_id=tokenizer.eos_token_id,
                do_sample=False,
                # repetition_penalty=1.1,
            )

            response = outputs[0][input_ids.shape[-1]:]
            response = tokenizer.decode(response, skip_special_tokens=True)

            # 結果を表示
            print(response.replace("\n", " "))
            fout.write(response.replace("\n", " ") + "\n")

            end = time.time()
            # print(f"推論にかかった時間 : {str(end-start)} [s]")


if __name__ == '__main__':
    main()
