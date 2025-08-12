import streamlit as st
from PIL import Image, ImageFilter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import altair as alt

# セッションのテキスト
st.title('PIL 画像サムネ生成アプリ')

# 画像ファイルのアップロード
uploaded_file = st.file_uploader('画像をアップロード', type='jpg')
if uploaded_file is not None:
    # 画像をパスシーケンスに保存
    image_path = 'image.jpg'
    with open(image_path, 'wb') as f:
        f.write(uploaded_file.read())

    # 画像サイズ変更
    st.header('サイズ変更')
    with_stretched_image = st.checkbox('拡張', value=False)
    if with_stretched_image:
        img = Image.open(image_path).resize((300, 300))
        img.save('stretched.jpg')

    # 画像フィルタ
    st.header('フィルタ')
    filter_values = ['Blur', 'Contrast', 'Sharpen']
    filter_value = st.selectbox('フィルタを適用する', filter_values)
    if filter_value == 'Blur':
        img = Image.open(image_path).filter(ImageFilter.GaussianBlur(radius=5))
    elif filter_value == 'Contrast':
        img = Image.open(image_path).convert('L').point(lambda x: 255 - x + 128)
    else:
        img = Image.open(image_path).filter(ImageFilter.Sharpen)

    # 画像をグラフに表示
    st.header('画像をグラフに')
    with_stretch_image = st.checkbox('拡張', value=False)
    if with_stretch_image:
        img = img.resize((300, 300))
        plt.imsave('image.png', np.array(img))
        img_plot = alt.Chart(pd.DataFrame({'color': 'RGB'})).mark_image().encode(color='x').properties(title='rgba(255, 0, 0, 1)')('width', 300)
    else:
        img_plot = alt.Chart(data=pd.DataFrame({'color': 'RGB'})).mark_image().encode(color='x').properties(title='rgba(255, 0, 0, 1)')('width', 300)

    # 画像をダウンロード
    st.header('画像をダウンロード')
    with_stretch_download = st.checkbox('拡張', value=False)
    if with_stretch_download:
        img = Image.open(image_path).resize((300, 300))
        download_button = st.button('画像をダウンロード')
        if download_button:
            img.save('downloaded.jpg')

# データ
data = pd.DataFrame({
    'name': ['image1', 'image2', 'image3'],
    'size': [100, 200, 300],
    'width': [50, 75, 150],
    'color': ['red', 'green', 'blue']
})

# より多くのデータを表示する
st.write('画像のデータは次のようになります。')
with st.expander('表示するデータ'):
    st.write(data)
    st.write('画像サイズは300x300pxに拡大されます。')

# 画像のグラフを作成する
def create_graph(data):
    img_plot = alt.Chart(data).mark_image().encode(color='x').properties(title='rgba(255, 0, 0, 1)')('width', 300)
    return img_plot

img_plot = create_graph(data)
st.altair_chart(img_plot)

# 画像をダウンロードする
def download_image(image_path):
    img = Image.open(image_path).resize((300, 300))
    img.save('downloaded.jpg')

download_button = st.button('画像をダウンロード')
if download_button:
    download_image(image_path)