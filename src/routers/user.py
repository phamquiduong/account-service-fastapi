from fastapi import APIRouter, HTTPException, status

from decorators.security import protect_response
from dependencies.auth import AuthTokenPayloadDep
from dependencies.repositories.user import UserRepositoryDep
from dependencies.services.password import PasswordServiceDep
from errors.api_exception import APIException
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


@user_router.get("/me")
async def get_current_user_info(user_repository: UserRepositoryDep, auth_token_payload: AuthTokenPayloadDep) -> User:
    user = await user_repository.get_by_id(int(auth_token_payload.sub))

    if not user:
        raise APIException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

    return user
