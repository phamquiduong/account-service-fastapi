from fastapi import APIRouter, HTTPException, status

from decorators.security import protect_response
from dependencies.auth import AuthTokenPayloadDep, AuthUserDep
from dependencies.services.user import UserServiceDep
from dependencies.services.white_list import WhiteListServiceDep
from errors.api_exception import APIException
from models.user import User
from schemas.auth import ChangePasswordRequestSchema
from schemas.user import UserCreateRequestSchema

user_router = APIRouter(prefix="/users", tags=["User"])


@user_router.post("", status_code=status.HTTP_201_CREATED)
@protect_response
async def register(user_service: UserServiceDep, user_create_request: UserCreateRequestSchema) -> User:
    if await user_service.get_by_email(user_create_request.email) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    return await user_service.create(user_create_request)


@user_router.get("/me")
async def get_current_user_info(user: AuthUserDep) -> User:
    return user


@user_router.patch("/me/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_current_user_password(
    user_service: UserServiceDep,
    white_list_service: WhiteListServiceDep,
    auth_token_payload: AuthTokenPayloadDep,
    change_password_request: ChangePasswordRequestSchema,
) -> None:
    user_id = int(auth_token_payload.sub)
    user = await user_service.get_by_id(user_id)

    if not user:
        raise APIException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

    if not await user_service.verify_password(user=user, current_password=change_password_request.current_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is incorrect")

    await user_service.update_password(user_id=user_id, new_password=change_password_request.new_password)
    await white_list_service.delete_by_user_id(user_id=auth_token_payload.sub)
