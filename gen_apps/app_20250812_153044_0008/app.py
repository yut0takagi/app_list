```python
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import SHAP
import plotly.express as px
import altair as alt

# データ生成
np.random.seed(0)
X = np.random.rand(100, 10)  # feature
y = (X[:, 8] > 0.5).astype(int)  # label

# Dataframeを作成
df = pd.DataFrame(X, columns=[f'特徴{i+1}' for i in range(10)])
df['ラベル'] = y

# SIDEBAR
with st.sidebar:
    st.title('学習データの特徴量重要度をSHAP風に擬似表示')
    
    # さて、次のセクションから始めましょう。
    if st.button('Next'):
        with st.expander('特徴量選択'):
            col1, col2 = st.columns(2)
            
            with col1:
                choice = st.selectbox('選択', range(1, 11))
                
            with col2:
                data = df.iloc[:, :choice]
                
    # Feature selection
    if st.button('Feature selection'):
        if choice == 1:
            data = df['特徴1']
        elif choice == 2:
            data = df['特徴2']
        else:
            data = df.sample(10, random_state=0)
            
        with st.expander('Plot'):
            fig = px.scatter(data, x='特徴0', y='特徴1')
            st.plotly_graph(fig)

    if st.button('SHAP value'):
        with st.expander('SHAP value'):
            # SHAP 値の表示
            model = RandomForestClassifier()
            X_train, X_test, y_train, y_test = train_test_split(data, df['ラベル'], test_size=0.3, random_state=42)
            
            scaler = StandardScaler()
            data_train_scaled = scaler.fit_transform(X_train)
            model.fit(scaler.transform(X_test), y_test)
            
            X_test_pred = scaler.transform(X_test)
            shap_values = SHAP(model, X_test_pred)
            
            # Feature importances
            feature_importances = pd.Series(model.feature_importances_, index=data.columns).sort_values(ascending=False)
            st.write(f'Feature importances:\n{feature_importances}')
            
            fig = px.bar(shap_values[0], x=data.columns, y='shap_value')
            st.plotly_graph(fig)

# ダウンロードボタン
if st.button('Download'):
    data.to_csv('sample.csv', index=False)

# Sidebar bottom
st.write('Copyright 2023')