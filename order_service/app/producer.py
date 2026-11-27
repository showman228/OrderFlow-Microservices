# create order и paid order передаем в notification эту информацию order_id user_id 

import json 

import aio_pika
from aio_pika.abc import AbstractExchange, AbstractRobustConnection

class OrderProducer:

    def __init__(self, url: str, exchange_name: str) -> None:
        self._url = url
        self._exchange_name = exchange_name
        self._connection: AbstractRobustConnection | None = None
        self._exchange: AbstractExchange | None = None

    async def connect(self) -> None:
        self._connection = await aio_pika.connect_robust(self._url)
        channel = await self._connection.channel()
        self._exchange = await channel.declare_exchange(self._exchange_name)

    async def publish(self, routing_key: str, data: dict) -> None:
        message = aio_pika.Message(json.dumps(data).encode())
        await self._exchange.publish(message, routing_key)

    async def close(self) -> None:
        if self._connection is not None:
            await self._connection.close()