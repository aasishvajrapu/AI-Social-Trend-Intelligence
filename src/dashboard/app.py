import streamlit as st
from streamlit_autorefresh import st_autorefresh

from components.database import *
from components.styles import load_css
from components.charts import *

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Social Trend Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- LOAD CSS ----------------

load_css()

# ---------------- AUTO REFRESH ----------------

st_autorefresh(
    interval=60000,
    key="dashboard_refresh"
)

# ---------------- LOAD DATA ----------------

videos = load_videos()
comments = load_comments()
sentiment = load_sentiment_counts()

# ---------------- HEADER ----------------

st.title("AI Social Trend Intelligence")

st.markdown("""
<div style="
padding:20px;
border-radius:20px;
background:rgba(15,23,42,0.45);
backdrop-filter:blur(20px);
margin-bottom:25px;
border:1px solid rgba(255,255,255,0.08);
">
<h4 style="
color:#94A3B8;
margin-bottom:0;
">
Real-Time Trend Analytics and Audience Intelligence Platform
</h4>
</div>
""",
unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

st.sidebar.header("Filters")

# Channel filter
channel = st.sidebar.selectbox(
    "Channel",
    ["All"] +
    sorted(
        videos["channel_name"].unique()
    )
)

if channel != "All":
    videos = videos[
        videos["channel_name"] == channel
    ]

# Views slider
min_views, max_views = st.sidebar.slider(
    "Views",
    int(videos["views"].min()),
    int(videos["views"].max()),
    (
        int(videos["views"].min()),
        int(videos["views"].max())
    )
)

videos = videos[
    (videos["views"] >= min_views)
    &
    (videos["views"] <= max_views)
]

# Search
search = st.sidebar.text_input(
    "Search Video"
)

if search:
    videos = videos[
        videos["title"]
        .str.contains(
            search,
            case=False,
            na=False
        )
    ]

# ---------------- METRICS ----------------

total_videos = len(videos)
total_comments = len(comments)

positive = len(
    comments[
        comments["sentiment"] == "Positive"
    ]
)

positivity = round(
    (positive / len(comments)) * 100,
    2
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Trending Videos",
        total_videos
    )

with col2:
    st.metric(
        "Comments Analysed",
        total_comments
    )

with col3:
    st.metric(
        "Positivity %",
        f"{positivity}%"
    )

st.divider()

# ---------------- CHARTS ----------------

left, right = st.columns(2)

with left:

    st.subheader("Top Videos")

    top = videos.nlargest(
        10,
        "views"
    ).copy()

    top["short_title"] = top[
        "title"
    ].apply(
        lambda x:
        x[:35] + "..."
        if len(x) > 35
        else x
    )

    st.plotly_chart(
        views_bar(top),
        use_container_width=True
    )

with right:

    st.subheader(
        "Sentiment Distribution"
    )

    st.plotly_chart(
        sentiment_pie(sentiment),
        use_container_width=True
    )

st.divider()

# ---------------- QUICK STATS ----------------

c1, c2 = st.columns(2)

with c1:

    st.subheader("Top Channels")

    top_channels = (
        videos.groupby(
            "channel_name"
        )["views"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        top_channels,
        use_container_width=True,
        height=400
    )

with c2:

    st.subheader("Most Discussed Videos")

    discussed = (
        comments.groupby(
            "video_id"
        )
        .size()
        .reset_index(
            name="comment_count"
        )
        .sort_values(
            "comment_count",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        discussed,
        use_container_width=True,
        height=400
    )

st.divider()

# ---------------- FULL DATASET ----------------

st.subheader("Trending Dataset")

display_df = videos[
    [
        "title",
        "channel_name",
        "views",
        "likes",
        "comments"
    ]
].sort_values(
    "views",
    ascending=False
)

st.dataframe(
    display_df,
    use_container_width=True,
    height=500
)