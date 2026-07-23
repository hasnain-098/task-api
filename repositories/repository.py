from database import cursor, conn

def get_all(done=None, search=None):

    query = "SELECT * FROM tasks"

    conditions = []
    params = []

    if done is not None:
        conditions.append("done=%s")
        params.append(int(done))

    if search:
        conditions.append("title LIKE %s")
        params.append(f"%{search}%")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY title"

    cursor.execute(query, params)

    return cursor.fetchall()


def get_by_id(task_id):

    cursor.execute(
        "SELECT * FROM tasks WHERE id=%s",
        (task_id,)
    )

    return cursor.fetchone()

def create(title):

    cursor.execute(
        """
        INSERT INTO tasks(title,done)
        VALUES(%s,%s)
        RETURNING *
        """,
        (title, False)
    )

    conn.commit()

    return cursor.fetchone()

def update(task_id, title, done):

    cursor.execute(
        """
        UPDATE tasks
        SET
            title=%s,
            done=%s,
            updated_at=CURRENT_TIMESTAMP
        WHERE id=%s
        """,
        (title, bool(done), task_id)
    )

    conn.commit()

    return get_by_id(task_id)

def delete(task_id):

    cursor.execute(
        "DELETE FROM tasks WHERE id=%s",
        (task_id,)
    )

    conn.commit()

def stats():

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM tasks
    """)

    total = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COUNT(*) AS completed
        FROM tasks
        WHERE done = TRUE
    """)

    completed = cursor.fetchone()["completed"]

    return total, completed
