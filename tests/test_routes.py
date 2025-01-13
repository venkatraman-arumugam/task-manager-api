def test_create_task(client):
    response = client.post("/tasks", json={"task_name": "Test Task", "duration": 5})
    assert response.status_code == 202
    data = response.get_json()
    assert "task_id" in data
    assert data["status"] == "QUEUED"

