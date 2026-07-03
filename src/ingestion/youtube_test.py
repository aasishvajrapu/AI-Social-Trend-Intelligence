import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

youtube = build(
    "youtube",
    "v3",
    developerKey=API_KEY
)

request = youtube.videos().list(
    part="snippet,statistics",
    chart="mostPopular",
    regionCode="IN",
    maxResults=10
)

response = request.execute()

for video in response["items"]:
    print("=" * 80)
    print("Title:", video["snippet"]["title"])
    print("Channel:", video["snippet"]["channelTitle"])
    print("Views:", video["statistics"].get("viewCount", "N/A"))
    print("Published:", video["snippet"]["publishedAt"])