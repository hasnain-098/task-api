import sqlite3

conn = sqlite3.connect(
    "tasks.db",
    check_same_thread=False
)

conn.row_factory = sqlite3.Row
cursor = conn.cursor()

def initialize_database():

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        done BOOLEAN NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM tasks")

    if cursor.fetchone()[0] == 0:

        cursor.executemany(
            """
            INSERT INTO tasks(title,done)
            VALUES(?,?)
            """,
            [
                ("Learn FastAPI", False),
                ("Complete Assignment", False),
                ("Push to GitHub", True)
            ]
        )

        conn.commit()

initialize_database()
