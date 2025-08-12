# App Factory

**App Factory** は、300行程度の Python アプリ（例: Streamlit、Flask など）を無限に自動生成するツールです。ローカル LLM（例: Ollama / llama3 系）と連携し、テンプレートベースではなく毎回異なるコードを生成します。生成されたアプリは、仮想環境または Docker 上で自動検証され、エラー発生時には改善案を提示します。

---

## 🚀 主な特徴

* **無限アプリ生成**: ランダムまたは指定テーマで 300 行程度のアプリを自動生成
* **ローカル LLM 直結**: `Ollama` や任意の OpenAI API 互換エンドポイントと連携
* **エラー自動検証**: 仮想環境または Docker で実行し、エラーを改善
* **進捗可視化**: 生成数・進行状況・実行中の処理をリアルタイム表示
* **環境ごとに再現性確保**: ライブラリのバージョンを固定化
* **Docker 検証環境生成**: 各アプリごとに推奨環境を Dockerfile 化

---

## 📦 インストール

```bash
git clone https://github.com/yourname/app-factory.git
cd app-factory
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## ⚙️ 事前準備

1. **Ollama** のインストール
   公式サイトの手順に従いインストール後、モデルを取得します。

   ```bash
   ollama pull llama3.2:3b
   ollama serve
   ```

2. **環境変数の設定**

   ```bash
   export OPENAI_API_KEY=ollama
   export OPENAI_API_BASE=http://127.0.0.1:11434/v1
   ```

---

## ▶ 実行方法

```bash
python app_factory.py \
    --model ollama/llama3.2:3b \
    --output gen_apps \
    --count 5 \
    --docker
```

* `--model` : 使用するモデル名
* `--output` : 生成アプリの保存先ディレクトリ
* `--count` : 生成するアプリ数（無限生成は `--infinite`）
* `--docker` : 各アプリを Docker 環境で検証

---

## 📊 可視化モード

生成状況や現在の処理をリアルタイムで確認できます。

```bash
python monitor.py --dir gen_apps
```

表示される情報:

* 生成完了アプリ数
* 現在生成中のアプリ
* エラー発生率と改善履歴

---

## 🐳 Dockerで実行

各生成アプリごとに `Dockerfile` が自動生成されます。以下のコマンドでコンテナを起動可能です。

```bash
cd gen_apps/app_001
docker build -t app_001 .
docker run -p 8501:8501 app_001
```

---

## 🧪 トラブルシュート

* **生成が遅い/詰まる**: `OLLAMA_NUM_PARALLEL=1` を確認、`--temperature` を下げる、VRAM が少ない場合は小さいモデルを使用
* **依存関係エラー**: 各アプリの `requirements.txt` は固定バージョン。Docker での実行を推奨
* **CORS/接続エラー**: `OPENAI_API_BASE`・ポート番号・Firewall を確認

---

## 📄 今後の改善予定

* 生成アプリのジャンル指定（例: データ可視化 / 機械学習 / Webツール）
* 自動テストコード生成
* GitHub Actions による CI/CD 自動化
* 生成コードのランキング機能（動作安定度・実行速度）

---

## 📜 ライセンス

MIT License
