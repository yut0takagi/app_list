import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from shap import SHAP
from shap import PlotlyJSBackend
from src.utils import download_data

# セッションスタートする際にダウンロードボタンを表示する
with st.sidebar:
    if 'download_url' in st.session_state:
        st.write('ダウンロードしたデータの特徴量重要度:')
        st.download_button('다운ロード', st.session_state['download_url'])
    
    # 1列に分ける
    col1, col2 = st.columns([4, 6])
    with col1:
        if 'x_data' not in st.session_state:
            st.write('データを読み込みます...')
            x_data, y_data = download_data()
            if len(x_data) < 1000: # 最低1000件のデータ
                x_data, x_test, y_data, y_test = train_test_split(x_data, y_data, test_size=0.2)
        st.session_state['x_data'] = x_data
    
    with col2:
        # セクションを設定する
        with st.expander('ポリマー生成や重要度表示'):
            if 'X' in st.session_state:
                X = pd.DataFrame(st.session_state['x_data'])
                model = RandomForestClassifier(n_estimators=10)
                model.fit(X, y_data)
                
                # SHAPを計算する
                shap = SHAP(model, explainer='lime')
                fig = px.scatter(shap.values, max_display=5)
            
            if 'result' in st.session_state:
                column1, column2 = st.columns(2)
                with column1:
                    col1_text = st.text_input("特徴量の値")
                
                with column2:
                    col2_text = st.text_input("重要度の値")
                    
                    if st.button("表示"):
                        result = model.predict(X[col1_text])
                        if str(result) == col2_text:
                            st.success('正解です!')

# データダウンロード
if not 'download_url' in st.session_state and len(x_data)<1000:
    x_data, y_data = download_data()
    if len(x_data) < 1000: # 最低1000件のデータ
        x_data, x_test, y_data, y_test = train_test_split(x_data, y_data, test_size=0.2)
    st.session_state['x_data'] = x_data