def create_project(client, auth_headers):
    response = client.post("/projects/", json={"title": "Test", "description": "A test project"}, headers=auth_headers)
    return {"owner_id": response.json()["owner_id"], "project_id": response.json()["id"]}

def create_task(client, auth_headers, project):
    response = client.post(f"projects/{project['project_id']}/tasks/", json={"name": "Test Task", "description": "A test task", "status": "todo", "priority": "medium", "assignee_id": project["owner_id"]}, headers=auth_headers)
    return response.json()["id"]

def test_create_task_success(client, auth_headers):
    project = create_project(client, auth_headers)
    response = client.post(f"projects/{project['project_id']}/tasks/", json={"name": "Test Task", "description": "A test task", "status": "todo", "priority": "medium", "assignee_id": project["owner_id"]}, headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Test Task"
    assert data["description"] == "A test task"
    assert data["status"] == "todo"
    assert data["priority"] == "medium"
    assert data["project_id"] == project["project_id"]
    assert data["assignee_id"] == project["owner_id"]
    assert "id" in data

def test_create_task_missing_fields(client, auth_headers):
    project = create_project(client, auth_headers)
    response = client.post(f"projects/{project['project_id']}/tasks/", json={}, headers=auth_headers)
    assert response.status_code == 422

def test_list_tasks(client, auth_headers):
    project = create_project(client, auth_headers)
    task_id = create_task(client, auth_headers, project)

    response = client.get(f"projects/{project['project_id']}/tasks/", headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert any(task["id"] == task_id for task in data)

def test_get_task_by_id(client, auth_headers):
    project = create_project(client, auth_headers)
    task_id = create_task(client, auth_headers, project)

    response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == task_id
    assert data["name"] == "Test Task"
    assert data["description"] == "A test task"
    assert data["project_id"] == project["project_id"]
    assert data["assignee_id"] == project["owner_id"]
    assert data["status"] == "todo"
    assert data["priority"] == "medium"

def test_get_task_not_found(client, auth_headers):
    response = client.get("/tasks/9999", headers=auth_headers)
    assert response.status_code == 404

def test_update_task_success(client, auth_headers):
    project = create_project(client, auth_headers)
    task_id = create_task(client, auth_headers, project)

    response = client.put(f"/tasks/{task_id}", json={"name": "Updated Task", "description": "Updated test task", "status": "in_progress", "priority": "high"}, headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == task_id
    assert data["name"] == "Updated Task"
    assert data["description"] == "Updated test task"
    assert data["project_id"] == project["project_id"]
    assert data["assignee_id"] == project["owner_id"]
    assert data["status"] == "in_progress"
    assert data["priority"] == "high"

def test_update_task_missing_fields(client, auth_headers):
    project = create_project(client, auth_headers)
    task_id = create_task(client, auth_headers, project)

    response = client.put(f"/tasks/{task_id}", json={}, headers=auth_headers)
    assert response.status_code == 200

def test_delete_task_success(client, auth_headers):
    project = create_project(client, auth_headers)
    task_id = create_task(client, auth_headers, project)

    response = client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200

    # Verify task is deleted
    response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 404

def test_delete_task_not_found(client, auth_headers):
    response = client.delete("/tasks/9999", headers=auth_headers)
    assert response.status_code == 404

def test_create_task_invalid_project(client, auth_headers):
    response = client.post("projects/9999/tasks/", json={"name": "Test Task", "description": "A test task", "project_id": 9999, "status": "todo", "priority": "medium"}, headers=auth_headers)
    assert response.status_code == 403

def test_create_task_invalid_user(client, auth_headers):
    # Create a task with a different user
    response = client.post("/auth/register", json={"email": "otheruser", "password": "otherpass"})
    assert response.status_code == 200

    response = client.post("/auth/login", data={"username": "otheruser", "password": "otherpass"})
    assert response.status_code == 200
    other_token = response.json()["access_token"]
    other_headers = {"Authorization": f"Bearer {other_token}"}

    project = create_project(client, auth_headers)
    response = client.post(f"projects/{project['project_id']}/tasks/", json={"name": "Test Task", "description": "A test task", "project_id": project["project_id"], "status": "todo", "priority": "medium"}, headers=other_headers)
    assert response.status_code == 403