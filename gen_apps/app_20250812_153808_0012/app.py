import streamlit as st
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from altair import chart, config
config.default_params['axis']['title'] = True

# データ生成
np.random.seed(0)
data = {
    '年齢': np.random.randint(20, 60, 100),
    '性別': np.random.choice(['男', '女'], 100),
    '月収': np.random.randint(200000, 600000, 100),
    '雇用歴': np.random.randint(5, 30, 100)
}
df = pd.DataFrame(data)

# セットアップ
st.title('アンケート集計ダッシュボード')
col1, col2 = st.sidebar.columns([1, 1])
with col1:
    st.write('年齢と性別のカラムを選択できます')
    age_col = st.selectbox('年齢カラム', ['年齢'])
if age_col:
    df[age_col] = pd.Categorical(df[age_col], categories=df['年齢'].unique())
with col2:
    st.write('月収と雇用歴のカラムを選択できます')
    income_col = st.selectbox('月収カラム', ['月収'])
    job_history_col = st.selectbox('雇用歴カラム', ['雇用歴'])

# カラムの選択に応してデータを集計
if age_col:
    age_df = df.groupby(age_col)[['性別', '月収', '雇用歴']].mean()
st.write('### {0} : '.format(age_col))
age_df = pd.DataFrame([age_df])
chart(altair chart(age_df, x=age_df.columns[0], y=[x for x in age_df.columns[1:] if x not in ['性別']], height=300))

# 使いたいカラムを選択し、グラフを見せます
col3, col4 = st.columns([1, 2])
with col3:
    st.write('使いたい列を選択')
if age_col and income_col:
    select_columns = st.multiselect('選択', df.columns)
elif age_col:
    select_columns = [age_col]
else:
    select_columns = []
df_selected = df[select_columns]

# グラフの設定
fig = chart(altair chart(df_selected, x='年齢', y=['月収', '雇用歴'], height=300))
st.pyplot(fig)

# ダウンロード
with st.download_button(
    label="ダウンロード",
    data=df.to_csv(index=False),
    file_name="アンケート集計データ.csv"
):
    pass

# 表示するデータの選択肢
col5, col6 = st.columns([1, 1])
with col5:
    st.write('表示するデータの選択')
if '年齢' in select_columns or '性別' in select_columns:
    df_selected_age = df_selected[['年齢', '性別']]
elif '月収' in select_columns or '雇用歴' in select_columns:
    df_selected_income = df_selected[['月収', '雇用歴']]
# データ表示の確認
col7, col8 = st.columns([1, 2])
with col7:
    if df_selected_age.shape[0] == 0 or df_selected_income.shape[0] == 0:
        st.write('選択したデータが存在しません')
    else:
        st.write(df_selected_age)
        st.write(df_selected_income)

# グラフの表示
if '業種' in select_columns and df_selected_income.shape[0] > 0:
    fig = chart(altair chart(df_selected_income, x='月収', y=['雇用歴'], height=300))
    st.pyplot(fig)