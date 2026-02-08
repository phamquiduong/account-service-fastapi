from pydantic import EmailStr
from sqlmodel import Field

from models.base import TimestampMixin
from schemas.fields.password import PasswordField


class User(TimestampMixin, table=True):
    id: int | None = Field(primary_key=True, default=None)
    email: EmailStr = Field(index=True, unique=True)
    password: PasswordField

    __tablename__: str = "users"
