from tests.conftest import TestingSessionLocal
from app.models import User
from app.security import hash_password


def register_and_login(client, username, email, password):
    client.post(
        "auth/register/",
        json={"username": username, "email": email, "password": password},
    )
    login_response = client.post(
        "auth/login/", data={"username": username, "password": password}
    )
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_get_resources(client):
    headers = register_and_login(
        client, "testuser", "testuser@example.com", "testpassword"
    )
    response = client.get("/resources/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data == []


def test_create_resource(client, admin_headers):
    resource_data = {"name": "Test Resource", "type": "Test Type"}
    response = client.post(
        "/resources/",
        json=resource_data,
        headers=admin_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == resource_data["name"]
    assert data["type"] == resource_data["type"]
    assert "id" in data
