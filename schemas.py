from pydantic import BaseModel

class Task(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: str
    done: bool
