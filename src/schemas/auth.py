from pydantic import BaseModel, EmailStr

from schemas.fields.password import PasswordField


class LoginSchema(BaseModel):
    email: EmailStr
    password: PasswordField
