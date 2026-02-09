from pydantic import BaseModel


class FieldError(BaseModel):
    name: str
    message: str


class ErrorResponse(BaseModel):
    status: int
    message: str
    error_fields: list[FieldError] | None = None
