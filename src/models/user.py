import uuid

from pwdlib import PasswordHash
from pydantic.main import BaseModel
from sqlalchemy import Column, String

from src.database import Base

from .token import create_access_token

hasher = PasswordHash.recommended()


class UserDTO(BaseModel):
    name: str
    password: str


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    def verify_password(self, plain_password: str) -> bool:
        return hasher.verify(plain_password, str(self.password))

    async def gen_token(self) -> str | None:
        (token, success) = await create_access_token({"name": self.name, "id": self.id})

        return token if success else None


fake_users_db: list[User] = []


def encrypt_password(password: str):
    return hasher.hash(password)
