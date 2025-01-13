import time
import uuid

from flask import Blueprint, request, jsonify

from app.models import TaskRequest, TaskResponse
from app import get_redis_instance
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

    task = long_running_task.apply_async(args=[task_data.duration], task_id=task_id)

    task_meta_data = {
        "status": "QUEUED",
        "submitted_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "task_name": task_data.task_name,
        "duration": task_data.duration,
    }
    redis_client.hset(f"task:{task_id}", mapping=task_meta_data)

    redis_client.rpush("all_tasks", task_id)

    response = TaskResponse(task_id=task_id, status=task_meta_data.get("status"), submitted_at=task_meta_data.get("submitted_at"))

    return jsonify(response.model_dump()), 202