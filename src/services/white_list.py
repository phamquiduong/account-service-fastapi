from schemas.token import TokenPayloadSchema
from services.dynamodb import DynamoDBService


class WhiteListService:
    def __init__(self, dynamodb_service: DynamoDBService) -> None:
        self._dynamodb_service = dynamodb_service

    async def create(self, token_payload: TokenPayloadSchema) -> None:
        self._dynamodb_service.add_item(token_payload.model_dump())

    async def get(self, token_payload: TokenPayloadSchema) -> dict | None:
        return self._dynamodb_service.get_item(self._get_dynamodb_key(token_payload))

    async def is_exist(self, token_payload: TokenPayloadSchema) -> bool:
        return await self.get(token_payload) is not None

    async def delete(self, token_payload: TokenPayloadSchema) -> None:
        return self._dynamodb_service.delete(self._get_dynamodb_key(token_payload))

    async def delete_by_user_id(self, user_id: str) -> None:
        self._dynamodb_service.delete_by_partition_key(partition_key="sub", partition_value=user_id, sorted_key="jti")

    @staticmethod
    def _get_dynamodb_key(token_payload: TokenPayloadSchema):
        return {"sub": token_payload.sub, "jti": token_payload.jti}
