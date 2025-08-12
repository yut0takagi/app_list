```python
import streamlit as st
import pandas as pd
import numpy as np
import plotly.exploration_layers as pxl
from sklearn.model_selection import train_test_split
from altair import Chart, mark_point
import io
import base64

# データ生成
np.random.seed(0)
data = {
    'ラベル': ['A', 'B', 'C', 'D', 'E'],
    '値1': np.random.rand(5),
    '値2': np.random.rand(5),
}

df = pd.DataFrame(data)

st.title('CSVアップロード→簡易EDA')

# ページタブ
tab1, tab2, tab3 = st.tabs(['アップロード', 'EDA', 'ヒートマップ'])

with tab1:
    # テキストボックスのインポート
    labeled_importance = st.text_input('ラベル')
    
    # Uploader
    with st.form(key='import-form'):
        file_uploader = st.file_uploader('ファイルアップロード')
        submit_button = st.form_submit_button('アップローダ')

        if submit_button:
            with open(file_uploader.name, 'r') as f:
                df_imported = pd.read_csv(f)
                
            # CSVをデータフレームに変換
            file_name = file_uploader.name.split('.')[0]
            df.file_name = file_name

    st.write('アップローダの例')
    if file_uploader and submit_button:
        st.subheader('アップローダのサンプル')

with tab2:
    if not labeled_importance:
        st.error('ラベルが選択してください')
    else:
        # EDA
        st.write(labeled_importance)
        
        with st.expander('詳細'):
            st.write(df['値1'].describe())
            st.write(df['値2'].describe())
            
            # 連続変数のsummary
            st.subheader('連続変数のsummary')
            st.write(df['値1'].corr())
            
            # 分布的_summary
            st.subheader('分布的_summary')
            st.write(df['値1'].skew())
            st.write(df['値2'].skew())

        # EDAのボタン
        with st.expander('EDAのボタン'):
            if labeled_importance:
                st.write('UDA')
            
            # データ分析のボタン
            with st.form(key='data-analyze-form'):
                analyze_button = st.form_submit_button('データ分析')

                if analyze_button:
                    st.write('データ分析')

with tab3:
    if not labeled_importance:
        st.error('ラベルが選択してください')
    else:
        # ユーザーインターフェース
        st.write(labeled_importance)
        
        # ヒートマップ
        fig = px.bar(df, x=labeled_importance, y='値1', color='値2', text_auto=True)
        
        with st.expander('ヒートマップ'):
            st.altair_chart(fig)

# 保存ボタン
if 'file_name' in df:
    file_buffer = io.BytesIO()
    df.to_csv(file_buffer, index=False)
    
    # ไฟลをダウンロードする
    file_buffer.seek(0)
    download_button = st.download_button(
        label='CSV Download',
        data=file_buffer,
        filename=df.file_name + '.csv',
        mime='text/csv'
    )

# データ分析
if 'file_name' in df:
    # データ分析のボタン
    with st.form(key='data-analyze-form'):
        analyze_button = st.form_submit_button('データ分析')

        if analyze_button:
            st.write('データ分析')