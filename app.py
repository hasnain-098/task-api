from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel

app = FastAPI()

tasks = [
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

class Task(BaseModel):
    title: str

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
def get_tasks():
    return tasks

@app.get("/tasks/{id}")
def get_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {id} not found"
    )

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