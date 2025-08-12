import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from scipy import stats

# データの生成
np.random.seed(0)
date = pd.date_range('2022-01-01', '2022-12-31')
open_price = np.random.uniform(100, 200, size=len(date))
high_price = open_price + np.random.uniform(0, 10, size=len(date))
low_price = open_price - np.random.uniform(0, 10, size=len(date))

# データfram
df = pd.DataFrame({'Date': date, 'Open': open_price, 'High': high_price, 'Low': low_price})

# Streamlitの設定
st.title('株価データ可視化')
st.sidebar.write('サイドバー')

# ウィジェットの追加
with st.sidebar:
    st.subheader('スキャン')
    st.write('')
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('[**移動平均**](#moving-average)')
        st.write('')
    with col2:
        st.markdown('[**ボリンジャーバンド**](#bollinger-band)')
        st.write('')

with st.expander(' **データ可視化** '):
    fig = go.Figure(data=[go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Open'] + np.random.uniform(0, 10, size=len(date)))])
    st.plotly_chart(fig)

# ウィジェットの追加
col1, col2 = st.columns(2)
with col1:
    st.write('')
    df_mavg = stats.mean(df['High'])
    st.write(f"**移動平均:** {df_mavg:.2f}")
st.write('')

col1, col2 = st.columns(2)
with col1:
    st.write('')
    df_bb = 20 * stats.sem(df['High'])
    st.write(f"**ボリンジャーバンド幅:** {df_bb:.2f}")

# スライスの追加
with st.expander(' **スライス** '):
    st.write('')
    st.write('')
    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure(data=[go.Scatter(x=df.index, y=df['Open'])])
        st.plotly_chart(fig)
    with col2:
        fig = go.Figure(data=[go.Scatter(x=df.index, y=df['Close'])])
        st.plotly_chart(fig)

# 連動スイッチの追加
if st.button('データをダウンロード'):
    st.download_button(label='データをダウンロード', data=df.to_csv(index=False), file_name='data.csv')

with st.expander(' **詳細** '):
    st.write(' ')
    st.write(' ')
    st.write(' ')