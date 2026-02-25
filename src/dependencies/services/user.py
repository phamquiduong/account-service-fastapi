from typing import Annotated

from fastapi import Depends

from dependencies.database import SessionDep
from dependencies.services.password import PasswordServiceDep
from services.user import UserService


async def _get_user_service(session: SessionDep, password_service: PasswordServiceDep):
    yield UserService(session=session, password_service=password_service)


UserServiceDep = Annotated[UserService, Depends(_get_user_service)]
