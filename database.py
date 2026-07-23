import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

conn = psycopg.connect(
    host=os.getenv("DB_HOST"),
    port=(os.getenv("DB_PORT")),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

conn.autocommit = True
cursor = conn.cursor(row_factory=psycopg.rows.dict_row)

def initialize_database():
    cursor.execute("""
       CREATE TABLE IF NOT EXISTS tasks(
           id SERIAL PRIMARY KEY,
           title VARCHAR(255) NOT NULL,
           done BOOLEAN NOT NULL DEFAULT FALSE,
           created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
           updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
           )
       """)

    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()["count"]

    if count > 0:
        return

    if count == 0:

        cursor.executemany(
            """
            INSERT INTO tasks(title,done)
            VALUES(%s,%s)
            """,
            [
                ("Learn FastAPI", False),
                ("Complete Assignment", False),
                ("Push to GitHub", True)
            ]
        )

initialize_database()
