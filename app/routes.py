import time
import uuid

from flask import Blueprint, request, jsonify

from app.long_running_task import long_running_task
from app.models import TaskRequest, TaskResponse

task_bp = Blueprint("tasks", __name__)

tasks = {}

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

    tasks[task_id] = {
        "status": "QUEUED",
        "submitted_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "task_name": task_data.task_name,
        "duration": task_data.duration,
    }

    response = TaskResponse(task_id=task_id, status=tasks[task_id].get("status"), submitted_at=tasks[task_id].get("submitted_at"))

    return jsonify(response.model_dump()), 202