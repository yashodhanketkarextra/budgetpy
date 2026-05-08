import jwt
import pytest

from src.config import settings as sc
from src.models.token import validate_token


class TestJWTValidation:
    def test_invalidate_jwt_returns_401(self, client, db_session):
        response = client.get("/me", headers={"Authorization": "Bearer invalid_token"})
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid token"

    def test_malformed_jwt_returns_401(self, client, db_session):
        response = client.get("/me", headers={"Authorization": "malformed_token"})
        assert response.status_code == 401
        assert response.json()["detail"] == "Malformed token"

    def test_missing_jwt_returns_401(self, client, db_session):
        response = client.get("/me")
        assert response.status_code == 401
        assert response.json()["detail"] == "No token provided"

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "payload, test_id",
        [
            ({"username": "test_user", "id": None}, "none_id"),
            ({"username": None, "id": "test_id"}, "none_username"),
            ({"username": None, "id": None}, "both_none"),
            ({"username": "", "id": "123"}, "both_none"),
        ],
    )
    async def test_none_id_jwt_returns_error(self, payload, test_id, db_session):
        token = jwt.encode(payload, sc.SECRET_KEY, sc.ALGORITHM)
        token_data, success = await validate_token(token)

        assert success is False, f"Failed case: {test_id}"
        assert token_data.username is None
        assert token_data.id is None
