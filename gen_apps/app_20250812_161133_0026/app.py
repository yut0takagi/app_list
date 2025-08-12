import streamlit as st
from PIL import Image, ImageFilter
import numpy as np
import os
import pandas as pd

# Data
df = pd.DataFrame({
    'Image': ['image1.jpg', 'image2.jpg', 'image3.jpg'],
    'Width': [200, 300, 400],
    'Height': [100, 150, 200]
})

# Sidebar
st.sidebar.title('')
st.sidebar.header('')
with st.sidebar.form(key='download'):
    if st.button('Download'):
        for index, row in df.iterrows():
            with open(f'output/{index}.jpg', 'wb') as f:
                f.write(Image.open(row['Image']).resize((row['Width'], row['Height'])).save())
        st.success('画像スムネを生成しました。')

# Main
st.title('')
img = Image.open('image1.jpg')
with st.sidebar.form(key='filter'):
    if st.selectbox('フィルタ', ['None', ' blur ', 'grayscale ']):
        img_filter = img.filter(ImageFilter.MOSAIC)
            .point(lambda x: 0.2 * x + 0.8 * x)
            .convert('L')
    else:
        img_filter = img

st.image(img_filter)

# Tab
tab = st.tabbed(
    ['画像スムネ生成', '画像サイズ変更'],
    ['サイズ変換', 'フィルタ']
)

with tab['画像スムネ生成']:
    df = pd.DataFrame({
        'Image': ['image1.jpg', 'image2.jpg', 'image3.jpg'],
        'Width': [200, 300, 400],
        'Height': [100, 150, 200]
    })
    st.write(df)
    with st.form(key='size'):
        col1, col2 = st.columns(2)
        col1.metric(label='Width', value=str(df['Width'].iloc[0]))
        col2.metric(label='Height', value=str(df['Height'].iloc[0]))
        if st.button('_SIZE'):
            df.loc[0,'Width'] = int(col1.text_input("幅"))
            df.loc[0,'Height'] = int(col2.text_input("高さ"))

with tab['画像サイズ変更']:
    st.selectbox('Size', [200, 300, 400])
    if st.button('_SIZE'):
        df.loc[0,'Width'] = int(st.text_input('Size'))

# Downloads
image = np.array(img)
if os.path.exists('output'):
    for file in os.listdir('output'):
        if file.startswith('output_') and file.endswith(".jpg"):
            os.remove(os.path.join('output', file))
            for new_file in ['output_0.jpg','output_1.jpg','output_2.jpg']:
                os.rename(f"output_{new_file}", f'output_{file}')
with st.download_button(label='ダウンロード', data=np.array_to_base64(image), filename='image.jpg'):
    pass