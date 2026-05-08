import src.models.user as U
from src.models.token import sc


async def register_user(data: U.UserDTO):
    return U.register_user(data)


async def get_all_users() -> list[dict[str, str | None]]:
    return [{"id": user.id, "name": user.name} for user in U.fake_users_db]


async def login_user(data: U.UserDTO) -> tuple[str | None, str, int]:
    user = U.get_user(data.name)
    if not user:
        return None, "No such user found. Please register", 404

    if not user.verify_password(data.password):
        return None, "Invalid credentials. Please try again", 403

    token = await user.gen_token()
    return token, "Success", 200


async def delete_user(username: str) -> tuple[str, int]:
    if sc.PY_ENV != "test":
        return "Forbidden", 403

    if not U.delete_user(username):
        return "User not found", 404

    return "Success", 200
