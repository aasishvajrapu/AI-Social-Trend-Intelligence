import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="trend_intelligence",
    user="postgres",
    password="Aasish@29",
    port="5432"
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS youtube_trending (
    id SERIAL PRIMARY KEY,
    video_id VARCHAR(50),
    title TEXT,
    channel_name TEXT,
    published_at TIMESTAMP,
    views BIGINT,
    likes BIGINT,
    comments BIGINT,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

conn.commit()
cursor.close()
conn.close()

print("youtube_trending table created!")