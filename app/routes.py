import time
import uuid

from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from app import get_redis_instance
from app.models import (
    TaskPaginationRequest,
    PaginationMetadata,
    TaskPaginationResponse,
)
from app.models import TaskRequest, TaskResponse
from app.task import long_running_task

task_bp = Blueprint("tasks", __name__)

tasks = {}

redis_client = get_redis_instance()


@task_bp.route("/tasks", methods=["POST"])
def create_task():
    """Create a new task."""
    data = request.get_json()
    try:
        task_data = TaskRequest(**data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    task_id = str(uuid.uuid4())

    long_running_task.apply_async(args=[task_data.duration], task_id=task_id)

    task_meta_data = {
        "status": "QUEUED",
        "submitted_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "task_name": task_data.task_name,
        "duration": task_data.duration,
    }
    redis_client.hset(f"task:{task_id}", mapping=task_meta_data)

    redis_client.rpush("all_tasks", task_id)

    response = TaskResponse(
        task_id=task_id,
        task_name=task_data.task_name,
        status=task_meta_data.get("status"),
        submitted_at=task_meta_data.get("submitted_at"),
    )

    return jsonify(response.model_dump()), 202


@task_bp.route("/tasks/<task_id>", methods=["GET"])
def get_task_status(task_id):
    """Get task status."""
    task_metadata = redis_client.hgetall(f"task:{task_id}")
    if not task_metadata:
        return jsonify({"error": "Invalid or expired task ID"}), 404

    response = TaskResponse(
        task_id=task_id,
        task_name=task_metadata.get("task_name"),
        status=task_metadata.get("status"),
        submitted_at=task_metadata.get("submitted_at"),
        result=task_metadata.get("result"),
    )

    return jsonify(response.model_dump())


@task_bp.route("/tasks", methods=["GET"])
def get_all_tasks():
    """Get all tasks with their statuses, with pagination."""
    try:
        query_params = TaskPaginationRequest(**request.args)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    start = (query_params.page - 1) * query_params.page_size
    end = start + query_params.page_size - 1

    total_tasks = redis_client.llen("all_tasks")
    task_ids = redis_client.lrange("all_tasks", start, end)

    tasks = []

    for task_id in task_ids:
        task_metadata = redis_client.hgetall(f"task:{task_id}")
        if task_metadata:
            tasks.append(
                TaskResponse(
                    task_id=task_id,
                    task_name=task_metadata.get("task_name"),
                    status=task_metadata.get("status"),
                    submitted_at=task_metadata.get("submitted_at"),
                    result=task_metadata.get("result"),
                )
            )

    pagination = PaginationMetadata(
        current_page=query_params.page,
        page_size=query_params.page_size,
        total_tasks=total_tasks,
        total_pages=(total_tasks + query_params.page_size - 1)
        // query_params.page_size,
    )

    response = TaskPaginationResponse(tasks=tasks, pagination=pagination)
    return jsonify(response.model_dump())
