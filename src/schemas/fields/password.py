import re
from typing import Annotated

from pydantic import Field
from pydantic.functional_validators import AfterValidator
from pydantic_core import PydanticCustomError

PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,64}$")


def _validate_password(v: str) -> str:
    if not PASSWORD_REGEX.match(v):
        raise PydanticCustomError("Invalid", "invalid password")
    return v


PasswordField = Annotated[
    str,
    Field(
        title="Password",
        description="Strong password (8-64 chars, include uppercase, lowercase, number and special character)",
        min_length=8,
        max_length=64,
        examples=["P@ssw0rd123!"],
        json_schema_extra={
            "format": "password",
            "writeOnly": True,
        },
        exclude=True,
    ),
    AfterValidator(_validate_password),
]
