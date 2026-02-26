from typing import Annotated

from fastapi import Depends

import settings
from services.dynamodb import DynamoDBService


def _get_dynamodb_service(table_name: str):
    async def _dependency():
        yield DynamoDBService(dynamo_table=table_name)

    return _dependency


WhiteListDynamoDBServiceDep = Annotated[
    DynamoDBService, Depends(_get_dynamodb_service(table_name=settings.TOKEN_WHITE_LIST_TABLE))
]
