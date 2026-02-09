from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from jwt.exceptions import InvalidTokenError

from errors.api_exception import APIException
from schemas.error import ErrorResponse, FieldError


async def _invalid_token_error_handler(_: Request, exc: InvalidTokenError):
    err_res = ErrorResponse(status=status.HTTP_400_BAD_REQUEST, message=str(exc))
    return JSONResponse(err_res.model_dump(exclude_none=True), status_code=err_res.status)


async def _validation_error_handler(_: Request, exc: RequestValidationError):
    error_fields = [FieldError(name=error["loc"][-1], message=error["msg"]) for error in exc.errors()]
    err_res = ErrorResponse(status=status.HTTP_422_UNPROCESSABLE_ENTITY, message="Invalid", error_fields=error_fields)
    return JSONResponse(err_res.model_dump(exclude_none=True), status_code=err_res.status)


async def _api_exception_handler(_: Request, exc: APIException):
    error_fields = [FieldError(name=field, message=msg) for field, msg in exc.fields.items()]
    err_res = ErrorResponse(status=exc.status_code, message=exc.detail, error_fields=error_fields)
    return JSONResponse(err_res.model_dump(exclude_none=True), status_code=err_res.status, headers=exc.headers)


async def _http_exception_handler(_: Request, exc: HTTPException):
    err_res = ErrorResponse(status=exc.status_code, message=exc.detail)
    return JSONResponse(err_res.model_dump(exclude_none=True), status_code=err_res.status, headers=exc.headers)


async def _exception_handler(_: Request, __: Exception):
    err_res = ErrorResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Internal server error")
    return JSONResponse(err_res.model_dump(exclude_none=True), status_code=err_res.status)


def handle_error(app: FastAPI):
    app.add_exception_handler(InvalidTokenError, _invalid_token_error_handler)
    app.add_exception_handler(RequestValidationError, _validation_error_handler)
    app.add_exception_handler(APIException, _api_exception_handler)
    app.add_exception_handler(HTTPException, _http_exception_handler)
    app.add_exception_handler(Exception, _exception_handler)
