# PBL-Script-Generation
学部共通PBL 自然言語処理 台本生成チームのリポジトリ

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