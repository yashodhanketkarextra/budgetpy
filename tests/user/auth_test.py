from tests.conftest import AUTH_HEADER, TEST_USER


class TestAuthentication:
    def test_successfull_login(self, auth_token):
        assert auth_token is not None

    def test_get_me_with_jwt(self, auth_token, client):
        response = client.get("/me", headers=AUTH_HEADER(auth_token))
        assert response.status_code == 200
        assert response.json()["user"] == TEST_USER["name"]


class TestLoginFailures:
    def test_login_unregisterd_user(self, client):
        user = {"name": "fake", "password": "securePasswords"}
        response = client.post("/login", json=user)
        assert response.status_code == 404
        assert response.json()["result"] == "No such user found. Please register"

    def test_login_wrong_password(self, client):
        user = {"name": "users", "password": "securePassword"}
        client.post("/register", json=user)

        user["password"] = "wrongPassword"
        response = client.post("/login", json=user)
        assert response.status_code == 403
        assert response.json()["result"] == "Invalid credentials. Please try again"

        # cleanup
        client.delete("/users/users")
