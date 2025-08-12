import streamlit as st
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import altair as alt
from datetime import date, timedelta

st.title('レコメンドUI')

# データ生成
np.random.seed(0)
data = {
    'title': ['アパート', '映画', '曲', '本', '旅行'],
    'artist': np.random.choice(['A', 'B', 'C'], size=25),
    'release_date': pd.date_range('20210101', periods=50, freq='D')
}
df = pd.DataFrame(data)

# レコメンドUI
st.write('**選択条件**')

with st.sidebar:
    title = st.selectbox('タイトル', df['title'].unique())
    artist = st.selectbox('アーティスト', df['artist'].unique())

# タブの切り替え
tab = st.tabs(['タブ1', 'タブ2', 'ダウンロード'])

with tab[0]:
    # ランダム埋め込み
    def random_embedding():
        idx = np.random.choice(df.index, size=15)
        return pd.DataFrame({'title': df.loc[idx, 'title'], 
                            'artist': df.loc[idx, 'artist'], 
                            'release_date': df.loc[idx, 'release_date']})

    with st.expander('ランダム埋め込み'):
        random_df = random_embedding()
        st.write(random_df)

with tab[1]:
    # 近傍検索
    def neighbors_search():
        similarity_matrix = cosine_similarity(df[['title', 'artist']], df[['title', 'artist']])
        idx = np.argsort(-similarity_matrix)
        return pd.DataFrame({'index': idx, 
                            ' sims': similarity_matrix[idx]})

    with st.expander('近傍検索'):
        neighbors_df = neighbors_search()
        st.write(neighbors_df)

with tab[2]:
    # ダウンロードボタン
    def download_data():
        data = df.to_csv(index=False)
        return data

    download_button = st.download_button('ダウンロード',  
                                           data=download_data(),  
                                           file_name='data.csv')

if download_button:
    st.success('ダウンロードしました。')