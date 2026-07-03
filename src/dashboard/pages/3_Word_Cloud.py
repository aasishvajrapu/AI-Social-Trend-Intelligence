import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
from collections import Counter
from nltk.corpus import stopwords
import re

from components.database import load_comments
from components.styles import load_css

st.set_page_config(
    page_title="Word Cloud",
    layout="wide"
)

load_css()

comments = load_comments()

st.title("Word Cloud")

st.markdown("""
<div style="
padding:20px;
border-radius:20px;
background:rgba(15,23,42,0.45);
backdrop-filter:blur(20px);
margin-bottom:25px;
border:1px solid rgba(255,255,255,0.08);
">
<h4 style="color:#94A3B8;">
Trending Topics and Audience Keywords
</h4>
</div>
""",
unsafe_allow_html=True)

# ====================================
# STOPWORDS
# ====================================

sw = set(STOPWORDS)
sw.update(stopwords.words("english"))

custom_stopwords = {
    "video","youtube","channel","please","bro","guys",
    "like","subscribe","hai","hain","bhai","bhaiya",
    "ka","ki","ke","ko","se","mein","mai","mera",
    "meri","mere","ho","ha","tha","nahi","kya",
    "xxx","next","will","movie","song","sir",
    "one","love","good","super","nice","thank",
    "thanks","new","top","last","back","play",
    "friend","actually","give","hu","raha","karo",
    "aap","fir","dekh","liye","bahut","bada",
    "sath","kuch","man","ji","v","w","na",
    "hi","ge","lol","omg","wow","ok","okay",
    "hey","really","make","made","also","see",
    "watch","watched","look","looks","today",
    "tomorrow","yes","no","wali","wala","wale",
    "tumhara","tumhari","tumhare","he","bhut",
    "kiva","apne","bolate","kuchh","face","reveal"
}

sw.update(custom_stopwords)

# ====================================
# CLEAN COMMENTS
# ====================================

comments["comment"] = (
    comments["comment"]
    .fillna("")
    .astype(str)
)

comments["clean_comment"] = (
    comments["comment"]
    .str.lower()
)

comments["clean_comment"] = comments[
    "clean_comment"
].apply(
    lambda x: re.sub(
        r"http\S+|www\S+",
        "",
        x
    )
)

comments["clean_comment"] = comments[
    "clean_comment"
].apply(
    lambda x: re.sub(
        r"[^a-zA-Z\s]",
        " ",
        x
    )
)

comments["clean_comment"] = comments[
    "clean_comment"
].apply(
    lambda x: re.sub(
        r"\s+",
        " ",
        x
    ).strip()
)

# ====================================
# MAIN WORD CLOUD
# ====================================

text = " ".join(
    comments["clean_comment"]
)

words = [
    word
    for word in text.split()
    if (
        word not in sw
        and len(word) > 4
    )
]

clean_text = " ".join(words)

wordcloud = WordCloud(
    width=1800,
    height=700,
    background_color="#020617",
    stopwords=sw,
    colormap="plasma",
    max_words=150
).generate(clean_text)

st.subheader("Trending Word Cloud")

fig, ax = plt.subplots(
    figsize=(18, 8)
)

ax.imshow(
    wordcloud,
    interpolation="bilinear"
)

ax.axis("off")

st.pyplot(fig)

st.divider()

# ====================================
# POSITIVE & NEGATIVE WORD CLOUDS
# ====================================

c1, c2 = st.columns(2)

with c1:

    st.subheader("Most Loved Topics")

    positive = comments[
        comments["sentiment"] == "Positive"
    ]

    pos_text = " ".join(
        positive["clean_comment"]
    )

    pos_words = [
        word
        for word in pos_text.split()
        if (
            word not in sw
            and len(word) > 4
        )
    ]

    if len(pos_words):

        pos_wc = WordCloud(
            width=800,
            height=400,
            background_color="#020617",
            colormap="summer"
        ).generate(
            " ".join(pos_words)
        )

        fig1, ax1 = plt.subplots(
            figsize=(8, 4)
        )

        ax1.imshow(pos_wc)

        ax1.axis("off")

        st.pyplot(fig1)

with c2:

    st.subheader("Most Criticized Topics")

    negative = comments[
        comments["sentiment"] == "Negative"
    ]

    neg_text = " ".join(
        negative["clean_comment"]
    )

    neg_words = [
        word
        for word in neg_text.split()
        if (
            word not in sw
            and len(word) > 4
        )
    ]

    if len(neg_words):

        neg_wc = WordCloud(
            width=800,
            height=400,
            background_color="#020617",
            colormap="autumn"
        ).generate(
            " ".join(neg_words)
        )

        fig2, ax2 = plt.subplots(
            figsize=(8, 4)
        )

        ax2.imshow(neg_wc)

        ax2.axis("off")

        st.pyplot(fig2)

st.divider()

# ====================================
# TOP KEYWORDS
# ====================================

counter = Counter(words)

top_words = pd.DataFrame(
    counter.most_common(20),
    columns=[
        "Word",
        "Count"
    ]
)

c1, c2 = st.columns(2)

with c1:

    st.subheader("Top Keywords")

    st.dataframe(
        top_words,
        use_container_width=True,
        height=450
    )

with c2:

    st.subheader("Keyword Search")

    keyword = st.text_input(
        "Search Keyword"
    )

    if keyword:

        occurrences = len(
            re.findall(
                rf"\b{keyword.lower()}\b",
                clean_text
            )
        )

        st.metric(
            "Occurrences",
            occurrences
        )

st.divider()

# ====================================
# BAR CHART
# ====================================

st.subheader("Top 15 Keywords")

fig3 = px.bar(
    top_words.head(15),
    x="Count",
    y="Word",
    orientation="h",
    color="Count",
    color_continuous_scale="Plasma"
)

fig3.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="white",
    height=650,
    yaxis=dict(
        categoryorder="total ascending"
    )
)

fig3.update_coloraxes(
    showscale=False
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.divider()

# ====================================
# DOWNLOADABLE TABLE
# ====================================

st.subheader("Keyword Frequency Analysis")

top50 = pd.DataFrame(
    counter.most_common(50),
    columns=[
        "Word",
        "Count"
    ]
)

st.dataframe(
    top50,
    use_container_width=True,
    height=500
)

csv = top50.to_csv(
    index=False
)

st.download_button(
    "Download Keywords CSV",
    csv,
    "keywords.csv",
    "text/csv"
)