import pytest
from fastapi import HTTPException

from src.middleware.auth import jwt_protect


@pytest.mark.asyncio
async def test_protector_missing_request(db_session):
    @jwt_protect
    async def fake_route():
        return "success"

    with pytest.raises(HTTPException, match="Request object missing"):
        await fake_route()
