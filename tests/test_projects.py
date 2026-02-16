def create_project(client, auth_headers):
    response = client.post("/projects/", json={"title": "Test", "description": "A test project"}, headers=auth_headers)
    return response.json()["id"]

def test_create_project_success(client, auth_headers):
    response = client.post("/projects", json={"title": "Test Project", "description": "A test project"}, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Project"
    assert data["description"] == "A test project"
    assert "id" in data

def test_create_project_missing_name(client, auth_headers):
    response = client.post("/projects", json={}, headers=auth_headers)
    assert response.status_code == 422

def test_list_projects(client, auth_headers):
    # Create a project first
    project_id = create_project(client, auth_headers)

    response = client.get("/projects", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(project["id"] == project_id for project in data)

def test_get_project_by_id(client, auth_headers):
    # Create a project first
    project_id = create_project(client, auth_headers)

    response = client.get(f"/projects/{project_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == project_id
    assert data["title"] == "Test"
    assert data["description"] == "A test project"

def test_get_project_not_found(client, auth_headers):
    response = client.get("/projects/9999", headers=auth_headers)
    assert response.status_code == 403

def test_update_project_success(client, auth_headers):
    # Create a project first
    project_id = create_project(client, auth_headers)

    response = client.put(f"/projects/{project_id}", json={"title": "Updated Project", "description": "Updated test project"}, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == project_id
    assert data["title"] == "Updated Project"
    assert data["description"] == "Updated test project"

def test_update_project_missing_name(client, auth_headers):
    # Create a project first
    project_id = create_project(client, auth_headers)

    response = client.put(f"/projects/{project_id}", json={}, headers=auth_headers)
    assert response.status_code == 200

def test_delete_project_success(client, auth_headers):
    # Create a project first
    project_id = create_project(client, auth_headers)

    response = client.delete(f"/projects/{project_id}", headers=auth_headers)
    assert response.status_code == 200

    # Verify the project is deleted
    response = client.get(f"/projects/{project_id}", headers=auth_headers)
    assert response.status_code == 403

def test_delete_project_not_found(client, auth_headers):
    response = client.delete("/projects/9999", headers=auth_headers)
    assert response.status_code == 403

def test_update_project_not_found(client, auth_headers):
    response = client.put("/projects/9999", json={"name": "Nonexistent Project"}, headers=auth_headers)
    assert response.status_code == 403

def test_list_projects_empty(client, auth_headers):
    response = client.get("/projects", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0

def test_create_project_unauthorized(client):
    response = client.post("/projects", json={"title": "Unauthorized Project"})
    assert response.status_code == 401

def test_create_second_user_project_isolation(client, auth_headers):
    # Create a project with the first user
    project_id = create_project(client, auth_headers)

    # Register and login a second user
    response = client.post("/auth/register", json={"email": "seconduser", "password": "secondpass"})
    assert response.status_code == 200
    response = client.post("/auth/login", data={"username": "seconduser", "password": "secondpass"})
    assert response.status_code == 200
    second_token = response.json()["access_token"]
    second_auth_headers = {"Authorization": f"Bearer {second_token}"}

    # Verify the second user cannot see the first user's project
    response = client.get("/projects", headers=second_auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all(project["id"] != project_id for project in data)
