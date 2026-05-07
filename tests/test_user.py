import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

TEST_USER = {"name": "test_user", "password": "secureTestPassword"}


def AUTH_HEADER(token):
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def auth_token():
    client.post("/register", json=TEST_USER)
    response = client.post("/login", json=TEST_USER)
    token = response.json()["token"]

    yield token

    client.delete(f"/users/{TEST_USER['name']}")


class TestAuthentication:
    def test_successfull_login(self, auth_token):
        assert auth_token is not None

    def test_get_me_with_jwt(self, auth_token):
        response = client.get("/me", headers=AUTH_HEADER(auth_token))
        assert response.status_code == 200
        assert response.json()["user"] == TEST_USER["name"]


class TestJWTValidation:
    def test_invalidate_jwt_returns_401(self):
        response = client.get("/me", headers={"Authorization": "Bearer invalid_token"})
        assert response.status_code == 401
        assert response.json()["result"] == "Invalid token"

    def test_malformed_jwt_returns_401(self):
        response = client.get("/me", headers={"Authorization": "malformed_token"})
        assert response.status_code == 401
        assert response.json()["result"] == "Malformed token"

    def test_missing_jwt_returns_401(self):
        response = client.get("/me", headers={"Authorization": "malformed_token"})
        assert response.status_code == 401
        assert response.json()["result"] == "Malformed token"


class TestUserManagement:
    def test_prevent_duplicate_user_registration(self):
        client.post("/register", json=TEST_USER)
        response = client.post("/register", json=TEST_USER)

        assert response.status_code == 400
        assert response.json()["result"] == "User already exists"
        client.delete(f"/users/{TEST_USER['name']}")

    def test_delete_ghost_user_returns_404(self):
        response = client.delete("/users/ghost_user")
        assert response.status_code == 404
        assert response.json()["result"] == "User not found"

    def test_get_all_users_flow(self):
        assert client.get("/users").json()["users"] == []

        client.post("/register", json=TEST_USER)
        response = client.get("/users")

        assert response.status_code == 200
        assert response.json()["users"][0]["name"] == "test_user"

        client.delete(f"/users/{TEST_USER['name']}")


class TestLoginFailures:
    def test_login_unregisterd_user(self):
        user = {"name": "fake", "password": "securePasswords"}
        response = client.post("/login", json=user)
        assert response.status_code == 404
        assert response.json()["result"] == "No such user found. Please register"

    def test_login_wrong_password(self):
        user = {"name": "users", "password": "securePassword"}
        client.post("/register", json=user)

        user["password"] = "wrongPassword"
        response = client.post("/login", json=user)
        assert response.status_code == 403
        assert response.json()["result"] == "Invalid credentials. Please try again"
