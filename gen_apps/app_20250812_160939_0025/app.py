import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from sklearn.decomposition import PCA
from altair import AltairChart, marks, encoding

st.title("アンケート集計ダッシュボード")
st.subheader("データ生成")
df = pd.DataFrame({
    '質問1': ['選択A', '選択B', '選択C'],
    '質問2': [np.random.randint(0, 10), np.random.randint(0, 10), np.random.randint(0, 10)],
    '質問3': ['回答4', '回答5', '回答6']
})

# データ集計
with st.expander("集計"):
    col1, col2 = st.columns([8, 2])
    with col1:
        df['選考数'] = df.groupby('質問1')['質問1'].transform('count')
        bar_chart = marks.bar(
            x='質問1',
            y='選考数',
            color='color',
            size=10
        )
        st.altair Chart(bar_chart, width=800, height=600)
    with col2:
        st.write("合計数:", df['選考数'].sum())
        st.write("平均値:", df['質問2'].mean())

# データ可視化
with st.expander("可視化"):
    col1, col2 = st.columns([8, 2])
    with col1:
        figs = []
        pca = PCA(df)
        for i in range(3):
            bar_chart = marks.bar(
                x=pca.components_[i, 0],
                y=pca.components_[i, 1],
                color='color',
                size=10
            )
            figs.append(bar_chart)
    with col2:
        st.altair Chart(figs[0] + figs[1], width=800, height=600)

# ダウンロードボタン
if st.button("ダウンロード"):
    df['選考数'] = df.groupby('質問1')['選考数'].transform('sum')
    st.download_button(
        label="擬似 CSV",
        file_type="csv",
        contents=df.to_csv(index=False),
        filename="アンケート集計.csv"
    )