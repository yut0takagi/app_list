import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
import altair as Alt

st.title('レコメンドUIのプロトタイプ')

# データ準備
np.random.seed(0)
n_users, n_items = 10, 50
user_item_matrix = np.random.randint(0, 100, size=(n_users, n_items))
item_features = pd.Series(np.random.rand(n_items)).sort_values()
user_features = pd.Series(np.random.rand(n_users)).sort_values()

# 近傍検索擬似とランダム埋め込み
def get_similar_items(item_id):
    similarities = cosine_similarity([item_features.loc[item_id]], user_features)
    return np.argsort(-similarities[0])

def get_similar_items_random(item_id):
    return np.argsort(-user_item_matrix[item_id, :])

# レコメンドウィジェット
st.subheader('レコメンドウィジェット')
item_list = item_features.index[:10]
selected_item = st.selectbox('選択したアイテム', item_list)

if 'similar_items' not in st.session_state:
    st.session_state.similar_items = []
for item in get_similar_items_reco(selected_item):
    st.session_state.similar_items.append(item)
st.write('選択したアイテムの近傍:', st.session_state.similar_items[:10])

# レコメンドウィジェット内
if 'recommended_items' not in st.session_state:
    st.session_state.recommended_items = []
for item in get_similar_items_reco(selected_item):
    if item not in st.session_state.similar_items:
        st.session_state.recommended_items.append(item)

st.write('選択したアイテムの近傍とレコメンド:', st.session_state.recommended_items)

# データビューワ
st.subheader('データビューワ')
df = pd.DataFrame(user_item_matrix, columns=[f'ユーザー{i+1}' for i in range(n_users)], index=item_features.index)
df['ランダム埋め込み'] = user_item_matrix.flatten()
df['ランダム burial類型'] = np.where(df.index.isin(item_features.index), 'アイテム', 'ユーザー')

# データビューワのグラフ
def plot_data():
    fig = Alt.VConcat(
        Alt.H bars(df.loc[:, 'ユーザー1':'ユーザー3'].mean()).encode(x='index', y='mean'),
        Alt.H bars(df.loc[:, ['ランダム burial']].mean()).encode(x='index', y='mean')
    ).properties(title='データビューワ')

    if st.session_state.data_viz:
        return fig
    else:
        return None

fig = plot_data()
if fig is not None:
    st.altair_chart(fig)

# ダウンロードボタン
st.subheader('ダウンロードボタン')
download_button = st.download_button(
    label='データを_download',
    data=df.to_csv(),
    file_name='user_item_matrix.csv'
)