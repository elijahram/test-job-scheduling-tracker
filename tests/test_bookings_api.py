from tests.conftest import TestingSessionLocal
from app.models import User
from app.security import hash_password


def register_and_login(client, username, email, password, role="engineer"):
    client.post(
        "auth/register/",
        json={"username": username, "email": email, "password": password, "role": role},
    )
    login_response = client.post(
        "auth/login/", data={"username": username, "password": password}
    )
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_get_bookings(client):
    headers = register_and_login(
        client, "testuser", "testuser@example.com", "testpassword"
    )
    response = client.get("/bookings/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data == []


def test_create_booking(client):
    db = TestingSessionLocal()
    admin_user = User(
        username="adminuser",
        email="adminuser@example.com",
        hashed_password=hash_password("adminpassword"),
        role="admin",
    )
    db.add(admin_user)
    db.commit()
    db.close()

    login_response = client.post(
        "auth/login/", data={"username": "adminuser", "password": "adminpassword"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {token}"}

    resource_data = {"name": "Test Resource", "type": "Test Type"}
    resource_response = client.post(
        "/resources/",
        json=resource_data,
        headers=admin_headers,
    )
    assert resource_response.status_code == 201

    headers = register_and_login(
        client, "testuser", "testuser@example.com", "testpassword"
    )

    booking_data = {
        "resource_id": resource_response.json()["id"],
        "start_time": "2026-09-24T09:00:00",
        "end_time": "2026-09-24T10:00:00",
    }
    booking_response = client.post("/bookings/", json=booking_data, headers=headers)
    assert booking_response.status_code == 201
    data = booking_response.json()
    assert data["resource_id"] == booking_data["resource_id"]
    assert data["start_time"] == booking_data["start_time"]
    assert data["end_time"] == booking_data["end_time"]
    assert "id" in data


def test_booking_conflict_returns_409(client):
    db = TestingSessionLocal()
    admin_user = User(
        username="adminuser",
        email="adminuser@example.com",
        hashed_password=hash_password("adminpassword"),
        role="admin",
    )
    db.add(admin_user)
    db.commit()
    db.close()

    login_response = client.post(
        "auth/login/", data={"username": "adminuser", "password": "adminpassword"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {token}"}

    resource_data = {"name": "Test Resource", "type": "Test Type"}
    resource_response = client.post(
        "/resources/",
        json=resource_data,
        headers=admin_headers,
    )
    assert resource_response.status_code == 201

    headers = register_and_login(
        client, "testuser", "testuser@example.com", "testpassword"
    )

    booking_data = {
        "resource_id": resource_response.json()["id"],
        "start_time": "2026-09-24T09:00:00",
        "end_time": "2026-09-24T10:00:00",
    }
    client.post("/bookings/", json=booking_data, headers=headers)

    conflicting_booking_data = {
        "resource_id": resource_response.json()["id"],
        "start_time": "2026-09-24T09:30:00",
        "end_time": "2026-09-24T10:30:00",
    }
    response = client.post("/bookings/", json=conflicting_booking_data, headers=headers)
    assert response.status_code == 409
    data = response.json()
    assert data["detail"] == "Booking conflicts with an existing booking."
