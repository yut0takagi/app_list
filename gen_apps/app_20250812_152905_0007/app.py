import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import altair as alt
from sklearn.preprocessing import StandardScaler
from io import BytesIO
import os

# データ生成
np.random.seed(0)
data = {
    'x': np.random.randn(100),
    'y': np.random.randn(100),
    'cat': np.random.choice(['a', 'b'], 100)
}
df = pd.DataFrame(data)

# Streamlit セットアップ
st.title('簡易EDA')
st.sidebar.write('')
st.subheader(' cat ')

# カテゴリー列の選択
category_col = st.sidebar.selectbox(
    ' cat ',
    df['cat'].unique(),
    index=0,
    key='category'
)
if category_col is None:
    st.stop()

# データ Upload
uploaded_file = st.file_uploader(
    'ファイルをアップロード',
    type=['csv'],
    accept_multiple_files=False,
    key='file'
)

if uploaded_file is not None:
    try:
        # CSV を読み込む
        df = pd.read_csv(uploaded_file)

        # データの前処理
        scale = StandardScaler()
        df[['x', 'y']] = scale.fit_transform(df[['x', 'y']])

        # 相関ヒートマップ
        fig = px.scatter(
            df,
            x='x',
            y='y',
            hover_data=['cat'],
            range_x=[df['x'].min(), df['x'].max()],
            range_y=[df['y'].min(), df['y'].max()],
            template='plotly_white'
        )
        st.plotly_chart(fig)

        # EDA
        st.dataframe(df[['x', 'y', 'cat']])

        # 表示するデータの数を選択
        num_rows = st.slider(
            '表示する行数',
            10,
            100,
            20,
            key='num_rows'
        )

        # データを分割
        df_split = df.head(num_rows)

        # 1列で表示
        col1, col2 = st.columns(2)
        with col1:
            st.write(df_split['x'])
        with col2:
            st.write(df_split['y'])

    except Exception as e:
        st.error(str(e))

# ダウンロードボタン
download_button = st.download Button('ファイルをダウンロード')
if download_button:
    if uploaded_file is not None:
        try:
            # CSV を Save
            df.to_csv(uploaded_file, index=False)
            st.success('ファイルがダウンロードされました。')

# サイドバーの表示
st.sidebar.write('')
st.sidebar.write('')