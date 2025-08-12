import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import plotly.express as px
import altair as alt

# データ生成
np.random.seed(0)
lat = np.random.uniform(-90, 90, 1000)
lon = np.random.uniform(-180, 180, 1000)
df = pd.DataFrame({'緯度': lat, '経度': lon})

# サイドバーのタブを設定する
st.sidebar.title('地理散布とクラスタリング結果')
tab1, tab2, tab3 = st.sidebar.tabs(['データ', 'クラスタリング', '視覚化'])

# タブ(tab1) - データ
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.write('データ')
        st.write(df.head())
    with col2:
        df_info = df.info()
        st.write('\n' + df_info)
        df_desc = df.describe()
        st.write('\n' + df_desc)

# タブ(tab2) - クラスタリング
with tab2:
    st.write('クラスタリング')
    kmeans = KMeans(n_clusters=5, random_state=0).fit(df[['緯度', '経度']])
    cluster_label = kmeans.labels_
    df['クラスタ番号'] = cluster_label

# タブ(tab3) - 視覚化
with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.write('クラスタ分布')
        fig = px.scatter(df, x='緯度', y='経度', hover_data=['クラスタ番号'], color='クラスタ番号')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.write('クラスタデータ')
        df_grouped = df.groupby('クラスタ番号')[' 緯度'].mean().reset_index()
        df_grouped.columns = ['クラスタ番号', '平均緯度']
        fig = alt.Chart(df_grouped).mark_bar().encode(
            x='クラスタ番号:O',
            y='平均緯度:Q',
            color='クラスタ番号:N'
        ).properties(title_text='クラスタデータ')
        st.altair_chart(fig)

    # クラスタ分布図の detail
    with col2:
        fig = px.scatter(df, x='緯度', y='経度', hover_data=['クラスタ番号'], color='クラスタ番号')
        st.write(fig.data[0].layout.title)
        st.write(fig.data[0].layout.yaxis.title)

# Download ボタン
if st.button('Download'):
    df.to_csv('geographic_spread_data.csv', index=False)

# クラスタ数選択ボタン
k_value = int(st.text_input('クラスタ数を選択してください'))

# クラスタリング実行
with tab2:
    if k_value > 0:
        kmeans = KMeans(n_clusters=k_value, random_state=0).fit(df[['緯度', '経度']])
        cluster_label = kmeans.labels_
        df['クラスタ番号'] = cluster_label

# 分類率の計算
if st.button('分類率を計算'):
    from sklearn.metrics import adjusted_rand_score
    y_true = np.unique(cluster_label)
    y_pred = np.unique(kmeans.labels_)
    score = adjusted_rand_score(y_true, y_pred)
    st.write(f'adjusted Rand Index: {score:.3f}')

# クラスタ分布図の変更
if st.button('クラスタ分布図を変更'):
    with tab3:
        col1, col2, col3 = st.columns(3)
        with col1:
            fig = px.scatter(df, x='緯度', y='経度', hover_data=['クラスタ番号'], color='クラステ NUM')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            df_grouped = df.groupby('クラスタ番号')[' 緯度'].mean().reset_index()
            fig = alt.Chart(df_grouped).mark_bar().encode(
                x='クラスタ番号:O',
                y='平均緯度:Q',
                color='クラスタ番号:N'
            ).properties(title_text='クラスタ分布')
            st.altair_chart(fig)

        with col3:
            df_pivot = df.pivot_table(index='クラスタ番号', values=['緯度', '経度'], aggfunc=np.mean)
            fig = px.imshow(df_pivot, title='クラスタ分布')
            st.plotly_chart(fig, use_container_width=True)