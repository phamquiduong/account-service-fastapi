from pydantic import EmailStr
from sqlmodel import Session, select, update

from models.user import User
from schemas.user import UserCreateSchema
from services.password import PasswordService


class UserService:
    def __init__(self, session: Session, password_service: PasswordService) -> None:
        self._session = session
        self._password_service = password_service

    async def create(self, user_create: UserCreateSchema) -> User:
        user = User(email=user_create.email, password=user_create.password)
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)
        return user

    async def get_by_email(self, email: EmailStr) -> User | None:
        return self._session.exec(select(User).where(User.email == email)).first()

    async def get_by_id(self, user_id: int) -> User | None:
        return self._session.exec(select(User).where(User.id == user_id)).first()

    async def verify_password(self, user: User, current_password) -> bool:
        return self._password_service.verify_password(plain_password=current_password, hashed_password=user.password)

    async def update_password(self, user_id: int, new_password: str) -> None:
        new_password_hashed = self._password_service.get_password_hash(new_password)
        self._session.exec(update(User).where(User.id == user_id).values({User.password: new_password_hashed}))
        self._session.commit()
