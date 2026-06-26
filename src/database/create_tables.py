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
CREATE TABLE IF NOT EXISTS social_posts (
    id SERIAL PRIMARY KEY,
    source VARCHAR(50),
    post_id VARCHAR(100),
    title TEXT,
    content TEXT,
    author VARCHAR(100),
    score INTEGER,
    created_at TIMESTAMP,
    sentiment VARCHAR(20),
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

conn.commit()
cursor.close()
conn.close()

print("Table created successfully!")