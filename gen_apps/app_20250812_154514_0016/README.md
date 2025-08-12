# Generated Streamlit App

## これは何？
- テーマ: **学習データの特徴量重要度をSHAP風に擬似表示（ダミーモデル）**
- 自動生成された Streamlit アプリ（約300行）。外部API不要、擬似データで動作します。

## 使い方（ローカル）
```bash
# 依存インストール（uv 推奨）
uv pip sync requirements.txt  # uv が無い場合: pip install -r requirements.txt
streamlit run app.py
```

## 構成
- `app.py` … 本体
- `requirements.txt` … 推奨バージョンを pin 済み
- `Dockerfile` / `docker-compose.yml` … 推奨実行環境（後述）

## 推奨実行環境（Docker）
- Python: 3.11 系
- 主要ライブラリ:
  - streamlit==1.37.1
  - pandas==2.2.2
  - numpy==1.26.4
  - plotly==5.23.0

```bash
docker compose up --build
# http://localhost:8501 へアクセス
```

## 生成メタ
```json
{
  "idea": "学習データの特徴量重要度をSHAP風に擬似表示（ダミーモデル）",
  "model": "llama3.2:3b",
  "base_url": "http://127.0.0.1:11434/v1",
  "time": "2025-08-12T15:43:23.930836",
  "lines": 73
}
```
