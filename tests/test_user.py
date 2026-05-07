import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.fixture
def auth_token():
    test_user_name = "username"
    user = {"name": test_user_name, "password": "securePassword"}
    client.post("/register", json=user)
    response = client.post("/login", json=user)
    token = response.json()["token"]

    yield token

    client.delete(f"/users/{test_user_name}")


def test_login(auth_token):
    assert auth_token is not None


def test_get_me_wth_jwt(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["user"] == "username"
