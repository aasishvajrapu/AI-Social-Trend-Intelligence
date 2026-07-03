import psycopg2
import pandas as pd


# ===================================
# DATABASE CONNECTION
# ===================================
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="trend_intelligence",
        user="postgres",
        password="enter your password here",
        port="5432"
    )


# ===================================
# LOAD VIDEOS
# ===================================
def load_videos():
    conn = get_connection()

    try:
        df = pd.read_sql(
            """
            SELECT *
            FROM youtube_trending
            ORDER BY fetched_at ASC
            """,
            conn
        )
    except Exception as e:
        print("load_videos error:", e)
        df = pd.DataFrame()

    conn.close()
    return df


def get_videos():
    return load_videos()


# ===================================
# LOAD COMMENTS
# ===================================
def load_comments():
    conn = get_connection()

    try:
        df = pd.read_sql(
            """
            SELECT *
            FROM youtube_comments
            """,
            conn
        )
    except Exception as e:
        print("load_comments error:", e)
        df = pd.DataFrame()

    conn.close()
    return df


def get_comments():
    return load_comments()


# ===================================
# SENTIMENT COUNTS
# ===================================
def load_sentiment_counts():
    conn = get_connection()

    try:
        df = pd.read_sql(
            """
            SELECT
                sentiment,
                COUNT(*) AS count
            FROM youtube_comments
            GROUP BY sentiment
            """,
            conn
        )
    except Exception as e:
        print("sentiment error:", e)
        df = pd.DataFrame()

    conn.close()
    return df


# ===================================
# LOAD HISTORY
# ===================================
def load_history():
    conn = get_connection()

    try:
        df = pd.read_sql(
            """
            SELECT *
            FROM video_history
            ORDER BY captured_at ASC
            """,
            conn
        )
    except Exception as e:
        print("history error:", e)
        df = pd.DataFrame()

    conn.close()
    return df


# ===================================
# TREND DATA
# ===================================
def get_trend_data():
    return load_history()


# ===================================
# TOP VIDEOS
# ===================================
def get_top_videos(limit=10):
    df = load_videos()

    if df.empty:
        return df

    return (
        df.sort_values(
            by="views",
            ascending=False
        )
        .head(limit)
    )


# ===================================
# TOP CHANNELS
# ===================================
def get_top_channels(limit=10):
    df = load_videos()

    if df.empty:
        return df

    if "channel_name" not in df.columns:
        return pd.DataFrame()

    return (
        df.groupby("channel_name")
        .agg(
            views=("views", "sum"),
            likes=("likes", "sum"),
            videos=("channel_name", "count")
        )
        .sort_values(
            by="views",
            ascending=False
        )
        .head(limit)
        .reset_index()
    )


# ===================================
# SEARCH VIDEO
# ===================================
def search_video(keyword):
    df = load_videos()

    if df.empty:
        return df

    if "title" not in df.columns:
        return pd.DataFrame()

    return df[
        df["title"]
        .str.contains(
            keyword,
            case=False,
            na=False
        )
    ]


# ===================================
# DASHBOARD METRICS
# ===================================
def get_dashboard_metrics():
    df = load_videos()

    if df.empty:
        return {
            "total_videos": 0,
            "total_views": 0,
            "total_likes": 0,
            "total_comments": 0
        }

    return {
        "total_videos": len(df),
        "total_views": int(df["views"].sum()),
        "total_likes": int(df["likes"].sum()),
        "total_comments": int(df["comments"].sum())
    }
