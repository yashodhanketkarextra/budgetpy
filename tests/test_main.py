from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_add_root():
    response = client.post("/add", json={"first": 1, "second": 2})
    assert response.status_code == 200
    assert response.json() == {"result": 3}


def test_add_root_invalid():
    response = client.post("/add", json={"first": 1, "second": "a"})
    assert response.status_code == 422
