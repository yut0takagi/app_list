import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import altair as alt

# 擬似データ生成
np.random.seed(0)
dates = pd.date_range(start='2022-01-01', periods=100)
close_prices = pd.Series(np.random.rand(100) * 100, index=dates).cumsum()

# ステータメントレンド
st.title('株価の擬似データ視覚化')
with st.sidebar:
    st.write('<style>body{font-family: MeireLecart, sans-serif;} </style>', safe=True)
    
    # ステータメントトレンド
    with st.expander("ステータmental_rend"):
        df = pd.DataFrame({'date': dates, 'close_price': close_prices})
        df['moving_avg'] = df['close_price'].rolling(window=20).mean()
        df['volatility'] = np.abs(df['close_price'].diff()).rolling(window=10).mean()

        st.pyplot(px.line(x='date', y=['close_price', 'moving_avg'], title='Close Price and Moving Average'))
        
    # ボリジャンバンド
    with st.expander("ボリジャンバンド"):
        st.write('移動平均に基づいてボリンジャーバンドを切替します。')
        
        df['bollinger_band_upper'] = df['moving_avg'] + 2 * df['volatility']
        df['bollinger_band_lower'] = df['moving_avg'] - 2 * df['volatility']

        st.pyplot(px.line(x='date', y=['close_price', 'bollinger_band_upper'], title='Close Price and Upper Bollinger Band'))
        
    # ボリジャンバンドグラフ
    altair_chart = alt.Vconcat(
        alt.Chart(df).mark_line().encode(x=alt.X('date'), y=alt.Y('close_price')),
        alt.Chart(df).mark_line().encode(x=alt.X('date'), y=alt.Y('bollinger_band_upper'))
    )
    
# ダウンロードボタン
with st.expander("ダウンロード"):
    if st.button("ダウンロード"):
        pd.DataFrame([df]).to_excel('stock_data.xlsx', index=False)
        
# グラフの選択
with st.sidebar:
    st.write('グラフの種類を選択してください。')
    graphs = ['Close Price', 'Moving Average', 'Bollinger Band']
    selected_graph = st.selectbox("グラフ", graphs)

if selected_graph == 'Close Price':
    st.pyplot(px.line(x='date', y=['close_price'], title='Close Price'))
elif selected_graph == 'Moving Average':
    st.pyplot(px.line(x='date', y=['moving_avg'], title='Moving Average'))
else:
    st.pyplot(px.line(x='date', y=['bollinger_band_upper'], title='Upper Bollinger Band'))