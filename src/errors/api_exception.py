from fastapi import HTTPException


class APIException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str,
        headers: dict[str, str] | None = None,
        fields: dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)
        self.fields = fields or {}

    def __str__(self) -> str:
        return f"Detail: {self.detail} - Fields: {self.fields}"
