import logging
import uuid
from datetime import datetime
from typing import Any

import boto3

logger = logging.getLogger()


class DynamoDBService:
    class _Encoder:
        def default(self, obj: Any):
            if isinstance(obj, uuid.UUID):
                return str(obj)
            if isinstance(obj, datetime):
                return int(obj.timestamp())
            return obj

    def __init__(self, dynamo_table: str) -> None:
        self._dynamodb = boto3.resource("dynamodb")
        self._table = self._dynamodb.Table(dynamo_table)  # type:ignore
        self._encoder = self._Encoder()

    def add_item(self, item: dict[str, Any]) -> None:
        item = {key: self._encoder.default(value) for key, value in item.items()}
        self._table.put_item(Item=item)

    def get_item(self, key: dict[str, Any]) -> dict | None:
        response = self._table.get_item(Key=key)
        item = response.get("Item")
        if not item:
            logger.error("No data found with key: %s", key)
            return None
        return item

    def update(self, key: dict[str, Any], **update_data):
        expression = "SET " + " , ".join(f"#update_{key} = :update_{key}" for key in update_data)

        expression_names = {f"#update_{key}": key for key in update_data}
        expression_values = {f":update_{key}": value for key, value in update_data.items()}

        self._table.update_item(
            Key=key,
            UpdateExpression=expression,
            ExpressionAttributeNames=expression_names,
            ExpressionAttributeValues=expression_values,
        )
