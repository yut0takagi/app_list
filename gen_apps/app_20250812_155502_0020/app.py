import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import altair as alt

# データ生成
np.random.seed(0)
X = np.random.rand(100, 10)  # feature
y = (np.random.randint(2, size=100) == 1).astype(int)  # label

# SHAP風に擬似するモデルの定義
class DummyModel:
    def fit(self, X, y):
        self.weights = np.random.rand(X.shape[1])

    def predict(self, X):
        return np.dot(X, self.weights)

# データの特徴量重要度をSHAP風に擬似するモデルの評価
st.title("SHAP風にPosliシーモデル")

with st.sidebar:
    st.markdown("---")
    st.write("Data")
    st.write(" feature - label")
    st.write(pd.DataFrame(X, columns=[f"feature_{i}" for i in range(10)]))
    st.write(y)

# SHAP風に擬似するモデルの評価
class DummyModelEvaluator:
    def __init__(self, model):
        self.model = model

    def evaluate(self, X_test, y_test):
        self.model.fit(X_test, y_test)
        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        confusion_matrix_value = confusion_matrix(y_test, predictions)

        return {
            "accuracy": accuracy,
            "confusion_matrix": confusion_matrix_value
        }

# データを擬似シーモデルで評価する
dummy_model = DummyModel()
dummy_model_evaluator = DummyModelEvaluator(dummy_model)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# SHAP風に擬似したデータの特徴量重要度を表示
fig = px.bar(x=dummy_model.weights.index, y=dummy_model.weights.values, text=[f"{i}: {j:.2f}" for i, j in zip(dummy_model.weights.index, dummy_model.weights.values)], title="特徴量重要度")
st.plotly_chart(fig)

# SHAP風に擬似したデータのConfusion Matrixを表示
conf_matrix_value = alt.Chart(dummy_model_evaluator.evaluate(X_train, y_train))
conf_matrix_value = conf_matrix_value.mark_bar()
conf_matrix_value = conf_matrix_value.encode(
    x=alt.X("Index:O"),
    y=alt.Y("Count:Q", stack=True)
)
st.write(conf_matrix_value)

# SHAP風に擬似したデータのAccuracyを表示
st.write(dummy_model_evaluator.evaluate(X_test, y_test)["accuracy"])

# SHAP風にPosliシーモデルをダウンロードするボタン
button = st.button("Download")

if button:
    df = pd.DataFrame({
        "feature": [f"feature_{i}" for i in range(10)],
        "weight": dummy_model.weights.values,
        "importance": dummy_model.weights.values / sum(dummy_model.weights.values)
    })
    
    st.download_button(label="Download", data=df.to_csv(index=False), file_name="posli_dummy_model.csv")

# SHAP風にPosliシーモデルをグラフ化する
fig = px.bar(x=dummy_model.weights.index, y=dummy_model.weights.values, text=[f"{i}: {j:.2f}" for i, j in zip(dummy_model.weights.index, dummy_model.weights.values)])
st.plotly_chart(fig)

# SHAP風にPosliシーモデルをConfusion Matrixで表示する
conf_mat = alt.Chart(df).mark_bar()
conf_mat = conf_mat.encode(
    x=alt.X("feature"),
    y=alt.Y("Count:Q", stack=True)
)
st.write(conf_mat)

# SHAP風にPosliシーモデルをAccuracyで表示する
st.write(dummy_model_evaluator.evaluate(X_test, y_test))

# SHAP風にPosliシーモデルをダウンロードする
if st.button("Download"):
    import pandas as pd
    
    df = pd.DataFrame({
        "feature": [f"feature_{i}" for i in range(10)],
        "weight": dummy_model.weights.values,
        "importance": dummy_model.weights.values / sum(dummy_model.weights.values)
    })
    
    st.download_button(label="Download", data=df.to_csv(index=False), file_name="posli_dummy_model.csv")

# SHAP風にPosliシーモデルをグラフ化する
fig = px.bar(x=dummy_model.weights.index, y=dummy_model.weights.values, text=[f"{i}: {j:.2f}" for i, j in zip(dummy_model.weights.index, dummy_model.weights.values)])
st.plotly_chart(fig)

