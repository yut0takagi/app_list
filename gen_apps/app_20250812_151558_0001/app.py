import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from altair import AltAirError
import matplotlib.pyplot as plt

# 擬似データ生成
np.random.seed(0)
data = {
    'Date': pd.date_range('2022-01-01', periods=100),
    'Close': np.random.uniform(80, 120, 100)
}
df = pd.DataFrame(data)

def create_app():
    st.title('株価の擬似データ')
    sidebar = st.sidebar

    # データビジュアライザ
    Tabs = ['データ visualizer', '移動平均線', 'ボリンジャーバンド']
    tab1, tab2, tab3 = st.tabs(Tabs)

    # データビューアル
    tab1_chart = tab1.plotly_chart(
        px.line(df['Date'], df['Close'], title='株価', x_axis_label='日付', y_axis_label='開 closing')
    )
    tab1_text = tab1.text("データ visualizer")

    # データの表示
    data_show = st.write("DATA")
    data_show = st.write(df)

    # 移動平均線
    params = st.slider('moving_average_params', (5, 20))
    moving_average_window = int(params[0])
    df['Moving_Avg'] = df['Close'].rolling(moving_average_window).mean()
    tab2_line_plot = tab2.line_plot(df['Date'], df['Moving_Avg'], title='移動平均', x_axis_label='日付', y_axis_label='値')
    tab2_text = tab2.text("移動平均")

    # ボリンジャーバンド
    try:
        params = st.slider('bollinger_band_params', (2, 10))
        moving_average_window = int(params[0])
        standard_deviation = int(params[1]) / 2
        df['Upper_BB'] = df['Close'].rolling(moving_average_window).mean() + standard_deviation
        df['Lower_BB'] = df['Close'].rolling(moving_average_window).mean() - standard_deviation
        tab3_scatter_plot = tab3.scatter_plot(df['Date'], df['Close'], title='ボリンジャーバンド', x_axis_label='値', y_axis_label='')
        tab3_scatter_plot = tab3.scatter_plot(df['Date'], df['Upper_BB'], title='上団線', x_axis_label='%s日平均' % moving_average_window, y_axis_label='')
        tab3_scatter_plot = tab3.scatter_plot(df['Date'], df['Lower_BB'], title='下団線', x_axis_label='%s日平均' % moving_average_window, y_axis_label='')
    except AltAirError:
        tab3_text = "ボリンジャーバンド生成に失敗した"

    # ダウンロード
    download_button = st.download_button(
        label='ダウンロード',
        data=df.to_csv(index=False),
        filename='stock_data.csv'
    )
    return st.container()

if __name__ == "__main__":
    app = create_app()