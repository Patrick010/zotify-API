from fastapi.testclient import TestClient

from minimal_test_app import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_create_and_read_item():
    # Create an item
    response_create = client.post("/items/1", json={"name": "Test Item"})
    assert response_create.status_code == 200
    assert response_create.json() == {"item_id": 1, "item": {"name": "Test Item"}}

    # Read the item back
    response_read = client.get("/items/1")
    assert response_read.status_code == 200
    assert response_read.json() == {"item_id": 1, "item": {"name": "Test Item"}}


def test_read_nonexistent_item():
    response = client.get("/items/99")
    assert response.status_code == 200
    assert response.json() == {"item_id": 99, "item": None}
