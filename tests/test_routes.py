import time


def test_create_task(client):
    response = client.post("/tasks", json={"task_name": "Test Task", "duration": 5})
    assert response.status_code == 202
    data = response.get_json()
    assert "task_id" in data
    assert data["status"] == "QUEUED"

def test_get_task_status(client):
    # Create a task
    response = client.post("/tasks", json={"task_name": "Test Task", "duration": 1})
    print(response.get_json())
    task_id = response.get_json()["task_id"]

    time.sleep(2)
    # Get task status
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["task_id"] == task_id
    assert data["status"] == "COMPLETED"