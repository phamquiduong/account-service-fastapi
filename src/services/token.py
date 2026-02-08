from datetime import timedelta

import jwt

from models.user import User
from schemas.token import AccessTokenPayloadSchema, RefreshTokenPayloadSchema, TokenPayloadSchema


class JWTService:
    def __init__(self, secret_key: str, algorithm: str) -> None:
        self._secret_key = secret_key
        self._algorithm = algorithm

    def create_token(self, payload: dict) -> str:
        return jwt.encode(payload=payload, key=self._secret_key, algorithm=self._algorithm)

    def get_payload(self, token: str) -> dict:
        return jwt.decode(jwt=token, key=self._secret_key, algorithms=[self._algorithm])


class TokenService(JWTService):
    def __init__(
        self, secret_key: str, algorithm: str, access_token_exp: timedelta, refresh_token_exp: timedelta
    ) -> None:
        super().__init__(secret_key, algorithm)
        self._access_token_exp = access_token_exp
        self._refresh_token_exp = refresh_token_exp

    def create_access_token(self, user: User) -> str:
        access_token_payload = AccessTokenPayloadSchema.from_user(user=user, exp=self._access_token_exp)
        return self.create_token(access_token_payload.model_dump())

    def create_refresh_token(self, user: User) -> str:
        refresh_token_payload = RefreshTokenPayloadSchema.from_user(user=user, exp=self._refresh_token_exp)
        return self.create_token(refresh_token_payload.model_dump())

    def get_token_payload(self, token: str) -> TokenPayloadSchema:
        return TokenPayloadSchema.model_validate(self.get_payload(token))