# SHAP風にPosliシーモデルをConfusion Matrixで表示する
conf_mat = alt.Chart(df).mark_bar()
conf_mat = conf_mat.encode(
    x=alt.X("feature"),
    y=alt.Y("Count:Q", stack=True)
)
st.write(conf_mat)

# SHAP風にPosliシーモデルをAccuracyで表示する
st.write(dummy_model_evaluator.evaluate(X_test, y_test))

# SHAP_windにPosliシーモデルをダウンロードする
if st.button("Download"):
    import pandas as pd
    
    df = pd.DataFrame({
        "feature": [f"feature_{i}" for i in range(10)],
        "weight": dummy_model.weights.values,
        "importance": dummy_model.weights.values / sum(dummy_model.weights.values)
    })
    
    st.download_button(label="Download", data=df.to_csv(index=False), file_name="posli_dummy_model.csv")

# SHAP風にPosliシーモデルをグラフ化する
fig = px.bar(x=dummy_model.weights.index, y=dummy_model.weights.values, text=[f"{i}: {j:.2f}" for i, j in zip(dummy_model.weights.index, dummy_model.weights.values)])
st.plotly_chart(fig)

# SHAP風にPosliシーモデルをConfusion Matrixで表示する
conf_mat = alt.Chart(df).mark_bar()
conf_mat = conf_mat.encode(
    x=alt.X("feature"),
    y=alt.Y("Count:Q", stack=True)
)
st.write(conf_mat)

# SHAP風にPosliシーモデルをAccuracyで表示する
st.write(dummy_model_evaluator.evaluate(X_test, y_test))

# SHAP風にPosliシーモデルをグラフ化する
fig = px.bar(x=dummy_model.weights.index, y=dummy_model.weights.values, text=[f"{i}: {j:.2f}" for i, j in zip(dummy_model.weights.index, dummy_model.weights.values)])
st.plotly_chart(fig)

# SHAP風にPosliシーモデルをConfusion Matrixで表示する
conf_mat = alt.Chart(df).mark_bar()
conf_mat = conf_mat.encode(
    x=alt.X("feature"),
    y=alt.Y("Count:Q", stack=True)
)
st.write(conf_mat)

# SHAP風にPosliシーモデルをAccuracyで表示する
st.write(dummy_model_evaluator.evaluate(X_test, y_test))

# SHAP風にPosliシーモデルをダウンロードするボタン
if st.button("Download"):
    import pandas as pd
    
    df = pd.DataFrame({
        "feature": [f"feature_{i}" for i in range(10)],
        "weight": dummy_model.weights.values,
        "importance": dummy_model.weights.values / sum(dummy_model.weights.values)
    })
    
    st.download_button(label="Download", data=df.to_csv(index=False), file_name="posli_dummy_model.csv")

# SHAP風にPosliシーモデルをグラフ化する
fig = px.bar(x=dummy_model.weights.index, y=dummy_model.weights.values, text=[f"{i}: {j:.2f}" for i, j in zip(dummy_model.weights.index, dummy_model.weights.values)])
st.plotly_chart(fig)

# SHAP風にPosliシーモデルをConfusion Matrixで表示する
conf_mat = alt.Chart(df).mark_bar()
conf_mat = conf_mat.encode(
    x=alt.X("feature"),
    y=alt.Y("Count:Q", stack=True)
)
st.write(conf_mat)

# SHAP_windにPosliシーモデルをAccuracyで表示する
st.write(dummy_model_evaluator.evaluate(X_test, y_test))

# SHAP風にPosliシーモデルをダウンロードします。
if st.button("Download"):
    import pandas as pd
    
    df = pd.DataFrame({
        "feature": [f"feature_{i}" for i in range(10)],
        "weight": dummy_model.weights.values,
        "importance": dummy_model.weights.values / sum(dummy_model.weights.values)
    })
    
    st.download_button(label="Download", data=df.to_csv(index=False), file_name="posli_dummy_model.csv")