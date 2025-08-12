import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import altair as alt
from datetime import datetime, timedelta

# データのための擬似生成
np.random.seed(0)
tasks = ['TODO ' + str(i) for i in range(1, 21)]  # TODOSタスク
times = pd.date_range(start='2023-01-01', periods=20, freq='D')  # ポモドーロタイマー用
percent = np.random.uniform(0, 100, 20).astype(np.int)  # 追加したい割合です。max は 99 です。

# スタートページ
st.title('ToDo+ポモドーロタイマー+進捗ガント風チャート')

tab = st.tabs(['TODO', 'トレーナー', '分析'])

# TODO タブ
with tab[0]:
    st.subheader('Todo List')
    df = pd.DataFrame(tasks, columns=['Task'])
    
    with_st = st.button('With Pomodoro Timer')
    if not with_st:
        st.write('Not started')
        started_time = None
    else:
        st.write('Started')
        started_time = datetime.now()
        
    update_timer = st.slider('Update interval (s)', 1, 60)
    
    def check_status(status):
        now = datetime.now()
        if status == 'started':
            duration = now - started_time
            minutes, seconds = divmod(duration.total_seconds(), 60)
            hours, mins = divmod(minutes, 60)
            duration_str = f'{int(hours):02d}:{int(mins):02d}:{int(seconds):02d}'
        elif status == 'finished':
            duration = now - started_time
            minutes, seconds = divmod(duration.total_seconds(), 60)
            hours, mins = divmod(minutes, 60)
            duration_str = f'{int(hours):02d}:{int(mins):02d}:{int(seconds):02d}'
        return duration_str
    
    if st.button('Show progress'):
        status = check_status(started_time) if started_time else 'Started'
        st.write(status)

# トレーナー タブ
with tab[1]:
    st.subheader('Training Data')
    data = pd.DataFrame([[i, np.random.rand(), np.random.rand() * 0.001] for i in range(20)], columns=['ID', 'X', 'V'])
    
    if st.button('Split'):
        X_train, X_test, y_train, y_test = train_test_split(data['X'], data['V'], test_size=0.2)
        
def plot_results():
    fig = alt.Chart(X_train).mark_point().encode(
        x='ID',
        y='V'
    ).title('Training Data')
    
    st.altair_chart(fig)

if st.button('Show plot'):
    plot_results()

# analysis タブ
with tab[2]:
    st.subheader('Analysis')
    data = pd.DataFrame([[i, np.random.rand(), np.random.rand() * 0.001] for i in range(20)], columns=['ID', 'X', 'V'])
    
    def plot_results():
        fig = alt.Chart(data).mark_line().encode(
            x='ID',
            y='V'
        ).title('Analysis')
        
        st.altair_chart(fig)

    if st.button('Show plot'):
        plot_results()

# sidebar
with st.sidebar:
    st.write('')
    
st.download_button(
    label="Download as CSV",
    data=dict(Task=tasks),
    file_name="tasks.csv",
    click_callback=lambda: None,
)

if st.button('Refresh'):
    tasks = ['TODO ' + str(i) for i in range(1, 21)]  # TODOSタスク
    times = pd.date_range(start='2023-01-01', periods=20, freq='D')  # ポモドーロタイマー用
    percent = np.random.uniform(0, 100, 20).astype(np.int)  # 追加したい割合です。max は 99 です.