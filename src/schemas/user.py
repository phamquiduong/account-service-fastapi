from pydantic import BaseModel, EmailStr

from schemas.fields.password import PasswordField


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: PasswordField
