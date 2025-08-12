import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords, wordnet
import random
import re

# データ生成
stop_words = set(stopwords.words("Japanese"))

def make_dataset(size):
    data = {
        "text": [random.choice(["この本は", "その本は", "この文は"], np.random.choice(3)) for _ in range(size)],
        "abstract": ["要約" for _ in range(size)]
    }
    df = pd.DataFrame(data).sample(frac=1)
    return df

# データ生成して用于
size = 100
df = make_dataset(size)

# UI設定
st.title("Text Summarization Tool")

# バリアンビリタル
if st.mode choice(["light", "dark"]):
    theme = "dark"
else:
    theme = "light"

st.write(
    """
    このアプリは、文章をランダムな要約して出力します。
    また、キーワードの抽出が可能です。
    """,
    f"**{theme}モード**"
)

# ユーザーインプット
user_input = st.text_area("文章", height=1000)
if user_input:
    # 分割
    doc_sentences = [sentiment.strip() for sentiment in user_input.split(".")]
    
    # Tfidfベクトル作成
    vectorizer = TfidfVectorizer(stop_words=stop_words)
    tfidf = vectorizer.fit_transform(doc_sentences)

    # スタンドアロン抽出
    abstract = []
    title = ""
    summary = ""

    # スタンドアロン解析
    for row in tfidf.toarray():
        _vector = np.array([row[0], row[1]])  
        candidate_word = [
            "この文章は",
            "{}は.",
            "{}という本は。",
            "{}の文章は"
        ]
        candidates = [wordnet.synsets("_vector")[0].lemmas()[0].name() for _ in range(4)]
        abstract_candidate = random.choice(candidate_word) + str(candidates[0])        
        abstract_candidate += "."
        if candidate_word == ["この文章は", "この本は"]:
            abstract_candidate = random.choice(["その文章は", "その本は"])
        elif candidate_word[index] in abstract:
            continue
        abstract.append(abstract_candidate)
    
    # スタンドアロン抽出
    title = random.choice(abstract)

    _summary = "".join(doc_sentences[0].split("."))
            
    # ダウンロードボタン
    download_button = st.download_button(
        label="要約",
        data={"text": f"{title}： 《{abstract}\n》. \"{_summary}\"."},
        file_name=f"sum_text_{random.randint(100, 999)}.txt",
        mime="plain/txt",
    )

# サイドバー
if st.sidebar:
    
    # tabcontrol
    if st.sidebar.checkbox("キーワード抽出"):
        st.write(
            """
            ここから、抽出されたキーワードを確認できます。
            """,
            "#キーワード",
            "   ",
            "   *".join(random.sample([wordnet.synsets("_vector")[0].lemmas()[0].name() for _ in range(10)], 10))
    else:
        st.write("")

# Altair
altair_chart = alt.Chart(df).mark_bar().encode(
    x='text:N',
    y='abstract:Q'
)
st.altair_chart(altair_chart)