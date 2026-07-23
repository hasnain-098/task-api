# Task API

A simple CRUD API built using **FastAPI** with **PostgreSQL** for persistent storage and **Docker Compose** for containerized deployment.

## Features
- Create, Read, Update, and Delete tasks
- PostgreSQL database with persistent storage
- Automatic database initialization and seeding
- Docker Compose support for one-command setup
- Interactive API documentation with Swagger UI

## Why PostgreSQL?
PostgreSQL was chosen because it is a powerful, open-source relational database management system that provides reliability, scalability, and SQL compliance. It is widely used in production environments and supports advanced querying and data integrity features.

## Database
The application uses a PostgreSQL database running inside a Docker container.  
On application startup it automatically:
- Creates the `tasks` table if it does not exist.
- Seeds three sample tasks when the table is empty.
- Preserves data using a Docker volume (`postgres_data`).

## Prerequisites
- Python 3.13+
- Docker Desktop
- Docker Compose

## Installation
```
pip install -r requirements.txt
```

## Run Locally
Start the PostgreSQL container:

```bash
docker compose up -d db
```

Run the FastAPI application:
```bash
uvicorn app:app --reload
```

## Run with Docker Compose
Start the complete application stack:

```bash
docker compose up --build
```

The API will be available at:

```
http://localhost:8000
```

## Endpoints

GET /  
GET /health  
GET /tasks  
GET /tasks/{id}  
GET /stats  
POST /tasks  
PUT /tasks/{id}  
DELETE /tasks/{id}  

## Example

curl -X GET http://localhost:8000/tasks

## Swagger

http://localhost:8000/docs

<p align="center">
  <img src="screenshots/swagger_ui.png" width="800">
</p>

## Example SQL Query
SELECT COUNT(*) FROM tasks;  
This query returns the total number of tasks currently stored in the SQLite database.  

## Technologies Used
- Python  
- FastAPI  
- PostgreSQL
- Psycopg
- Docker
- Docker Compose
- Uvicorn  

## Project Structure
```
task-api/
├── routes/
├── services/
├── repositories/
├── schemas.py
├── database.py
├── app.py
├── Dockerfile
├── compose.yaml
├── .env (git ignored)
├── requirements.txt
└── README.md
```

## Notes
- The PostgreSQL database starts automatically using Docker Compose.
- The `tasks` table is created automatically if it does not exist.
- Three sample tasks are inserted only when the table is empty.
- SQL queries use parameterized placeholders (`%s`) to prevent SQL injection.
- Database data persists across container restarts using the `postgres_data` Docker volume.
 
