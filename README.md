# Task API

Simple CRUD API built using FastAPI.

## Installation
```
pip install -r requirements.txt
```
## Run
```
uvicorn app:app --reload
```
## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/tasks` | Get all tasks |
| GET | `/tasks?done=true` | Get completed tasks |
| GET | `/tasks?done=false` | Get pending tasks |
| GET | `/tasks?search=keyword` | Search tasks by title |
| GET | `/tasks/{id}` | Get a task by ID |
| POST | `/tasks` | Create a new task |
| PUT | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |
| GET | `/stats` | Get task statistics |
| POST | `/reset` | Reset tasks to default data |

## Example

curl -X GET http://localhost:8000/tasks

## Swagger

http://localhost:8000/docs

<p align="center">
  <img src="screenshots/swagger_ui.png" width="800">
</p>
