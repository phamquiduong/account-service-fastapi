from functools import wraps

from fastapi import HTTPException, status

import settings
from constants.server import Environment


def protect_response(view):
    @wraps(view)
    async def inner(*args, **kwargs):
        try:
            return await view(*args, **kwargs)
        except HTTPException as http_exc:
            if settings.ENVIRONMENT == Environment.PRODUCTION:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request") from http_exc
            raise

    return inner
