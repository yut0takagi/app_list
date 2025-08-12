import streamlit as st
from PIL import Image
from io import BytesIO
import numpy as np
import altair asalt
from scipy import signal
from sklearn.feature_selection import SelectKBest, mutual_info_regression
import pandas as pd

# 画像ファイル選択
uploaded_file = st.file_uploader("画像ファイルを選択", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:

    # 画像表示
    img = Image.open(uploaded_file)
    st.image(img, width=500)

    # 画像サイズ変更
    row1 = st.columns(2)
    with row1[0]:
        with st.form("size_form"):
            size = st.number_input("サイズ", 1, 1000)
            submitted = st.form_submit_button("サイズ")
            if submitted:
                img = img.resize((int(size), int(size/3.0)))
    with row1[1]:
        with st.form("size_form"):
            size = st.number_input("サイズ", 1, 1000)
            submitted = st.form_submit_button("サイズ")
            if submitted:
                img = img.resize((int(size), int(size/3.0)))

    # 画像フィルタ
    row2 = st.columns(2)
    with row2[0]:
        with st.form("filter_form"):
            kernel_type = st.selectbox("フィルタ", ["gaussian", "sobel"])
            ksize = st.number_input("コンテンツサイズ", 3, 101)
            submitted = st.form_submit_button("フィルタ")
            if submitted:
                if kernel_type == "gaussian":
                    imgfilter = process_image(img, "gaussian", ksize)
                elif kernel_type == "sobel":
                    imgfilter = process_image(img, "sobel", ksize)
    with row2[1]:
        with st.form("filter_form"):
            kernel_type = st.selectbox("フィルタ", ["gaussian", "sobel"])
            ksize = st.number_input("コンテンツサイズ", 3, 101)
            submitted = st.form_submit_button("フィルタ")
            if submitted:
                if kernel_type == "gaussian":
                    imgfilter = process_image(img, "gaussian", ksize)
                elif kernel_type == "sobel":
                    imgfilter = process_image(img, "sobel", ksize)

    # 画像ダウンロード
    row3 = st.columns(2)
    with row3[0]:
        with st.form("down_form"):
            download = st.button("ダウンロード")
            if download:
                img.save("data.png")
    with row3[1]:
        with st.form("down_form"):
            download = st.button("ダウンロード")
            if download:
                imgfilter.save('data2.png')

st.title("画像サムネ生成")

def process_image(image, kernel_type, ksize):
    # 画像サイズ変更
    img = image.resize((int(size), int(size/3.0)))

    # 画像フィルタ
    if kernel_type == "gaussian":
        imgfilter = Gaussian(ksize=ksize).filter(img)
    elif kernel_type == "sobel":
        imgfilter = Sobel(ksize=ksize).filter(img)

    return imgfilter

class ImageFilter(ImageImageProcessor):
    def __init__(self, kernel):
        self.kernel = kernel

    def filter(self, image):
        pixel_data = np.array(image)
        filtered_pixel = np.zeros((pixel_data.shape[0], pixel_data.shape[1]))
        for i in range(pixel_data.shape[0]):
            for j in range(pixel_data.shape[1]):
                total_weight = 0
                for x in range(-1,2):
                    for y in range(-1,2):
                        w = self.kernel[x + 1][y + 1] / 16
                        filtered_pixel[i][j] += pixel_data[i + x][j + y] * w
                        total_weight += abs(w)
                if total_weight != 0:
                    filtered_pixel[i][j] /= total_weight

        return Image.fromarray(filtered_pixel)

class Gaussian(ImageImageProcessor):
    def __init__(self, ksize=3):
        self.ksize = ksize
        self.filter_array = np.zeros((ksize * 2 + 1, ksize * 2 + 1))
        for i in range(self.ksize):
            for j in range(self.ksize):
                self.filter_array[i+j+1][i+j+1] = ((-1)**(i+j)) / (np.pi * (self.ksize ** 2) * self.ksize)
        self.factor = np.exp(-(i + j) ** 2 / (2.0 * (self.ksize ** 2)))

    def filter(self, image):
        pixel_data = np.array(image)
        filtered_pixel = np.zeros((pixel_data.shape[0], pixel_data.shape[1]))
        for i in range(pixel_data.shape[0]):
            for j in range(pixel_data.shape[1]):
                total_weight = 0
                center_x, center_y = int(i + self.ksize / 2), int(j+self.ksize/2)
                for x in range(-int(self.ksize) // 2, int( self.ksize / 2)):
                    for m in range(-int( self.ksize )// 2 , int (self.ksize/2)):
                        w = (self.filter_array[(x + self.ksize)][(y + self.ksize)]) * pixel_data[i+x+center_x][j+y+center_y] * self.factor
                total_weight +=w
                if total_weight !=0:
                    filtered_pixel[i][j]=pixel_data[i center_ x][ ( j + center_y)] * w /2.0/ total_weight

        return Image.fromarray(filtered_pixel)

class Sobel(ImageImageProcessor):
    def __init__(self, ksize):
        self.ksize = ksize
        # horizontal direction filter
        self.xFilter = np.array([
            [-1, 0, 1], [2, -4, 2],
            [1,-2, 1]
        ])
        # Vertical direction filter
        self.yFilter = np.zeros((3, 3))
        for i in range(-1,2):
            for j in range(-1,2):
                self.yFilter[i+j+1][i+j+1] = ((-1)**(i+j)) / (np.sqrt(2) * ksize)
    def filter(self, image):
        pixel_data = np.array(image)
        filtered_pixel = np.zeros((pixel_data.shape[0], pixel_data.shape[1]))
        for i in range(pixel_data.shape[0]):
            for j in range(pixel_data.shape[1]):
                total_weight = 0
                center_x, center_y = int(i + self.ksize / 2), int(j+self.ksize/2)
                for x in range(-int(self.ksize) // 2, int( self.ksize / 2)):
                    for m in range(-int( self.ksize )// 2 , int (self.ksize/2)):
                        w = pixel_data[i+k+center_x][j+m+center_y] * self.xFilter[k][m]*self.factor[0][0] * self.factor [k+m][k+m]
                    total_weight +=w
                if total_weight != 0:
                    filtered_pixel[i][j] = pixel_data[(i+ center_x )][ ( j + center_y)] * w /2.0/ total_weight

        # vertical
        for i in range(pixel_data.shape[0]):
            for j in range(pixel_data.shape[1]):
                total_weight = 0
                for k in  range(-int(self.ksize) // 2, int( self.ksize / 2)):
                    for m in range(-int( self.ksize )// 2 , int (self.ksize/2)):
                        w= pixel_data[i+k+center_x][j+m+center_y]* self.xFilter[k][m] *self.factor[1][1] *w
            total_weight += w

                if total_weight /=0:
                    filtered_pixel[i][j] = pixel_data[i center_ x][ ( j + center_y)] * w /2.0/ total_weight

        return Image.fromarray(filtered_pixel)