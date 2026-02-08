from typing import Annotated

from fastapi import Depends

from services.password import PasswordService


async def _get_password_service():
    yield PasswordService()


PasswordServiceDep = Annotated[PasswordService, Depends(_get_password_service)]
