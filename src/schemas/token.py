import uuid
from datetime import datetime, timedelta, timezone

from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field

from constants.token import TokenType
from models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


class OAuth2TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenPayloadSchema(BaseModel):
    sub: str
    token_type: TokenType | None = None
    iat: datetime
    exp: datetime
    jti: uuid.UUID = Field(default_factory=uuid.uuid4)

    @classmethod
    def from_user(cls, user: User, exp: timedelta):
        time_now = datetime.now(timezone.utc)
        return cls(
            sub=str(user.id),
            iat=time_now,
            exp=time_now + exp,
        )


class AccessTokenPayloadSchema(TokenPayloadSchema):
    token_type: TokenType = TokenType.ACCESS


class RefreshTokenPayloadSchema(TokenPayloadSchema):
    token_type: TokenType = TokenType.REFRESH


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
