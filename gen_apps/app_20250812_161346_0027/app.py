import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.decomposition import PCA

# データ生成
np.random.seed(0)
data = pd.DataFrame(np.random.randint(1, 100, size=(100, 3)), columns=['A', 'B', 'C'])

st.title('簡易EDAアプリ')

# CSVアップロード
csv_file = st.file_uploader('CSVファイルを選択', type='csv')

if csv_file is not None:
    # データ読み込み
    df = pd.read_csv(csv_file)
    
    # データ視覚化
    st.subheader('データ視覚化')
    fig = px.scatter(df, x='A', y='B', hover_data=['C'])
    st.plotly_chart(fig)

# EDA
st.subheader('基本統計量')
if df is not None:
    mean_val = df.mean().mean()
    median_val = df.median().mean()
    std_val = df.std().mean()

    st.write(f'mean: {mean_val}')
    st.write(f'median: {median_val}')
    st.write(f'standard deviation: {std_val}')

# 相関ヒートマップ
st.subheader('相関矩阵')
if df is not None:
    corr_matrix = df.corr()
    fig = px.imshow(corr_matrix, text_auto=True)
    st.plotly_chart(fig)

# 前処理（PCA）
pca = PCA(n_components=2)
data_pca = pca.fit_transform(data)

# 相関ヒートマップ（PCAs）
if data_pca is not None:
    corr_pca = data_pca.corr()
    fig = px.imshow(corr_pca, text_auto=True)
    st.plotly_chart(fig)

# ダウンロード
if csv_file is not None:
    st.subheader('ダウンロード')
    st.download_button(label='CSVをダウンロード', data=csv_file.read(), file_name='output.csv')

# サイドバーの追加
with st.sidebar:
    st.markdown('---')
    st.write('**簡易EDAアプリ**')
    st.write('このアプリは、CSVファイルをアップ로드して簡易EDAと相関ヒートマップを使用することを目的としています.')
    st.write('データ生成のため、サンプルデータが使用されます.')

# ページタブ
with st.tabs(['アップロード', 'EDA']):
    with st.tabs('アップロード'):
        if csv_file is not None:
            st.subheader('CSVファイルを選択')
            html = st.markdown(f'**{csv_file.name}**')

            with st.expander('詳細'):
                st.write(csv_file.read())
    
    with st.tabs('EDA'):
        if df is not None:
            st.subheader('基本統計量')
            mean_val = df.mean().mean()
            median_val = df.median().mean()
            std_val = df.std().mean()

            st.write(f'mean: {mean_val}')
            st.write(f'median: {median_val}')
            st.write(f'standard deviation: {std_val}')

# 相関ヒートマップ（PCAs）
with st.tabs('前処理'):
    if data_pca is not None:
        st.subheader('相関ヒートマップ（PCAs）')
        fig = px.imshow(data_pca.corr(), text_auto=True)
        st.plotly_chart(fig)

# ダウンロードボタン
if csv_file is not None:
    st.download_button(label='CSVをダウンロード', data=csv_file.read(), file_name='output.csv')