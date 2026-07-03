import schedule
import time
from youtube_ingestor import fetch_trending

schedule.every(1).hours.do(
    fetch_trending
)

while True:
    schedule.run_pending()
    time.sleep(60)