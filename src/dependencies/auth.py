from typing import Annotated

from fastapi import Depends, status

from constants.token import TokenType
from dependencies.services.token import TokenServiceDep
from errors.api_exception import APIException
from schemas.token import TokenPayloadSchema, oauth2_scheme


async def _get_auth_token_payload(
    token_service: TokenServiceDep, token: Annotated[str, Depends(oauth2_scheme)]
) -> TokenPayloadSchema:
    token_payload = token_service.get_token_payload(token)

    if token_payload.token_type != TokenType.ACCESS:
        raise APIException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token required")

    return token_payload


AuthTokenPayloadDep = Annotated[TokenPayloadSchema, Depends(_get_auth_token_payload)]
