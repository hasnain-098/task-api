from fastapi import HTTPException
import repositories.repository as repository

def serialize(row):

    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"]),
        "created_at": row["created_at"],
        "updated_at": row["updated_at"]
    }

def get_tasks(done, search):

    rows = repository.get_all(done, search)

    return [serialize(row) for row in rows]

def get_task(task_id):

    row = repository.get_by_id(task_id)

    if row is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    return serialize(row)

def create_task(task):

    if task.title.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Task title cannot be empty"
        )

    return serialize(repository.create(task.title))

def update_task(task_id, task):

    if task.title.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Task title cannot be empty"
        )

    if repository.get_by_id(task_id) is None:

        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    return serialize(
        repository.update(
            task_id,
            task.title,
            task.done
        )
    )

def delete_task(task_id):

    if repository.get_by_id(task_id) is None:

        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    repository.delete(task_id)

def get_stats():

    total, completed = repository.stats()

    return {
        "total": total,
        "done": completed,
        "open_tasks": total - completed
    }
