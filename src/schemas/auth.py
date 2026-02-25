from pydantic import BaseModel, EmailStr

from schemas.fields.password import PasswordField


class LoginRequestSchema(BaseModel):
    email: EmailStr
    password: PasswordField


class ChangePasswordRequestSchema(BaseModel):
    current_password: PasswordField
    new_password: PasswordField


class VerifyTokenRequestSchema(BaseModel):
    access_token: str


class RefreshTokenRequestSchema(BaseModel):
    refresh_token: str
