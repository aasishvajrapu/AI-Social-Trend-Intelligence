import streamlit as st
import pandas as pd
import plotly.express as px

from components.database import load_comments, load_videos
from components.styles import load_css

st.set_page_config(
    page_title="Sentiment Analysis",
    layout="wide"
)

load_css()

comments = load_comments()
videos = load_videos()

st.title("Sentiment Analysis")

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
Audience Sentiment and Comment Intelligence
</h4>
</div>
""",
unsafe_allow_html=True)

# ---------------- KPIs ----------------

positive = len(
    comments[
        comments["sentiment"] == "Positive"
    ]
)

neutral = len(
    comments[
        comments["sentiment"] == "Neutral"
    ]
)

negative = len(
    comments[
        comments["sentiment"] == "Negative"
    ]
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Comments",
    len(comments)
)

c2.metric(
    "Positive",
    positive
)

c3.metric(
    "Neutral",
    neutral
)

c4.metric(
    "Negative",
    negative
)

st.divider()

# ---------------- DONUT ----------------

left, right = st.columns(2)

with left:

    st.subheader("Sentiment Distribution")

    sentiment_df = (
        comments["sentiment"]
        .value_counts()
        .reset_index()
    )

    sentiment_df.columns = [
        "sentiment",
        "count"
    ]

    fig1 = px.pie(
        sentiment_df,
        values="count",
        names="sentiment",
        hole=0.6,
        color="sentiment",
        color_discrete_map={
            "Positive": "#10B981",
            "Neutral": "#F59E0B",
            "Negative": "#EF4444"
        }
    )

    fig1.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

with right:

    st.subheader("Sentiment Counts")

    fig2 = px.bar(
        sentiment_df,
        x="sentiment",
        y="count",
        color="sentiment",
        color_discrete_map={
            "Positive": "#10B981",
            "Neutral": "#F59E0B",
            "Negative": "#EF4444"
        }
    )

    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

st.divider()

# ---------------- VIDEO SENTIMENT ----------------

st.subheader("Sentiment by Video")

video_sentiment = (
    comments.groupby(
        ["video_id", "sentiment"]
    )
    .size()
    .reset_index(
        name="count"
    )
)

video_sentiment = pd.merge(
    video_sentiment,
    videos[
        ["video_id", "title"]
    ],
    on="video_id",
    how="left"
)

video_sentiment["short_title"] = (
    video_sentiment["title"]
    .fillna("Unknown")
    .apply(
        lambda x:
        x[:35] + "..."
        if len(x) > 35
        else x
    )
)

fig3 = px.bar(
    video_sentiment,
    x="short_title",
    y="count",
    color="sentiment",
    barmode="group",
    color_discrete_map={
        "Positive": "#10B981",
        "Neutral": "#F59E0B",
        "Negative": "#EF4444"
    }
)

fig3.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="white",
    xaxis_title=None
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.divider()

# ---------------- MOST POSITIVE ----------------

left, right = st.columns(2)

with left:

    st.subheader("Most Positive Videos")

    positive_videos = (
        comments[
            comments["sentiment"]
            == "Positive"
        ]
        .groupby("video_id")
        .size()
        .reset_index(
            name="positive_comments"
        )
        .sort_values(
            "positive_comments",
            ascending=False
        )
        .head(10)
    )

    positive_videos = pd.merge(
        positive_videos,
        videos[
            ["video_id", "title"]
        ],
        on="video_id",
        how="left"
    )

    st.dataframe(
        positive_videos[
            [
                "title",
                "positive_comments"
            ]
        ],
        use_container_width=True
    )

with right:

    st.subheader("Most Negative Videos")

    negative_videos = (
        comments[
            comments["sentiment"]
            == "Negative"
        ]
        .groupby("video_id")
        .size()
        .reset_index(
            name="negative_comments"
        )
        .sort_values(
            "negative_comments",
            ascending=False
        )
        .head(10)
    )

    negative_videos = pd.merge(
        negative_videos,
        videos[
            ["video_id", "title"]
        ],
        on="video_id",
        how="left"
    )

    st.dataframe(
        negative_videos[
            [
                "title",
                "negative_comments"
            ]
        ],
        use_container_width=True
    )

st.divider()

# ---------------- SEARCH ----------------

st.subheader("Comment Explorer")

search = st.text_input(
    "Search Comments"
)

display_comments = comments.copy()

if search:

    display_comments = display_comments[
        display_comments["comment_text"]
        .str.contains(
            search,
            case=False,
            na=False
        )
    ]

st.dataframe(
    display_comments,
    use_container_width=True,
    height=500
)

# ---------------- DOWNLOAD ----------------

csv = display_comments.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "Download Comments CSV",
    csv,
    "youtube_comments.csv",
    "text/csv"
)