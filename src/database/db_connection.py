import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="trend_intelligence",
        user="postgres",
        password="enter your password here",
        port="5432"
    )

    print("Connected to PostgreSQL successfully!")

    conn.close()

except Exception as e:
    print("Connection failed:")
    print(e)
