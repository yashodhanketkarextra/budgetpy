from unittest import mock

from tests.conftest import TEST_USER


class TestUserManagement:
    def test_get_all_users_flow(self, client):
        assert client.get("/users").json()["users"] == []

        client.post("/register", json=TEST_USER)
        response = client.get("/users")
        assert response.status_code == 200
        assert response.json()["users"][0]["name"] == "test_user"

        client.delete(f"/users/{TEST_USER['name']}")

    def test_prevent_duplicate_user_registration(self, client):
        client.post("/register", json=TEST_USER)
        response = client.post("/register", json=TEST_USER)

        assert response.status_code == 400
        assert response.json()["result"] == "User already exists"
        client.delete(f"/users/{TEST_USER['name']}")

    def test_delete_ghost_user_returns_404(self, client):
        response = client.delete("/users/ghost_user")
        assert response.status_code == 404
        assert response.json()["result"] == "User not found"


class TestMissingEnv:
    def test_delete_user(self, client):
        client.post("/register", json=TEST_USER)
        with mock.patch("src.config.settings.PY_ENV", "prod"):
            response = client.delete("/users/test_user")
            assert response.status_code == 403
            assert response.json()["result"] == "Forbidden"
