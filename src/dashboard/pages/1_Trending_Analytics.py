import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from components.database import load_videos
from components.styles import load_css

st.set_page_config(
    page_title="Trending Analytics",
    layout="wide"
)

load_css()

videos = load_videos()

st.title("Trending Analytics")

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
Video Performance and Engagement Analytics
</h4>
</div>
""",
unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

st.sidebar.header("Analytics Filters")

channel = st.sidebar.selectbox(
    "Channel",
    ["All"] +
    sorted(videos["channel_name"].unique())
)

if channel != "All":
    videos = videos[
        videos["channel_name"] == channel
    ]

# ---------------- EXTRA METRIC ----------------

videos["engagement_score"] = (
    videos["likes"] +
    videos["comments"]
) / videos["views"] * 100

# ---------------- KPI CARDS ----------------

total_views = int(videos["views"].sum())
total_likes = int(videos["likes"].sum())
avg_views = int(videos["views"].mean())
avg_engagement = round(
    videos["engagement_score"].mean(),
    2
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Views",
    f"{total_views:,}"
)

c2.metric(
    "Total Likes",
    f"{total_likes:,}"
)

c3.metric(
    "Average Views",
    f"{avg_views:,}"
)

c4.metric(
    "Engagement %",
    f"{avg_engagement}%"
)

st.divider()

# ---------------- TOP CHANNELS ----------------

st.subheader("Top Channels by Views")

top_channels = (
    videos.groupby(
        "channel_name"
    )["views"]
    .sum()
    .reset_index()
    .sort_values(
        "views",
        ascending=False
    )
    .head(10)
)

fig1 = px.bar(
    top_channels,
    x="views",
    y="channel_name",
    orientation="h",
    color="views",
    color_continuous_scale="Blues"
)

fig1.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="white",
    height=500
)

fig1.update_yaxes(title=None)
fig1.update_xaxes(title=None)
fig1.update_coloraxes(showscale=False)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.divider()

# ---------------- HISTOGRAMS ----------------

left, right = st.columns(2)

with left:

    st.subheader("Views Distribution")

    fig2 = px.histogram(
        videos,
        x="views",
        nbins=15,
        color_discrete_sequence=["#3B82F6"]
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

with right:

    st.subheader("Likes Distribution")

    fig3 = px.histogram(
        videos,
        x="likes",
        nbins=15,
        color_discrete_sequence=["#8B5CF6"]
    )

    fig3.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

st.divider()

# ---------------- SCATTER ----------------

st.subheader("Views vs Likes")

fig4 = px.scatter(
    videos,
    x="views",
    y="likes",
    size="comments",
    color="engagement_score",
    hover_data=[
        "title",
        "channel_name"
    ],
    color_continuous_scale="Turbo"
)

fig4.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="white",
    height=600
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

st.divider()

# ---------------- CORRELATION ----------------

st.subheader("Correlation Heatmap")

corr = videos[
    [
        "views",
        "likes",
        "comments",
        "engagement_score"
    ]
].corr()

fig5 = go.Figure(
    data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        colorscale="Blues",
        text=corr.round(2).values,
        texttemplate="%{text}"
    )
)

fig5.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="white",
    height=500
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

st.divider()

# ---------------- TOP VIDEOS ----------------

st.subheader("Top 10 Videos")

top_videos = videos.nlargest(
    10,
    "views"
)[
    [
        "title",
        "channel_name",
        "views",
        "likes",
        "comments"
    ]
]

st.dataframe(
    top_videos,
    use_container_width=True
)

st.divider()

# ---------------- FULL DATA ----------------

st.subheader("Trending Dataset")

st.dataframe(
    videos[
        [
            "title",
            "channel_name",
            "views",
            "likes",
            "comments",
            "engagement_score"
        ]
    ],
    use_container_width=True,
    height=500
)

# ---------------- DOWNLOAD ----------------

csv = videos.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "Download CSV",
    csv,
    "youtube_trending.csv",
    "text/csv"
)