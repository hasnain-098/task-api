from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
import copy
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
    done BOOLEAN NOT NULL
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

INITIAL_TASKS = [
    {
        "id":1,
        "title":"Learn FastAPI",
        "done":False
    },
    {
        "id":2,
        "title":"Complete Assignment",
        "done":False
    },
    {
        "id":3,
        "title":"Push to GitHub",
        "done":True
    }
]

tasks = copy.deepcopy(INITIAL_TASKS)

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

    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()

    result = []
    for row in rows:
        result.append(
            {
                "id": row["id"],
                "title": row["title"],
                "done": bool(row["done"]),
            }
        )

    if done is not None:
        result = [
            task for task in result
            if task["done"] == done
        ]

    if search:
        result = [
            task for task in result
            if search.lower() in task["title"].lower()
        ]

    return result

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

    newTask = {
        "id": len(tasks) + 1,
        "title": task.title,
        "done": False
    }
    tasks.append(newTask)

    return newTask

@app.put("/tasks/{id}")
def update_task(id: int, data: TaskUpdate):
    if data.title.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Task title cannot be empty"
        )

    for task in tasks:
        if task["id"] == id:
            task["title"] = data.title
            task["done"] = data.done
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {id} not found"
    )

@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: int):
    for task in tasks:
        if task["id"] == id:
            tasks.remove(task)
            return

    raise HTTPException(
        status_code=404,
        detail=f"Task {id} not found"
    )

@app.get("/stats")
def get_stats():
    total = len(tasks)

    done = len([
        task for task in tasks
        if task["done"]
    ])

    open_tasks = total - done

    return {
        "total": total,
        "done": done,
        "open_tasks": open_tasks,
    }