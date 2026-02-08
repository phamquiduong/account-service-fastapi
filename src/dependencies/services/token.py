from typing import Annotated

from fastapi import Depends

import settings
from services.token import TokenService


async def _get_token_service():
    yield TokenService(
        secret_key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
        access_token_exp=settings.ACCESS_TOKEN_EXPIRE,
        refresh_token_exp=settings.REFRESH_TOKEN_EXPIRE,
    )


TokenServiceDep = Annotated[TokenService, Depends(_get_token_service)]
