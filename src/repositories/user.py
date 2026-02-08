from pydantic import EmailStr
from sqlmodel import Session, select

from models.user import User
from schemas.user import UserCreateSchema


class UserRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    async def create(self, user_create: UserCreateSchema) -> User:
        user = User(email=user_create.email, password=user_create.password)
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)
        return user

    async def get_by_email(self, email: EmailStr) -> User | None:
        return self._session.exec(select(User).where(User.email == email)).first()
