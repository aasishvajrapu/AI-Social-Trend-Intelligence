from db_connection import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS video_history(
    id SERIAL PRIMARY KEY,
    video_id VARCHAR(100),
    title TEXT,
    views BIGINT,
    likes BIGINT,
    comments BIGINT,
    captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

conn.commit()
conn.close()

print("History table created.")