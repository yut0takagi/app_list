import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import altair as alt

st.title("学習データの特徴量重要度をSHAP風に擬似表示")

# データロード
with st.sidebar:
    data_file = st.file_uploader('データファイルを選択', type='csv')

@st.cache
def load_data(data):
    df = pd.read_csv(data)
    X = df.drop(['target'], axis=1)
    y = df['target']
    return X, y

X, y = load_data(data_file) if data_file else None

# データプリセット
if not X or not y:
    st.write("データが選択されませんでした。")
else:
    st.header('デモ用データ')
    demo_df = pd.DataFrame({
        '特徴量1': [1, 2, 3],
        '特徴量2': [4, 5, 6],
        'target': [0, 1, 0]
    })
    st.write(demo_df)

# トレーニングと評価
st.subheader('トレーニングと評価')
if not X or not y:
    st.header('データが選択されませんでした。')
else:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

# モデル評価
    # accuracy
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    st.write(f" accuracy: {accuracy:.3f}")
    st.write(report)

# SHAP 重要度の可視化
st.subheader('SHAP 重要度')
if not X or not y:
    st.header('データが選択されませんでした。')
else:
    explainer = plotly.explainers.shap.TreeExplainer(model)
    shap_values = explainer.fit_transform(X, y)

    # SHAP 重要度をプロット
    fig = alt.Chart(shap_values).mark_bar(x='feature').encode(x='feature', y='value')
    st.altair(fig)

# ダウンロード
if X is not None:
    st.subheader('ダウンロード')
    download_button = st.download_button(
        label="データ(Excel)",
        data=pd.DataFrame(X, columns=['特徴量1', '特徴量2']).to_csv(index=False),
        file_type='text/csv',
    )