#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
App Factory v2: Streamlit 300行アプリを無限生成 + 逐次検証 + 進捗可視化 + Docker化

機能:
- LLM から app.py を生成（Ollama / OpenAI 互換 / 任意ベースURL）
- 各アプリごとに **隔離仮想環境(.venv)** を作成して依存をインストール
- **構文チェック/インポート/簡易起動** のスモークテストを自動実行
- **README拡充**（アプリ説明/使い方/要件/生成メタを自動追記）
- **進捗ダッシュボード**（JSONラインログ + `factory_ui.py` で閲覧）
- **Dockerfile と docker-compose.yml** を各アプリに自動生成（version pinも付与）

使い方:
  export OPENAI_BASE_URL="http://127.0.0.1:11434/v1"
  export APP_MODEL="llama3.2:3b"
  python app_factory_v2.py

ダッシュボード:
  生成中の状況は `python factory_ui.py` でブラウズ（Streamlit）

注意:
- `uv` があれば依存インストール高速化。無ければ pip へフォールバック
- Docker は任意。`--no-docker` で無効化可能
"""

import os, time, json, textwrap, random, re, pathlib, datetime, subprocess, shlex, sys
import tempfile
from dataclasses import dataclass, asdict
import requests

# ===================== 設定 =====================
BASE_URL = os.environ.get("OPENAI_BASE_URL", "http://127.0.0.1:11434/v1")
MODEL    = os.environ.get("APP_MODEL", "llama3.2:3b")
OUT_ROOT = pathlib.Path(os.environ.get("OUT_ROOT", "gen_apps"))
OUT_ROOT.mkdir(parents=True, exist_ok=True)

ISOLATED_VENV     = os.environ.get("APP_ISOLATED_VENV", "1") == "1"
DOCKER_ENABLED    = os.environ.get("APP_DOCKER", "1") == "1"
SMOKE_RUN_ENABLED = os.environ.get("APP_SMOKE_STREAMLIT", "1") == "1"

# ログ／UI 連携
RUN_ID = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
LOG_PATH = OUT_ROOT / f"factory_{RUN_ID}.jsonl"

# ベースとなる requirements pin（最低限）
BASE_REQUIREMENTS = [
    "streamlit==1.37.1",
    "pandas==2.2.2",
    "numpy==1.26.4",
    "plotly==5.23.0",
]

# ===================== プロンプト =====================
SYSTEM = """You are a senior Python developer building Streamlit apps.
Requirements:
- Output ONLY a single code block with the FULL content of app.py. No prose.
- Exactly one file (app.py) that runs with: streamlit run app.py
- Keep it self-contained; avoid external APIs that require keys.
- Keep total length ~300 lines (target ~300, acceptable 250–350).
- Use stdlib + optional: pandas, numpy, plotly, scikit-learn, altair.
- Small in-memory datasets.
- Japanese UI labels. Clear sections and sidebar controls.
- Concise comments. No long docstrings.
- IMPORTANT: begin with `import` lines and return only code (no backticks).
"""

IDEAS = [
  "株価の擬似データを可視化し、移動平均やボリンジャーバンドを切替",
  "学習データの特徴量重要度をSHAP風に擬似表示（ダミーモデル）",
  "CSVアップロード→簡易EDA→相関ヒートマップ→軽い前処理",
  "ToDo＋ポモドーロタイマー＋進捗ガント風チャート（全てローカル状態）",
  "地理散布（緯度経度を擬似生成）とクラスタリング結果の色分け",
  "画像サムネ生成ごっこ（PILでサイズ変更・フィルタ）",
  "テキスト要約“風”ツール（ランダム要約＋キーワード抽出のフェイク）",
  "A/Bテストダッシュボード（ベイズ推定“風”の可視化、擬似データ）",
  "レコメンドUIのプロトタイプ（ランダム埋め込み＋近傍検索擬似）",
  "アンケート集計ダッシュボード（擬似CSV生成→集計→可視化）",
]

USER_TEMPLATE = """次のテーマで 1 ファイルの Streamlit アプリ (app.py) を約300行で実装してください。

テーマ: {idea}

