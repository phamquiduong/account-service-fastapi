from pydantic import BaseModel, EmailStr

from schemas.fields.password import PasswordField


class UserCreateRequestSchema(BaseModel):
    email: EmailStr
    password: PasswordField
