from typing import Annotated

from fastapi import Depends

from dependencies.database import SessionDep
from repositories.user import UserRepository


async def _get_user_repository(session: SessionDep):
    yield UserRepository(session=session)


UserRepositoryDep = Annotated[UserRepository, Depends(_get_user_repository)]