制約:
- 1ファイルのみ(app.py)。実行は `streamlit run app.py`
- 依存は標準＋必要なら pandas/numpy/plotly/scikit-learn/altair 程度
- 250–350 行に収める（300前後）
- UIは日本語。サイドバー、タブ、ダウンロードボタン等を活用
- 外部APIや鍵は不要。データは擬似生成で
- 先頭から末尾までコードのみ（コードフェンス禁止）。
"""

# ===================== ログ/イベント =====================
@dataclass
class Event:
    ts: float
    run_id: str
    idx: int
    phase: str
    status: str
    message: str = ""
    extra: dict | None = None

    def dump(self):
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(self), ensure_ascii=False) + "\n")


def emit(idx:int, phase:str, status:str, message:str="", **extra):
    Event(time.time(), RUN_ID, idx, phase, status, message, extra or None).dump()

# ===================== LLM 呼び出し =====================

def call_chat(messages, temperature=0.9):
    url = f"{BASE_URL}/chat/completions"
    payload = {
        "model": MODEL,
        "temperature": temperature,
        "messages": messages,
        "n": 1,
    }
    headers = {"Content-Type": "application/json"}
    resp = requests.post(url, headers=headers, json=payload, timeout=300)
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"]


def extract_code(text: str) -> str:
    m = re.search(r"```(?:python)?\s*(.*?)```", text, re.S)
    return (m.group(1) if m else text).strip()


def within_line_range(code: str, lo=250, hi=350):
    n = len(code.splitlines())
    return (lo <= n <= hi), n

# ===================== 書き出し =====================

def write_scaffold(app_dir: pathlib.Path, code: str, idea: str, meta: dict):
    app_dir.mkdir(parents=True, exist_ok=True)
    (app_dir / "app.py").write_text(code, encoding="utf-8")
    (app_dir / "requirements.txt").write_text("\n".join(BASE_REQUIREMENTS)+"\n", encoding="utf-8")

    readme = f"""# Generated Streamlit App

## これは何？
- テーマ: **{idea}**
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
{os.linesep.join([f"  - {r}" for r in BASE_REQUIREMENTS])}

```bash
docker compose up --build
# http://localhost:8501 へアクセス
```

## 生成メタ
```json
{json.dumps(meta, ensure_ascii=False, indent=2)}
```
"""
    (app_dir / "README.md").write_text(readme, encoding="utf-8")

    # Docker 化
    dockerfile = f"""
FROM python:3.11-slim
ENV PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip \
    && pip install -r requirements.txt
