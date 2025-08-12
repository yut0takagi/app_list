import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import LabelEncoder
from altair import chart, data, geom
import warnings
warnings.simplefilter("ignore")

# データの生成
np.random.seed(0)
data = {
    "category": np.repeat(["A", "B"], 10),
    "option": np.random.choice([1, 2], size=20)  
}
df = pd.DataFrame(data)

st.title("アンケート集計ダッシュボード")

# UI設定
tab1, tab2 = st.tabs(["アンケートデータ", "集計分析"])

with tab1:
    st.write("アンケートデータ")
    data_frame = df.copy()
    label_encoder = LabelEncoder()
    data_frame["category"] = label_encoder.fit_transform(data_frame["category"])
    # データの表示
    with st.expander("データ"):
        st.dataframe(data_frame)

with tab2:
    st.write("集計分析")
    df_count = df.groupby("category")["option"].count()
    fig = px.bar(df_count, x="category", y="option", title="アンケート結果")
    st.plotly_chart(fig)
    
    # オプションの集計結果の表示
    data_frame = df.groupby("category").mean()
    label_encoder = LabelEncoder()
    data_frame["option"] = label_encoder.fit_transform(data_frame["option"])
    col1, col2 = st.columns(2)
    with col1:
        if st.checkbox("オプション 1?", False):
            col1.write(data_frame["option"][0])
    with col2:
        if st.checkbox("オプション 2?", False):
            col2.write(data_frame["option"][1])
            
# ダウンロードボタン
if st.button("ダウンロード", key=1):
    df.to_csv("result.csv", index=False)

with st.expander("ヘルプ"):
    st.write(
        """
        このアプリでは、アンケートデータの集計や分析結果を表示するダッシュボードが用意されています。

        **タブ**:

        1. **アンケートデータ**: このタブを選択すると、アンケートデータが表示されます。
        
        2. **集計分析**: このタブを選択すると、アンケートデータの各カテゴリごとに結果の集計結果が表示されます。オプション1またはオプション2をクリックすることで、その結果を個別に表示することができます。

        *   オプション 1: category
        *   オプション 2: option

    """
    )