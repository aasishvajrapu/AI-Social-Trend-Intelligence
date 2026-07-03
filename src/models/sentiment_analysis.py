import psycopg2
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

conn = psycopg2.connect(
    host="localhost",
    database="trend_intelligence",
    user="postgres",
    password="enter your password here",
    port="5432"
)

cursor = conn.cursor()

cursor.execute("""
SELECT id, comment
FROM youtube_comments
WHERE comment IS NOT NULL;
""")

comments = cursor.fetchall()

for row in comments:
    comment_db_id = row[0]
    text = row[1]

    score = analyzer.polarity_scores(text)
    compound = score["compound"]

    if compound >= 0.05:
        sentiment = "Positive"
    elif compound <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    cursor.execute("""
        UPDATE youtube_comments
        SET sentiment = %s
        WHERE id = %s
    """, (sentiment, comment_db_id))

    print(f"{sentiment}: {text[:50]}")

conn.commit()

cursor.close()
conn.close()

print("Sentiment analysis completed!")
