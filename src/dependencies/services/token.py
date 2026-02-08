from typing import Annotated

from fastapi import Depends

from services.token import TokenService
from settings import ACCESS_TOKEN_EXPIRE, ALGORITHM, REFRESH_TOKEN_EXPIRE, SECRET_KEY


async def _get_token_service():
    yield TokenService(
        secret_key=SECRET_KEY,
        algorithm=ALGORITHM,
        access_token_exp=ACCESS_TOKEN_EXPIRE,
        refresh_token_exp=REFRESH_TOKEN_EXPIRE,
    )


TokenServiceDep = Annotated[TokenService, Depends(_get_token_service)]
