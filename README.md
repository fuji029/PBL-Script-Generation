# PBL-Script-Generation
学部共通PBL 自然言語処理 台本生成チームのリポジトリ

## 概要と機能
テレビ番組のデータ（動画または音声）を入力し、
発話内容を自動で文字起こしして台本を作成し、
Microsoft WordおよびCSV形式で出力する。

## Usage
`whisper.py`または`whisper.ipynb`を使用する。
### 環境構築
以下を実行してインストール
```bash
pip install git+https://github.com/openai/whisper.git
pip install python-docx
```

### データ準備
動画データまたは音声データを`whisper.py`と同じディレクトリに配置する。

### 出力
生成された台本データはMicrosoft Word形式とCSV形式で合計2ファイル出力される。

## その他のファイルについて
1. exp/

    実験用の.pyファイル
2. my_whisper/

    whisperのソースコードを改変し、出力文からlogitsを取り出せるようにした
3. tools/

    CERの測定や正解データのテキストファイルの整形等に用いた.pyファイル

## License
MIT License

Copyright (c) 2022 OpenAI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.