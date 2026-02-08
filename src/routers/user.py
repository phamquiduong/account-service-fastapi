from fastapi import APIRouter, HTTPException, status

from decorators.security import protect_response
from dependencies.repositories.user import UserRepositoryDep
from dependencies.services.password import PasswordServiceDep
from models.user import User
from schemas.user import UserCreateSchema

user_router = APIRouter(prefix="/users", tags=["User"])


@user_router.post("", status_code=status.HTTP_201_CREATED)
@protect_response
async def register(
    user_repository: UserRepositoryDep, password_service: PasswordServiceDep, user_create: UserCreateSchema
) -> User:
    if await user_repository.get_by_email(user_create.email) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    user_create.password = password_service.get_password_hash(user_create.password)
    return await user_repository.create(user_create)
