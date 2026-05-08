from functools import wraps

from fastapi import HTTPException
from starlette.requests import Request

from src.models.token import validate_token


async def handle_jwt(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="No token provided")

    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Malformed token")

    token = auth_header.split(" ")[1]
    try:
        payload, success = await validate_token(token)
        if not success:
            raise HTTPException(status_code=401, detail="Unauthorized")

        request.state.username = payload.username
        request.state.id = payload.id

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


def jwt_protect(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = kwargs.get("request")
        if not request:
            raise HTTPException(status_code=400, detail="Request object missing")

        await handle_jwt(request)
        return await func(*args, **kwargs)

    return wrapper
