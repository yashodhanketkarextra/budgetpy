from fastapi import APIRouter, Request, Response

import src.models.user as U
import src.services.user as userService
from src.middleware.auth import jwt_protect

userRouter = APIRouter()


@userRouter.post("/register")
async def register_user_handler(data: U.UserDTO, response: Response):
    success, message = await userService.register_user(data)
    response.status_code = 201 if success else 400
    return {"result": message}


@userRouter.get("/users")
async def get_users_handler():
    return {"users": await userService.get_all_users()}


@userRouter.post("/login")
async def login_user_handler(data: U.UserDTO, response: Response):
    token, message, status = await userService.login_user(data)

    response.status_code = status
    if token:
        return {"result": message, "token": token}

    return {"result": message}


@userRouter.get("/me")
@jwt_protect
async def verify_token_handler(request: Request):
    return {
        "result": "authenticated",
        "user": request.state.username,
        "id": request.state.id,
    }


@userRouter.delete("/users/{username}")
async def delete_user_handler(username: str, response: Response):
    message, status = await userService.delete_user(username)
    response.status_code = status
    return {"result": message}
