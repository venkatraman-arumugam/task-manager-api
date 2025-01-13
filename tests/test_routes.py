import time

def get_current_task_length(client):
    response = client.get(f"/tasks")
    data = response.get_json()
    return data["pagination"]["total_tasks"]

def wait_for_task_completion(client, count, retries=5, delay=1, ):
    """Helper function to wait for tasks to complete."""

    for _ in range(retries):
        response = client.get("/tasks")
        data = response.get_json()
        time.sleep(delay)
        if data["pagination"]["total_tasks"] >= count:
            return True
    return False

def test_create_task(client):
    current_length = get_current_task_length(client)
    response = client.post("/tasks", json={"task_name": "Test Task", "duration": 1})

    assert wait_for_task_completion(client, current_length + 1, retries=5, delay=1), "Tasks did not complete in time."
    assert response.status_code == 202
    data = response.get_json()
    assert "task_id" in data
    assert data["status"] == "QUEUED"

def test_get_task_status(client):
    current_length = get_current_task_length(client)

    response = client.post("/tasks", json={"task_name": "Test Task", "duration": 1})
    task_id = response.get_json()["task_id"]

    assert wait_for_task_completion(client, current_length + 1, retries=5, delay=1), "Tasks did not complete in time."

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["task_id"] == task_id
    assert data["status"] == "COMPLETED"

def test_get_all_tasks(client):
    current_length = get_current_task_length(client)

    client.post("/tasks", json={"task_name": "Test Task", "duration": 1})
    client.post("/tasks", json={"task_name": "Test Task", "duration": 1})
    client.post("/tasks", json={"task_name": "Test Task", "duration": 1})

    assert wait_for_task_completion(client, current_length + 3, retries=5, delay=1), "Tasks did not complete in time."