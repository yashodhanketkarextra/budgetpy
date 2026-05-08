from sqlalchemy.orm import Session

from src.models.user import User, UserDTO, encrypt_password


async def get_all_users(db: Session) -> list[User]:
    return db.query(User).all()


async def get_user(db: Session, username: str) -> User:
    return db.query(User).filter(User.name == username).first()


async def create_user(db: Session, user_data: UserDTO) -> tuple[bool, str]:
    user = await get_user(db, user_data.name)
    if user:
        return False, "User already exists"

    db_user = User(
        name=user_data.name,
        password=encrypt_password(user_data.password),
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return True, "Success"


async def delete_user(db: Session, username: str) -> bool:
    user = await get_user(db, username)
    if not user:
        return False

    db.delete(user)
    db.commit()
    return True
