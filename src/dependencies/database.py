from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine

from settings import DB_URL

_engine = create_engine(DB_URL, pool_pre_ping=True)


async def _get_session():
    with Session(_engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(_get_session)]
