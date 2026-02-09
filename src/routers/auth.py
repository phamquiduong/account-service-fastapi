from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from constants.token import TokenType
from decorators.security import protect_response
from dependencies.repositories.user import UserRepositoryDep
from dependencies.services.dynamodb import WhiteListDynamoDBServiceDep
from dependencies.services.password import PasswordServiceDep
from dependencies.services.token import TokenServiceDep
from errors.api_exception import APIException
from schemas.auth import LoginSchema
from schemas.token import OAuth2TokenSchema, TokenPayloadSchema, TokenResponse

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/login")
@protect_response
async def login(
    user_repository: UserRepositoryDep,
    password_service: PasswordServiceDep,
    token_service: TokenServiceDep,
    white_list_dynamodb_service: WhiteListDynamoDBServiceDep,
    login_schema: LoginSchema,
) -> TokenResponse:
    user = await user_repository.get_by_email(login_schema.email)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not password_service.verify_password(plain_password=login_schema.password, hashed_password=user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is incorrect")

    access_token_payload = token_service.create_access_token_payload(user)
    refresh_token_payload = token_service.create_refresh_token_payload(user)

    white_list_dynamodb_service.add_item(refresh_token_payload.model_dump())

    return TokenResponse(
        access_token=token_service.create_access_token(access_token_payload),
        refresh_token=token_service.create_refresh_token(refresh_token_payload),
    )


@auth_router.post("/token", include_in_schema=False)
async def login_for_access_token(
    user_repository: UserRepositoryDep,
    password_service: PasswordServiceDep,
    token_service: TokenServiceDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> OAuth2TokenSchema:
    user = await user_repository.get_by_email(form_data.username)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not password_service.verify_password(plain_password=form_data.password, hashed_password=user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is incorrect")

    access_token_payload = token_service.create_access_token_payload(user)
    access_token = token_service.create_access_token(access_token_payload)

    return OAuth2TokenSchema(access_token=access_token, token_type="bearer")


@auth_router.post("/verify")
async def verify(token_service: TokenServiceDep, token: str = Body()) -> TokenPayloadSchema:
    return token_service.get_token_payload(token)


@auth_router.post("/refresh")
async def refresh_token(
    user_repository: UserRepositoryDep,
    token_service: TokenServiceDep,
    white_list_dynamodb_service: WhiteListDynamoDBServiceDep,
    token: str = Body(),
) -> TokenResponse:
    token_payload = token_service.get_token_payload(token)

    if token_payload.token_type != TokenType.REFRESH:
        raise APIException(status_code=status.HTTP_400_BAD_REQUEST, detail="Refresh token required")

    if not white_list_dynamodb_service.get_item({"sub": token_payload.sub, "jti": token_payload.jti}):
        raise APIException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token was revoked")

    user = await user_repository.get_by_id(int(token_payload.sub))
    if not user:
        raise APIException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

    access_token_payload = token_service.create_access_token_payload(user)
    refresh_token_payload = token_service.create_refresh_token_payload(user)

    white_list_dynamodb_service.delete({"sub": token_payload.sub, "jti": token_payload.jti})
    white_list_dynamodb_service.add_item(refresh_token_payload.model_dump())

    return TokenResponse(
        access_token=token_service.create_access_token(access_token_payload),
        refresh_token=token_service.create_refresh_token(refresh_token_payload),
    )
