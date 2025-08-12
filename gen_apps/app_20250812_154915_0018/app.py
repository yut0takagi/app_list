import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import shap
import seaborn as sns
import altair as alt
import matplotlib.pyplot as plt

# データ生成
np.random.seed(0)
X = pd.DataFrame(np.random.rand(100, 5))
y = np.random.randint(2, size=100)

# SHAP値を計算するRandomForestクラスを作成
class SHAPS:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=10, random_state=0)
    
    def train(self, X, y):
        self.model.fit(X, y)
        return self
    
    def explain(self, X):
        explainer = shap.Explainer(target=self.model.predict_proba)
        return explainer(X)

# アプリの設定
st.title('SHAP値の擬似表示')

# サイドバーとタブ
with st.sidebar:
    st.header('選択')
    feature_names = list(X.columns)
    all_features = ['feature_{}'.format(i) for i in range(5)]
    selected_features = st.multiselect('選択', all_features, default=feature_names)

# データ表示
X_selected = X.loc[:, [f for f in feature_names if f in selected_features]]
st.write(f'選択特徴数: {len(selected_features)}')
st.write(X_selected.head())

# SHAP値の計算と表示
shap_values = SHAPS().train(X_selected, y).explain(X_selected)
fig = alt.Chart(shap_values.shap_values).mark_bar(stroke='red').encode(
    x='feature',
    value='value'
).properties(title_text='特徴量のSHAP値')
st.altair_chart(fig)

# ダウンロードボタン
def shap_value_file(shap_values):
    df = pd.DataFrame(shap_values.shap_values, columns=['value'])
    html = df.to_html(index=False)
    return html

shap_df = shap_value_file(shap_values).replace('<table>', '<div style="border: 1px solid black; padding: 10px;">')
st.markdown('''
[ダウンローします](https://github.com/your_username/streamlit-app/blob/master/output.html)
''')

# SHAP値の視覚化
fig = px.bar(shap_values.shap_values, x='feature', y='value')
st.plotly_chart(fig)

# データ分析
sns.set()
plt = sns.heatmap(X_selected.corr(), annot=True)
st.pyplot(plt)

# パラメータの Fine-Tuning
with st.expander("パラメータ"):
    a = st.number_input('a', value=1, min_value=0)
    b = st.number_input('b', value=2, min_value=0)
    c = st.number_input('c', value=3, min_value=0)

# SHAP値の可視化
shap_map = shap_values.shap_values.mean(axis=1).plot(kind='bar')
st.pyplot(shap_map)