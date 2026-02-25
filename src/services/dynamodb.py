import logging
import uuid
from datetime import datetime
from typing import Any

import boto3
from boto3.dynamodb.conditions import Key

logger = logging.getLogger()


class DynamoDBService:
    class _Encoder:
        def default(self, obj: Any):
            if isinstance(obj, uuid.UUID):
                return obj.bytes
            if isinstance(obj, datetime):
                return int(obj.timestamp())
            return obj

    def __init__(self, dynamo_table: str) -> None:
        self._dynamodb = boto3.resource("dynamodb")
        self._table = self._dynamodb.Table(dynamo_table)  # type:ignore
        self._encoder = self._Encoder()

    async def add_item(self, item: dict[str, Any]) -> None:
        item = {key: self._encoder.default(value) for key, value in item.items()}
        self._table.put_item(Item=item)

    async def get_item(self, key: dict[str, Any]) -> dict | None:
        key = {key: self._encoder.default(value) for key, value in key.items()}
        response = self._table.get_item(Key=key)
        item = response.get("Item")
        if not item:
            logger.error("No data found with key: %s", key)
            return None
        return item

    async def query_by_partition_key(self, partition_key: str, partition_value: Any) -> list[dict]:
        partition_value = self._encoder.default(partition_value)
        items: list[dict] = []
        last_key = None

        while True:
            kwargs = {"KeyConditionExpression": Key(partition_key).eq(partition_value)}
            if last_key:
                kwargs["ExclusiveStartKey"] = last_key

            response = self._table.query(**kwargs)
            items.extend(response.get("Items", []))

            last_key = response.get("LastEvaluatedKey")
            if not last_key:
                break

        return items

    async def update(self, key: dict[str, Any], **update_data):
        key = {key: self._encoder.default(value) for key, value in key.items()}
        update_data = {key: self._encoder.default(value) for key, value in update_data.items()}

        expression = "SET " + " , ".join(f"#update_{key} = :update_{key}" for key in update_data)

        expression_names = {f"#update_{key}": key for key in update_data}
        expression_values = {f":update_{key}": value for key, value in update_data.items()}

        self._table.update_item(
            Key=key,
            UpdateExpression=expression,
            ExpressionAttributeNames=expression_names,
            ExpressionAttributeValues=expression_values,
        )

    async def delete(self, key: dict[str, Any]):
        key = {key: self._encoder.default(value) for key, value in key.items()}
        self._table.delete_item(Key=key)

    async def delete_by_partition_key(self, partition_key: str, partition_value: Any, sorted_key: str):
        items = await self.query_by_partition_key(partition_key=partition_key, partition_value=partition_value)
        with self._table.batch_writer() as batch:
            for item in items:
                batch.delete_item(Key={partition_key: item[partition_key], sorted_key: item[sorted_key]})