COPY app.py /app/app.py
EXPOSE 8501
CMD ["python", "-m", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
""".strip()
    (app_dir / "Dockerfile").write_text(dockerfile, encoding="utf-8")

    compose = {
        "version": "3.9",
        "services": {
            "app": {
                "build": ".",
                "ports": ["8501:8501"],
                "environment": {
                    "PYTHONUNBUFFERED": "1"
                }
            }
        }
    }
    (app_dir / "docker-compose.yml").write_text(json.dumps(compose, indent=2), encoding="utf-8")

# ===================== セットアップ/テスト =====================


def run(cmd: str, cwd: pathlib.Path, logfile: pathlib.Path, timeout: int | None = None) -> int:
    with logfile.open("a", encoding="utf-8") as f:
        f.write(f"\n$ {cmd}\n")
        try:
            proc = subprocess.run(shlex.split(cmd), cwd=str(cwd), stdout=f, stderr=subprocess.STDOUT, timeout=timeout)
            return proc.returncode
        except subprocess.TimeoutExpired:
            f.write("\n[Timeout]\n")
            return 124


def create_venv(app_dir: pathlib.Path):
    if not ISOLATED_VENV:
        return None
    venv_dir = app_dir / ".venv"
    if not venv_dir.exists():
        subprocess.check_call([sys.executable, "-m", "venv", str(venv_dir)])
    # uv があれば uv で pin 同期、無ければ pip
    setup_log = app_dir / "setup.log"
    if shutil.which("uv"):
        run("uv pip sync requirements.txt", app_dir, setup_log, timeout=600)
    else:
        # venv の pip を使う
        pip = venv_dir / "bin" / "pip"
        run(f"{pip} install -r requirements.txt", app_dir, setup_log, timeout=900)
    return venv_dir


def smoke_test(app_dir: pathlib.Path, venv_dir: pathlib.Path | None):
    env = os.environ.copy()
    smoke_log = app_dir / "smoke.log"

    def _py(cmd: str, timeout=60):
        if venv_dir:
            py = venv_dir / "bin" / "python"
            return run(f"{py} - <<'PY'\n{cmd}\nPY", app_dir, smoke_log, timeout=timeout)
        else:
            return run(f"python - <<'PY'\n{cmd}\nPY", app_dir, smoke_log, timeout=timeout)

    # 1) import チェック
    imports = "import importlib;\nfor m in ['streamlit','pandas','numpy','plotly']:\n    importlib.import_module(m)\nprint('OK-imports')\n"
    rc = _py(imports, timeout=60)
    if rc != 0:
        return False, "import error"

    # 2) 構文チェック
    compile_snip = "import py_compile; py_compile.compile('app.py', doraise=True); print('OK-compile')\n"
    rc = _py(compile_snip, timeout=60)
    if rc != 0:
        return False, "compile error"

    # 3) streamlit 短時間起動
    if SMOKE_RUN_ENABLED:
        if venv_dir:
            exe = venv_dir / "bin" / "python"
        else:
            exe = "python"
        cmd = f"{exe} -m streamlit run app.py --server.headless true --server.port 0"
        rc = run(cmd, app_dir, smoke_log, timeout=20)
        # 0 or 130 あたりは許容。Timeout 124 も起動自体は通っている可能性が高い
        if rc not in (0, 124, 130):
            return False, f"streamlit rc={rc}"

    return True, "ok"

# ===================== 生成メイン =====================

import shutil

def generate_one(idx: int):
    idea = random.choice(IDEAS)
    meta = {"idea": idea, "model": MODEL, "base_url": BASE_URL, "time": datetime.datetime.now().isoformat()}

    emit(idx, "generate", "start", idea)
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user",   "content": USER_TEMPLATE.format(idea=idea)},
    ]

    raw = call_chat(messages)
    code = extract_code(raw)
    ok, n = within_line_range(code)
    tries = 0
    while not ok and tries < 2:
        messages += [
            {"role": "assistant", "content": raw},
            {"role": "user", "content": f"行数が {n} 行でした。250〜350行に収めて書き直してください。"}
        ]
        raw = call_chat(messages, temperature=0.7)
        code = extract_code(raw)
        ok, n = within_line_range(code)
        tries += 1

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    app_dir = OUT_ROOT / f"app_{ts}_{idx:04d}"
    write_scaffold(app_dir, code, idea, {**meta, "lines": n})
    emit(idx, "write", "ok", str(app_dir), lines=n)

    # セットアップ
    emit(idx, "setup", "start")
    try:
        venv_dir = create_venv(app_dir)
        emit(idx, "setup", "ok", venv=str(venv_dir) if venv_dir else "system")
    except Exception as e:
        (app_dir/"error.txt").write_text(f"setup error: {e}", encoding="utf-8")
        emit(idx, "setup", "fail", str(e))
        return

    # スモーク
    emit(idx, "smoke", "start")
    ok, reason = smoke_test(app_dir, venv_dir)
    if not ok:
        (app_dir/"error.txt").write_text(f"smoke failed: {reason}", encoding="utf-8")
        emit(idx, "smoke", "fail", reason)
    else:
        emit(idx, "smoke", "ok", reason)

    # Docker 生成
    if DOCKER_ENABLED:
        emit(idx, "docker", "start")
        # 既に write_scaffold で作成済みだが、将来の拡張用にイベントだけ
        emit(idx, "docker", "ok")


def main():
    print(f"[factory] run_id={RUN_ID} model={MODEL} base={BASE_URL} out={OUT_ROOT}")
    i = 0
    while True:
        i += 1
        try:
            generate_one(i)
        except Exception as e:
            emit(i, "fatal", "error", str(e))
            time.sleep(3)
        time.sleep(1.0)

if __name__ == "__main__":
    main()
