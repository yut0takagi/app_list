import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import plotly.express as px
import altair as alt
import matplotlib.pyplot as plt

# データ擬似生成
np.random.seed(0)
df = pd.DataFrame({
    '緯度': np.random.uniform(-180, 180, 100).round(6),
    '経度': np.random.uniform(-90, 90, 100).round(6),
})

# サイドバー上の選択肢
st.title("地理散布とクラスタリング結果の色分け")

with st.sidebar:
    select = st.selectbox(
        "データを操作したい方法",
        options=["データ表示", "クラスタリング結果の色分け"]
    )

if select == "データ表示":
    df_list = [df, df[['緯度','経度']], df.describe()]
    for i in range(len(df_list)):
        if i == 0:
            st.write("データ")
            fig = px.scatter_mapbox(df_list[i], lat='緯度', lon='経度')
            st.plotly_chart(fig)
        elif i == 1:
            st.write("特定の列")
            fig = px.scatter_mapbox(df_list[i], lat='緯度', lon='経度')
            st.plotly_chart(fig)
        else:
            st.write("データ分析")

elif select == "クラスタリング結果の色分け":
    # クラスタリング
    kmeans = KMeans(n_clusters=5)
    kmeans.fit(df[['緯度','経度']])
    df['cluster'] = kmeans.labels_

    # サイドバー上の選択肢
    col = st.selectbox(
        "色分けはどのクラスターにアピールしますか?",
        options=list(range(1,6))
    )
    if col == 1:
        df['color'] = 'red'
    elif col == 2:
        df['color'] = 'green'
    elif col == 3:
        df['color'] = 'yellow'
    elif col == 4:
        df['color'] = 'blue'
    else:
        df['color'] = 'purple'

    # データ表示
    st.write(df)

# ダウンロードボタン
if st.checkbox("ダウンロード"):
    with open("result.csv", "w") as file:
        pd.DataFrame(df).to_csv(file, index=False)