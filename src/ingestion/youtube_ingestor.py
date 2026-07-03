import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
import psycopg2
from datetime import datetime

# Load .env file
load_dotenv()

# Check if API key is being loaded
print("API KEY:", os.getenv("YOUTUBE_API_KEY"))

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="trend_intelligence",
    user="postgres",
    password="Aasish@29",
    port="5432"
)

cursor = conn.cursor()

# Connect to YouTube API
youtube = build(
    "youtube",
    "v3",
    developerKey=YOUTUBE_API_KEY
)

# Get trending videos
request = youtube.videos().list(
    part="snippet,statistics",
    chart="mostPopular",
    regionCode="IN",
    maxResults=25
)

response = request.execute()

print("Number of videos fetched:", len(response["items"]))

# Insert data into PostgreSQL
for video in response["items"]:

    video_id = video["id"]
    title = video["snippet"]["title"]
    channel_name = video["snippet"]["channelTitle"]

    published_at = datetime.strptime(
        video["snippet"]["publishedAt"],
        "%Y-%m-%dT%H:%M:%SZ"
    )

    views = int(video["statistics"].get("viewCount", 0))
    likes = int(video["statistics"].get("likeCount", 0))
    comments = int(video["statistics"].get("commentCount", 0))

    cursor.execute(
        """
        INSERT INTO youtube_trending
        (video_id, title, channel_name, published_at, views, likes, comments)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (video_id)
        DO NOTHING
        """,
        (
            video_id,
            title,
            channel_name,
            published_at,
            views,
            likes,
            comments
        )
    )

    print(f"Inserted: {title}")

conn.commit()

cursor.close()
conn.close()

print("\nAll videos inserted successfully!")