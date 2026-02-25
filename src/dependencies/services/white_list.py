from typing import Annotated

from fastapi import Depends

from dependencies.services.dynamodb import WhiteListDynamoDBServiceDep
from services.white_list import WhiteListService


async def _get_white_list_service(dynamodb_service: WhiteListDynamoDBServiceDep):
    yield WhiteListService(dynamodb_service=dynamodb_service)


WhiteListServiceDep = Annotated[WhiteListService, Depends(_get_white_list_service)]
