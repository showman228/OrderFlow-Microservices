from enum import StrEnum

import aio_pika
from aio_pika import ExchangeType
from aio_pika.abc import AbstractIncomingMessage, AbstractRobustConnection
from pydantic import BaseModel, ValidationError, Field

from notification_service.app.services.notification_services import NotificationService
from notification_service.app.api_clients.order_client import OrderClient
from notification_service.app.database import SessionLocal

class OrderEvent(BaseModel):
    user_id: int = Field(ge=1)
    order_id: int = Field(ge=1)
    amount: float = Field(ge=0, allow_inf_nan=False)

class OrderRoutingKey(StrEnum):
    CREATED = "order.created"
    PAID = "order.paid"

class NotificationConsumer:
    def __init__(self, url: str, exchange_name: str, queue_name: str, routing_keys: list[str], order_client: OrderClient):
        self._url = url
        self._exchange_name = exchange_name
        self._queue_name = queue_name
        self._routing_keys = routing_keys
        self._order_client = order_client
        self._connection: AbstractRobustConnection | None = None

    async def connect(self) -> None:
        self._connection = await aio_pika.connect_robust(self._url)
        channel = await self._connection.channel()
        exchange = await channel.declare_exchange(self._exchange_name, ExchangeType.DIRECT)
        queue = await channel.declare_queue(self._queue_name, durable=True)
        for routing_key in self._routing_keys:
            await queue.bind(exchange, routing_key)
        await queue.consume(self._on_message)

    async def _on_message(self, message: AbstractIncomingMessage) -> None:
        async with message.process():
            routing_key = OrderRoutingKey(message.routing_key)
            event = OrderEvent.model_validate_json(message.body)

            async with SessionLocal() as session:
                service = NotificationService(
                    order_client=self._order_client,
                    db=session,
                )

                if routing_key == OrderRoutingKey.CREATED:
                    await service.create_order_created_notification(
                        order_id=event.order_id,
                        user_id=event.user_id,
                        amount=event.amount,
                    )
                elif routing_key == OrderRoutingKey.PAID:
                    await service.create_notification_for_pay(
                        order_id=event.order_id,
                        user_id=event.user_id,
                        amount=event.amount,
                    )

    async def close(self) -> None:
        if self._connection is not None:
            await self._connection.close()