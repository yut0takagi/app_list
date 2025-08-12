import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import shap
import plotly.express as px
import altair as alt
import matplotlib.pyplot as plt

# データ生成
np.random.seed(0)
X = np.random.rand(100, 4)  # feature
y = (X[:, 0] > 0.5).astype(int)  # target

# データ分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ダミーモデル生成
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# SHAP 値の計算
shap_values = shap.TreeExplainer(model).fit(X_train)

# UI設定
st.title('SHAP 値の重要度')

with st.expander("データ"):
    with st.expander("特徴量"):
        st.write(pd.DataFrame(X, columns=['feature1', 'feature2', 'feature3', 'feature4']))
    with st.expander("target"):
        st.write(y)

st.altair_chart(px.scatter(x="feature1", y="feature2", data=pd.DataFrame(X), color=y))

with st.expander("ダミーモデル"):
    st.pyplot(shap.summary_plot(shap_values.xFeatureImportance['weights'], X_train.columns, max_display=10))

# ダウンロードボタン
if st.button('ダウンロード'):
    df = pd.DataFrame(X, columns=['feature1', 'feature2', 'feature3', 'feature4'])
    df['target'] = y
    df.to_csv('data.csv', index=False)
    st.success('ダウンロード完了')

# SIDEBAR
st.sidebar.title("サイドバー")
options = ['Random Forest', 'SHAP']
selected_option = st.sidebar.selectbox("選択", options)

if selected_option == 'Random Forest':
    model_2 = RandomForestClassifier(n_estimators=100)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model_2.fit(X_train, y_train)
    shap_values_2 = shap.TreeExplainer(model_2).fit(X_train)

# SHAP 値を表示
if selected_option == 'Random Forest':
    st.pyplot(shap.summary_plot(shap_values_2.xFeatureImportance['weights'], X_train.columns, max_display=10))

st.write("サイドナビ")

with st.expander("SIDENAV"):
    st.write("SIDENAV")