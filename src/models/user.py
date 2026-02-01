from pydantic import EmailStr
from sqlmodel import Field

from models.base import TimestampMixin


class User(TimestampMixin):
    id: int = Field(primary_key=True)
    email: EmailStr = Field(index=True, unique=True)
    password: str = Field()

    __tablename__: str = "users"
