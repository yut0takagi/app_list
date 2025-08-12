import streamlit as st
import pandas as pd
import numpy as np
import random

# データ生成
data = {
    '文章': [
        'テキストを要約するツールは、特定のキーワードとテキストの相関性に基づいてランダムな要約を生成します。',
        'このツールでは、ユーザーが入力したキーワードや文章を使用して、ランダムな要約を生成できます。'
    ]
}
df = pd.DataFrame(data)

# サイド バー
st.sidebar.header('サイド バー')
with st.sidebar:
    selected_text = st.text_input('入力したテキスト', value='', placeholder='テキストを入力してください')
    keyword = st.text_input('入力するキーワード', value='ランダム', placeholder='キーワードを入力してください')

# メイン コンテンツ
st.title('テキスト要約ツール')
st.write(df)

if selected_text != '':
    # wantage生成
    def generate_wantage(text):
        words = text.split()
        keywords = list(set(words) - set(['と','は','、','。','？','!']))
        return [word for word in keywords if keyword.lower() in word.lower()]

    wantage = '\n'.join(generate_wantage(selected_text))

    # 要約生成
    def generate_summary(text, wantage):
        words = text.split()
        summary = ' '.join([words[0], wantage])
        return summary

    summary = generate_summary(selected_text, wantage)
    st.write('要約:')
    st.write(summary)

# ダウンロード ボタン
st.sidebar.header('ダウンロード')
if selected_text != '':
    download_file = 'want_age.txt'
    with open(download_file, 'w') as file:
        file.write(wantage)
    downloaded_file = st.download_button(label='ダウンロード', data=download_file.replace('\n', '\r\n'), file_name=download_file)

# キーワード抽出
if keyword != '':
    def extract_keyword(text):
        words = text.split()
        return list(set(words) - set(['と','は','、','。','？','!']))

    extracted_keyword = extract_keyword(selected_text)
    st.write('キーワード抽出:')
    st.write(extracted_keyword)

# テキスト生成
def generate_text():
    text = ''
    for _ in range(50):
        sentence = random.choice(['このツールは', 'テキストを要約するツールは','ユーザーが入力したキーワードや文章を使用してランダムな要約を生成できます。'])
        text += sentence + '\n'
    return text

# テキスト表示
text = generate_text()
st.write('テキスト:')
st.markdown(text, unsafe_allow_html=True)

if __name__ == '__main__':
    pass