import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import pandas as pd

# ファイル選択セレクトボックス
file = st.file_uploader("画像ファイルを選択", type=["png", "jpg"])

if file is not None:
    img = Image.open(file)

    # サムネ生成ボタン
    with st.expander("サムネ生成"):
        sample_size = st.text_input("サイズ（px）")
        sample_filter = st.selectbox("フィルタ", ["なし", "グレSCALE", "コントラスト"])

        if st.button("Sample"):
            width, height = map(int, sample_size.split("x"))
            img.thumbnail((width, height))

            if sample_filter == "グレ スケ":
                img = img.convert("L")
            elif sample_filter == "コントラスト":
                img = np.array(img)
                img[:, :, 0] -= np.min(img[:, :, 0])
                img[:, :, 1] -= np.min(img[:, :, 1])
                img[:, :, 2] -= np.min(img[:, :, 2])

            with st.expander("サムネ"):
                st.image(img)

    # ダウンロードボタン
    with st.expander("ダウンロード"):
        sample_size = st.text_input("サイズ（px）")
        sample_format = st.selectbox("形式", ["PNG", "JPEG"])

        if st.button("Download"):
            img.save(f"sample_{st.file_hash(file).hexdigest()}.png")

    # 画像サイズ変更セレクトボックス
    with st.expander("サイズ変更"):
        size_factor = st.number_input("サイズ変更係数")

        if st.button("Size"):
            width, height = img.size
            new_width = int(width * size_factor)
            new_height = int(height * size_factor)
            img = img.resize((new_width, new_height))

    # 画像フィルタボタン
    with st.expander("フィルタ"):
        filter_type = st.selectbox("フィルタ", ["なし", "blur", "contrast"])

        if st.button(filter_type):
            if filter_type == "blur":
                img = img.filter(ImageFilter.GaussianBlur(radius=3))
            elif filter_type == "contrast":
                img = np.array(img)
                img[:, :, 0] *= (2/5)
                img[:, :, 1] *= (6/5)
                img[:, :, 2] *= (4/5)

    # DataFrameとPlotlyチャート
    df = pd.DataFrame(
        columns=["画像", "サイズ(px)", "フィルタ"],
        index=[0],
        data={"blurred": "blurred", "contrast": "contrast"},
    )

    fig = Figure(figsize=(5, 4))
    ax = fig.add_subplot(111)
    if filter_type == "blur":
        img = img.filter(ImageFilter.GaussianBlur(radius=3))
    elif filter_type == "contrast":
        img = np.array(img)
        img[:, :, 0] *= (2/5)
        img[:, :, 1] *= (6/5)
        img[:, :, 2] *= (4/5)

    ax.imshow(img)
    ax.set_title(filter_type)
    st.pyplot(fig)

    # サムネ生成結果
    if file is not None:
        img = Image.open(file)
        img.thumbnail((200, 200))
        st.image(img)

# SIDEBAR
if file is not None:
    with st.sidebar:
        st.write("画像ファイルを選択してください")