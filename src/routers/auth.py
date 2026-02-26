from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from constants.token import TokenType
from decorators.security import protect_response
from dependencies.services.token import TokenServiceDep
from dependencies.services.user import UserServiceDep
from dependencies.services.white_list import WhiteListServiceDep
from errors.api_exception import APIException
from schemas.auth import LoginRequestSchema, RefreshTokenRequestSchema, VerifyTokenRequestSchema
from schemas.token import OAuth2TokenSchema, TokenDetailResponse, TokenPayloadSchema, TokenResponse

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/login")
@protect_response
async def login(
    user_service: UserServiceDep,
    token_service: TokenServiceDep,
    white_list_service: WhiteListServiceDep,
    login_request: LoginRequestSchema,
) -> TokenResponse:
    user = await user_service.get_by_email(login_request.email)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not await user_service.verify_password(user=user, current_password=login_request.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is incorrect")

    access_token_payload = token_service.create_access_token_payload(user)
    refresh_token_payload = token_service.create_refresh_token_payload(user)

    await white_list_service.create(refresh_token_payload)

    return TokenResponse(
        access=TokenDetailResponse(
            token=token_service.create_access_token(access_token_payload),
            payload=access_token_payload,
        ),
        refresh=TokenDetailResponse(
            token=token_service.create_refresh_token(refresh_token_payload),
            payload=refresh_token_payload,
        ),
    )


@auth_router.post("/token", include_in_schema=False)
async def login_for_access_token(
    user_service: UserServiceDep,
    token_service: TokenServiceDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> OAuth2TokenSchema:
    user = await user_service.get_by_email(form_data.username)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not await user_service.verify_password(user=user, current_password=form_data.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is incorrect")

    access_token_payload = token_service.create_access_token_payload(user)
    access_token = token_service.create_access_token(access_token_payload)

    return OAuth2TokenSchema(access_token=access_token, token_type="bearer")


@auth_router.post("/verify")
async def verify(token_service: TokenServiceDep, verify_token_request: VerifyTokenRequestSchema) -> TokenPayloadSchema:
    return token_service.get_token_payload(verify_token_request.access_token)


@auth_router.post("/refresh")
async def refresh_token(
    user_service: UserServiceDep,
    token_service: TokenServiceDep,
    white_list_service: WhiteListServiceDep,
    refresh_token_request: RefreshTokenRequestSchema,
) -> TokenResponse:
    token_payload = token_service.get_token_payload(refresh_token_request.refresh_token)

    if token_payload.token_type != TokenType.REFRESH:
        raise APIException(status_code=status.HTTP_400_BAD_REQUEST, detail="Refresh token required")

    if not await white_list_service.is_exist(token_payload=token_payload):
        raise APIException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token was revoked")

    user = await user_service.get_by_id(int(token_payload.sub))
    if not user:
        raise APIException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

    access_token_payload = token_service.create_access_token_payload(user)
    refresh_token_payload = token_service.create_refresh_token_payload(user)

    await white_list_service.delete(refresh_token_payload)
    await white_list_service.create(refresh_token_payload)

    return TokenResponse(
        access=TokenDetailResponse(
            token=token_service.create_access_token(access_token_payload),
            payload=access_token_payload,
        ),
        refresh=TokenDetailResponse(
            token=token_service.create_refresh_token(refresh_token_payload),
            payload=refresh_token_payload,
        ),
    )
