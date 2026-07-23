from fastapi import APIRouter, Response
from typing import Optional

import services.service as service
from schemas import Task, TaskUpdate

router = APIRouter()

@router.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/tasks")
def get_tasks(
    done: Optional[bool] = None,
    search: Optional[str] = None
):
    return service.get_tasks(done, search)


@router.get("/tasks/{id}")
def get_task(id: int):
    return service.get_task(id)


@router.post("/tasks", status_code=201)
def create(task: Task):
    return service.create_task(task)


@router.put("/tasks/{id}")
def update(id: int, task: TaskUpdate):
    return service.update_task(id, task)


@router.delete("/tasks/{id}", status_code=204)
def delete(id: int):

    service.delete_task(id)

    return Response(status_code=204)


@router.get("/stats")
def stats():
    return service.get_stats()