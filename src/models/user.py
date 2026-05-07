import uuid

from pwdlib import PasswordHash
from pydantic.main import BaseModel

from .token import create_access_token

hasher = PasswordHash.recommended()


class UserDTO(BaseModel):
    name: str
    password: str


class User(BaseModel):
    id: str | None = None
    name: str
    password: str

    def verify_password(self, plain_password: str) -> bool:
        return hasher.verify(plain_password, self.password)

    async def gen_token(self) -> str | None:
        (token, success) = await create_access_token({"name": self.name, "id": self.id})

        return token if success else None


fake_users_db: list[User] = []


def is_exist(username: str) -> bool:
    return any(u.name == username for u in fake_users_db)


def get_user(username: str) -> User | None:
    if not is_exist(username):
        return None

    return next(u for u in fake_users_db if u.name == username)


def register_user(user_data: UserDTO) -> bool:
    if is_exist(user_data.name):
        raise Exception("User already exists")

    new_user = User(
        id=str(uuid.uuid4()),
        name=user_data.name,
        password=encrypt_password(user_data.password),
    )

    fake_users_db.append(new_user)
    return True


def encrypt_password(password: str):
    return hasher.hash(password)


def delete_user(username: str) -> bool:
    if not is_exist(username):
        return False

    fake_users_db.remove(get_user(username))
    return True
