import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import altair as alt
import matplotlib.pyplot as plt

# データ生成
np.random.seed(0)
lat = np.random.uniform(-90, 90, 10000)
lon = np.random.uniform(-180, 180, 10000)

data = pd.DataFrame({
    'Latitude': lat,
    'Longitude': lon
})

st.title('地理散布とクラスタリングの結果')

# サイドバーを使用して、選択肢を表示します。
st.sidebar.header('選択')

with st.sidebar:
    clusters = ['KMeans', 'DBSCAN', 'Hierarchical']
    selected_cluster = st.selectbox(
        "クラスター", 
        clusters
    )

# クラスタリングを実行するボタン
if st.button("クラスタリング"):
    st.write("")
    
    if selected_cluster == 'KMeans':
        kmeans = KMeans(n_clusters=5)
        x_scaled = StandardScaler().fit_transform(data[['Latitude', 'Longitude']])
        kmeans.fit(x_scaled)
        
        # クラスタリング結果の色分け
        fig = px.scatter_3d(
            data=data,
            x='Latitude',
            y='Longitude',
            color=np.random.randint(0, 2, size=len(data)),
            color_discrete_sequence=px.colors.sequencedColor('viridis')
        )
        
        # クラスタリング結果の分析
        clusters_result = kmeans.labels_
        st.write(clusters_result)
        
        # ダウンロードボタン
        download_button = st.download_button(
            label="ダウンロード",
            data=fig.to_html(),
            file_name='map.html'
        )
    
    elif selected_cluster == 'DBSCAN':
        dbscan = KMeans(n_clusters=5)
        x_scaled = StandardScaler().fit_transform(data[['Latitude', 'Longitude']])
        dbscan.fit(x_scaled)
        
        # クラスタリング結果の色分け
        fig = px.scatter_3d(
            data=data,
            x='Latitude',
            y='Longitude',
            color=np.random.randint(0, 2, size=len(data)),
            color_discrete_sequence=px.colors.sequencedColor('viridis')
        )
        
        # クラスタリング結果の分析
        clusters_result = dbscan.labels_
        st.write(clusters_result)
        
        # ダウンロードボタン
        download_button = st.download_button(
            label="ダウンロード",
            data=fig.to_html(),
            file_name='map.html'
        )
    
    elif selected_cluster == 'Hierarchical':
        hierarchical = AgglomerativeClustering(n_clusters=5)
        x_scaled = StandardScaler().fit_transform(data[['Latitude', 'Longitude']])
        hierarchical.fit(x_scaled)
        
        # クラスタリング結果の色分け
        fig = px.scatter_3d(
            data=data,
            x='Latitude',
            y='Longitude',
            color=np.random.randint(0, 2, size=len(data)),
            color_discrete_sequence=px.colors.sequencedColor('viridis')
        )
        
        # クラスタリング結果の分析
        clusters_result = hierarchical.labels_
        st.write(clusters_result)
        
        # ダウンロードボタン
        download_button = st.download_button(
            label="ダウンロード",
            data=fig.to_html(),
            file_name='map.html'
        )