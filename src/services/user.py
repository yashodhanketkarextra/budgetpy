from sqlalchemy.orm import Session

import src.models.user as U
import src.repository.user as repo
from src.models.token import sc


def fmt(user) -> dict[str, str | None]:
    return {"id": str(user.id), "name": str(user.name)}


async def register_user(db: Session, data: U.UserDTO):
    return await repo.create_user(db, user_data=data)


async def get_all_users(db: Session) -> list[dict[str, str | None]]:
    users = await repo.get_all_users(db)
    return [fmt(user) for user in users]


async def login_user(db: Session, data: U.UserDTO) -> tuple[str | None, str, int]:
    user = await repo.get_user(db, username=data.name)
    if not user:
        return None, "No such user found. Please register", 404

    if not user.verify_password(data.password):
        return None, "Invalid credentials. Please try again", 403

    token = await user.gen_token()
    return token, "Success", 200


async def delete_user(db: Session, username: str) -> tuple[str, int]:
    if sc.PY_ENV != "test":
        return "Forbidden", 403

    if not await repo.delete_user(db, username):
        return "User not found", 404

    return "Success", 200
