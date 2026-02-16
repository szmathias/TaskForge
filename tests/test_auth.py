def test_auth_new_user(client):
    # Test registration
    response = client.post("/auth/register", json={"email": "newuser", "password": "newpass"})
    assert response.status_code == 200

    # Test login
    response = client.post("/auth/login", data={"username": "newuser", "password": "newpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_auth_invalid_login(client):
    # Test login with invalid credentials
    response = client.post("/auth/login", data={"username": "invaliduser", "password": "invalidpass"})
    assert response.status_code == 401

def test_auth_access_protected_route(client, auth_headers):
    # Test access to a protected route with valid token
    response = client.get("/projects/", headers=auth_headers)
    assert response.status_code == 200

def test_auth_access_protected_route_no_token(client):
    # Test access to a protected route without token
    response = client.get("/projects/")
    assert response.status_code == 401