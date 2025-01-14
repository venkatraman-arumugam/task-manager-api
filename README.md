## TaskManagerAPI
HomeAssignment as part of the interview process at Squid IQ.

### Overview

A Flask-based Task Manager API that utilizes Redis as both the Celery broker and backend for asynchronous task processing.

## Features

- **Task Management**: Create, retrieve, update, and delete tasks.
- **Asynchronous Processing**: Tasks are processed asynchronously using Celery.
- **Redis Integration**: Redis serves as both the message broker and result backend for Celery.
- **Dockerized Services**: The application, along with Redis and Celery, can be run using Docker Compose for easy setup.
- **Centralized Logging**: Fluentd integration for centralized logging. 
## Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your machine.
- [Docker Compose](https://docs.docker.com/compose/install/) installed.

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/venkatraman-arumugam/task-manager-api.git
cd task-manager-api
```
### Build and Run the Application

Run with docker-compose.override.yml for development (picked up by default):

bash
Copy code


```bash
docker-compose up --build
```

## UI

```commandline
http://localhost:5000/
```

## API Endpoints

POST /tasks: Create a new task.

Request

```commandline
curl --location 'http://127.0.0.1:5000/tasks' \
--header 'Content-Type: application/json' \
--data '{"task_name": "test", "duration": 3}'
```

Response (Sample)

```commandline
{
    "status": "QUEUED",
    "submitted_at": "2025-01-13 06:53:09",
    "task_id": "a491f24b-5966-4fc1-a81f-6aa78f6ce6b7"
}
```

GET /tasks: Retrieve all tasks with their statuses.

Request

```commandline
curl --location 'http://127.0.0.1:5000/tasks'
```
Response (Sample)

```commandline
{
    "pagination": {
        "current_page": 1,
        "page_size": 10,
        "total_pages": 4,
        "total_tasks": 40
    },
    "tasks": [
        {
            "result": "Task completed in 10 seconds",
            "status": "COMPLETED",
            "submitted_at": "2025-01-13 02:33:42",
            "task_id": "c0b5d97e-7834-48e8-9005-124ce1916a9a"
        },
        {
            "result": "Task completed in 10 seconds",
            "status": "COMPLETED",
            "submitted_at": "2025-01-13 02:33:43",
            "task_id": "cbc256c5-38dc-40aa-8651-be53e5a0a4e3"
        }
    ]
}
```
GET /tasks/<task_id>: Retrieve a specific task by its ID.

Request

```commandline
curl --location 'http://127.0.0.1:5000/tasks/<task_id>'
```

Response (Sample)

```commandline
{
    "result": "Task completed in 3 seconds",
    "status": "COMPLETED",
    "submitted_at": "2025-01-13 06:53:09",
    "task_id": "a491f24b-5966-4fc1-a81f-6aa78f6ce6b7"
}
```

### Failure Scenarios 

To stimulate and play with failure scenarios following commands can be used

#### Stop Celery
To simulate Celery unavailability:

```
 docker-compose stop celery
```

#### Stop Redis
To simulate Redis unavailability:
```
 docker-compose stop redis
```

#### Stop Flask
To simulate API server downtime:
```
 docker-compose stop flask
```