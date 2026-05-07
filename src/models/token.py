from datetime import UTC, datetime, timedelta
from typing import Tuple

import jwt
from pydantic.main import BaseModel

from src.config import settings as sc


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str | None = None
    username: str | None = None


def check_env() -> str:
    import os

    SECRET_KEY = os.getenv("SECRET_KEY")

    if not SECRET_KEY:
        raise ValueError("SECRET_KEY is not set")
    return SECRET_KEY


async def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
) -> Tuple[str, bool]:
    expire = (
        datetime.now(UTC) + expires_delta
        if expires_delta
        else datetime.now(UTC) + timedelta(minutes=sc.TOKEN_EXP)
    )

    to_encode = {"username": data.get("name"), "id": data.get("id"), "exp": expire}
    encoded_jwt = jwt.encode(to_encode, sc.SECRET_KEY, sc.ALGORITHM)

    return encoded_jwt, True


async def validate_token(token: str) -> Tuple[TokenData, bool]:
    try:
        payload = jwt.decode(token, sc.SECRET_KEY, algorithms=[sc.ALGORITHM])
        username: str = payload["username"]
        id: str = payload["id"]

        if not username or not id:
            return TokenData(), False

        return TokenData(id=id, username=username), True

    except (jwt.PyJWTError, KeyError):
        return TokenData(), False
