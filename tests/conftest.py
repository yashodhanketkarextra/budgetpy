import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture
def auth_token(client: TestClient):
    test_user = {"name": "test_user", "password": "secureTestPassword"}
    client.post("/register", json=test_user)

    # token provider
    response = client.post("/login", json=test_user)
    token = response.json()["token"]
    yield token

    # cleanup
    client.delete(f"/users/{test_user['name']}")


TEST_USER = {"name": "test_user", "password": "secureTestPassword"}


def AUTH_HEADER(token):
    return {"Authorization": f"Bearer {token}"}
