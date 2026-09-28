def test_get_bookings(client):
    response = client.get("/bookings/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data == []


def test_create_booking(client):
    resource_response = client.post(
        "/resources/", json={"name": "Test Resource", "type": "Test Type"}
    )
    booking_data = {
        "resource_id": resource_response.json()["id"],
        "start_time": "2026-09-24T09:00:00",
        "end_time": "2026-09-24T10:00:00",
    }
    response = client.post("/bookings/", json=booking_data)
    assert response.status_code == 200
    data = response.json()
    assert data["resource_id"] == booking_data["resource_id"]
    assert data["start_time"] == booking_data["start_time"]
    assert data["end_time"] == booking_data["end_time"]
    assert "id" in data


def test_booking_conflict_returns_409(client):
    resource_response = client.post(
        "/resources/", json={"name": "Test Resource", "type": "Test Type"}
    )
    booking_data = {
        "resource_id": resource_response.json()["id"],
        "start_time": "2026-09-24T09:00:00",
        "end_time": "2026-09-24T10:00:00",
    }
    client.post("/bookings/", json=booking_data)

    conflicting_booking_data = {
        "resource_id": resource_response.json()["id"],
        "start_time": "2026-09-24T09:30:00",
        "end_time": "2026-09-24T10:30:00",
    }
    response = client.post("/bookings/", json=conflicting_booking_data)
    assert response.status_code == 409
    data = response.json()
    assert data["detail"] == "Booking conflicts with an existing booking."
