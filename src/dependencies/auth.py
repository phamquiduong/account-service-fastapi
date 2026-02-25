from typing import Annotated

from fastapi import Depends, status

from constants.token import TokenType
from dependencies.services.token import TokenServiceDep
from dependencies.services.user import UserServiceDep
from errors.api_exception import APIException
from models.user import User
from schemas.token import TokenPayloadSchema, oauth2_scheme


async def _get_auth_token_payload(
    token_service: TokenServiceDep, token: Annotated[str, Depends(oauth2_scheme)]
) -> TokenPayloadSchema:
    token_payload = token_service.get_token_payload(token)
    if token_payload.token_type != TokenType.ACCESS:
        raise APIException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token required")
    return token_payload


AuthTokenPayloadDep = Annotated[TokenPayloadSchema, Depends(_get_auth_token_payload)]


async def _get_auth_user(user_service: UserServiceDep, auth_token_payload: AuthTokenPayloadDep):
    user = await user_service.get_by_id(int(auth_token_payload.sub))
    if not user:
        raise APIException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
    return user


AuthUserDep = Annotated[User, Depends(_get_auth_user)]
