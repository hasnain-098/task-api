from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Response
from pydantic import BaseModel
from typing import Optional
import sqlite3

app = FastAPI()
conn = sqlite3.connect(
    "tasks.db",
    check_same_thread=False
)

conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

cursor.execute("SELECT COUNT(*) FROM tasks")
count = cursor.fetchone()[0]

if count == 0:
    sample_tasks = [
        ("Learn FastAPI", False),
        ("Complete Assignment", False),
        ("Push to GitHub", True),
    ]

    cursor.executemany(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        sample_tasks
    )

    conn.commit()

class Task(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: str
    done: bool

@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": [
            "/tasks"
        ]
    }

@app.get("/health")
def health():
    return {
        "status": "ok"
    }

@app.get("/tasks")
def get_tasks(
        done: Optional[bool] = None,
        search: Optional[str] = None,
    ):

    query = """SELECT * FROM tasks"""

    conditions = []
    params = []

    if done is not None:
        conditions.append("done = ?")
        params.append(int(done))

    if search:
        conditions.append("title LIKE ?")
        params.append(f"%{search}%")

    if conditions:
        query += " WHERE " + " AND " .join(conditions)

    query += " ORDER BY title"

    cursor.execute(query, params)
    rows = cursor.fetchall()

    return [
        {
            "id": row["id"],
            "title": row["title"],
            "done": bool(row["done"]),
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }
        for row in rows
    ]

@app.get("/tasks/{id}")
def get_task(id: int):

    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    )

    row = cursor.fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {id} not found"
        )

    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"])
    }

@app.post("/tasks", status_code=201)
def create_task(task: Task):
    if task.title.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Task title cannot be empty"
        )

    cursor.execute(
        """INSERT INTO tasks (title, done) VALUES (?, ?)""",
        (task.title, False)
    )
    conn.commit()

    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (cursor.lastrowid,)
    )
    row = cursor.fetchone()

    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"]),
        "created_at": row["created_at"],
        "updated_at": row["updated_at"]
    }

@app.put("/tasks/{id}")
def update_task(id: int, data: TaskUpdate):
    if data.title.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Task title cannot be empty"
        )

    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    )

    if cursor.fetchone() is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {id} not found"
        )

    cursor.execute(
        """
        UPDATE tasks 
        SET title = ?, done = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (data.title, int(data.done), id)
    )

    conn.commit()

    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    )
    row = cursor.fetchone()

    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"]),
        "created_at": row["created_at"],
        "updated_at": row["updated_at"]
    }

@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: int):
    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    )
    if cursor.fetchone() is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {id} not found"
        )

    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (id,)
    )
    conn.commit()

    return Response(status_code=204)

@app.get("/stats")
def get_stats():
    cursor.execute("SELECT COUNT(*) FROM tasks")
    total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM tasks WHERE done = 1"
    )
    completed = cursor.fetchone()[0]

    return {
        "total": total,
        "done": completed,
        "open_tasks": total - completed
    }