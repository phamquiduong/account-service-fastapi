from typing import Annotated

from fastapi import Depends

import settings
from services.dynamodb import DynamoDBService


async def _get_white_list_dynamodb_service():
    yield DynamoDBService(dynamo_table=settings.TOKEN_WHITE_LIST_TABLE)


WhiteListDynamoDBServiceDep = Annotated[DynamoDBService, Depends(_get_white_list_dynamodb_service)]
