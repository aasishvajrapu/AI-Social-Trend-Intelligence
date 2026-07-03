import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
import psycopg2
from datetime import datetime

# Load environment variables
load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# PostgreSQL connection
conn = psycopg2.connect(
    host="localhost",
    database="trend_intelligence",
    user="postgres",
    password="enter your password here",
    port="5432"
)

cursor = conn.cursor()

# Connect to YouTube API
youtube = build(
    "youtube",
    "v3",
    developerKey=YOUTUBE_API_KEY
)

# Get video IDs from database
cursor.execute("""
SELECT video_id
FROM youtube_trending
LIMIT 10;
""")

videos = cursor.fetchall()

for row in videos:
    video_id = row[0]

    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=20,
            textFormat="plainText"
        )

        response = request.execute()

        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]

            comment_id = item["snippet"]["topLevelComment"]["id"]
            author = comment["authorDisplayName"]
            text = comment["textDisplay"]
            likes = comment["likeCount"]

            published_at = datetime.strptime(
                comment["publishedAt"],
                "%Y-%m-%dT%H:%M:%SZ"
            )

            cursor.execute(
                """
                INSERT INTO youtube_comments
                (video_id, comment_id, author, comment, likes, published_at)
                VALUES (%s,%s,%s,%s,%s,%s)
                ON CONFLICT (comment_id)
                DO NOTHING
                """,
                (
                    video_id,
                    comment_id,
                    author,
                    text,
                    likes,
                    published_at
                )
            )

        print(f"Comments fetched for video: {video_id}")

    except Exception as e:
        print(f"Could not fetch comments for {video_id}")
        print(e)

conn.commit()

cursor.close()
conn.close()

print("\nComments ingestion completed!")
