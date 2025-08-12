import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
import altair as alt

# セットアップ
st.set_page_config(layout="wide")
st.title("A/Bテストダッシュボード")

# データ生成
X, y = make_classification(n_samples=1000, n_features=10, n_informative=5, random_state=42)
df = pd.DataFrame(X, columns=[f"特徴{i+1}" for i in range(10)])
df["ターゲット"] = y

# グラフ生成
fig = px.scatter(df, x="特徴0", y="特徴4", hover_data=["ターゲット"])
st subplot("Scatter Plot")
px.plot(fig)

# ベイズ推定の可視化
df["ベイズプッシ"] = np.random.rand(len(df))  # 擬似データ生成
fig = px.scatter(df, x="特徴0", y="特徴4", color="ベイズプッシ")
st subplot("Scatter Plot with Bayes")
px.plot(fig)

# 模型評価
model_X, model_y = train_test_split(X, test_size=0.2, random_state=42)
model_df = pd.DataFrame(model_X, columns=[f"特徴{i+1}" for i in range(10)])
model_df["ターゲット"] = model_y

# モデルパラメータの可視化
st.subheader("モデル パラメータ")
with st.expander("展開"):
    st.write(model_df.head())

# ダウンロード
download_button = st.download_button(label="データダウンロード", data=df.to_csv(index=False), file_name="data.csv")

# タブ制御
tab1, tab2 = st.tabs(["グラフ", "モデル"])

with tab1:
    fig = px.bar(df, x="特徴0", y="特徴4")
    st subplot("Bar Chart")
    px.plot(fig)

with tab2:
    model = sklearn.tree.DecisionTreeClassifier()
    model.fit(model_X, model_y)
    st.write("モデル")

# ロジストック
st.subheader("ロジスティック")
st.write("ロジスティック")

# ダウンロードボタン
download_button = st.download_button(label="データダウンロード", data=df.to_csv(index=False), file_name="data.csv")

# ペイロード
if st.checkbox("ペイロード"):
    df.to_csv("data.csv", index=False)