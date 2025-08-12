import Streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.model_selection import train_test_split
from altair import Chart, mark_line, mark_area, config
config.default_params_schema = {}
config.disable_prefix_default_params = False

# データ生成
np.random.seed(0)
dates = pd.date_range('2020-1-1', '2022-12-31')
df = pd.DataFrame({
    'date': dates,
    'close': np.random.uniform(90, 110, len(dates)),
    'high': np.random.uniform(100, 120, len(dates)),
    'low': np.random.uniform(80, 100, len(dates))
})

# データの表示
with st.sidebar:
    if st.checkbox("データ表示"):
        st.write(df)

st.header("データ")

# データの構成を表示する
with st.expander("データ構成"):
    st.write(df.info())
    st.write(df.describe())

# 移動平均線
def moving_average(df, column, window):
    return df[column].rolling(window).mean()

st.header("移動平均")

col1, col2, col3 = st.columns(3)
if col1.checkbox("_close_20"):
    avg_line = [moving_average(df, "close", 20).iloc[-1]]
with col1:
    st.line_chart(avg_line, title="close_20")
if col2.checkbox("high_50"):
    avg_line = [moving_average(df, "high", 50).iloc[-1]]
with col2:
    st.line_chart(avg_line, title="high_50")
if col3.checkbox("low_30"):
    avg_line = [moving_average(df, "low", 30).iloc[-1]]
with col3:
    st.line_chart(avg_line, title="low_30")

# ボリンジャーバンド
df_boll = df.copy()
df_boll["upper_band"] = df_boll["close"].rolling(20).max()
df_boll["lower_band"] = df_boll["close"].rolling(20).min()

st.header("ボリンジャーバンド")

col1, col2 = st.columns(2)
if col1.checkbox("上限線"):
    boll_line = [df_boll["upper_band"].iloc[-1]]
with col1:
    st.line_chart(boll_line, title="上限線")
if col2.checkbox("下限線"):
    boll_line = [df_boll["lower_band"].iloc[-1]]
with col2:
    st.line_chart(boll_line, title="下限線")

# ダウンロード
download_button = st.download_button("ダウンロード", df.to_csv(index=False))