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
CREATE TABLE IF NOT EXISTS youtube_comments (
    id SERIAL PRIMARY KEY,
    video_id VARCHAR(50),
    comment_id VARCHAR(100) UNIQUE,
    author TEXT,
    comment TEXT,
    likes INTEGER,
    published_at TIMESTAMP,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

conn.commit()
cursor.close()
conn.close()

print("youtube_comments table created!")