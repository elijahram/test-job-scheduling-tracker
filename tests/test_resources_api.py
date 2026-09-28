def test_get_resources(client):
    response = client.get("/resources/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data == []


def test_create_resource(client):
    resource_data = {"name": "Test Resource", "type": "Test Type"}
    response = client.post("/resources/", json=resource_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == resource_data["name"]
    assert data["type"] == resource_data["type"]
    assert "id" in data
