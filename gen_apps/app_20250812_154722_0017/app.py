import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import altair as alt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import base64

st.set_page_config(layout="wide")

# ショートカット
sidebar = st.sidebar
tab1, tab2 = st.tabs(["グラフ", "パラメータ"])

# データ生成
np.random.seed(0)
df = pd.DataFrame(
    {
        "date": pd.date_range("2023-01-01", periods=100),
        "open": np.random.uniform(90, 110, size=100),
        "high": np.random.uniform(95, 105, size=100),
        "low": np.random.uniform(85, 95, size=100),
        "close": np.random.uniform(90, 110, size=100),
    }
)

# グラフ
def plot_stock(df):
    fig_open = px.line(df["open"], title="Opening Price")
    fig_high = px.line(df["high"], title="Highest Price")
    fig_low = px.line(df["low"], title="Lowest Price")
    fig_close = px.line(df["close"], title="Closing Price")
    return fig_open, fig_high, fig_low, fig_close

fig_open, fig_high, fig_low, fig_close = plot_stock(df)

# パラメータ
df_mean = df.groupby("date")["close"].mean().resample("M").mean()
fig_mean = alt.Chart(df_mean).mark_line(point=True)
fig_mean.title("Moving Average")

def param():
    with st.expander("移動平均"):
        param_value = df_mean["2023-01"]
        fig = px.bar(x="date", y="value", title="Mean")
        return fig

param()

# ボリンジャーバンド
df_bollungband_open = df.groupby("date")["open"].mean().resample("M").mean()
df_bollungband_high = df.groupby("date")["high"].max().resample("M").max()

fig_banding = alt.Chart(df_bollungband_open).mark_line(point=True)
fig_banding.title("Upper Band")

def select():
    with st.expander("選択"):
        param = ["移動平均", "ボリンジャーバンド"]
        selected = st.selectbox(label=param)
        return selected

selected = select()
if selected == "移動平均":
    fig_mean
elif selected == "ボリンジャーバンド":
    fig_banding

# ダウンロード
download_button = st.download_button(
    label="ダウンロード", 
    data=df.to_excel("download.xlsx").read_excel(), 
    file_format="xlsx"
)

with st.expander("ダウンロッド"):
    with download_button:
        plt.ion()
        fig_down = df.plot.line(subplots=True, figsize=(10,6))
        fig_down.savefig('download.xlsx')

# グラフの表示
st.write(fig_open)
st.write(fig_high)
st.write(fig_low)
st.write(fig_close)

# パラメータの表示
fig_param = param()
st.write(fig_param)