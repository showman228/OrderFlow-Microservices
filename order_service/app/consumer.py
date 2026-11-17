# получаем из payment_service/producer статус оплаты и присваиваем его к статусу заказа

import logging

import aio_pika
from aio_pika import ExchangeType
from aio_pika.abc import AbstractIncomingMessage, AbstractRobustConnection
from pydantic import BaseModel, ValidationError

from order_service.app.cache.redis import RedisCache
from order_service.app.database import SessionLocal
from order_service.app.models.order import Order, PaymentStatus
from order_service.app.repository.order_repository import OrderRepository
from order_service.app.schemas.order import OrderUpdate
from order_service.app.services.order_services import ORDER_CACHE_KEY, USER_ORDERS_CACHE_KEY

logger = logging.getLogger(__name__)


class PaymentEvent(BaseModel):
    order_id: int
    status: PaymentStatus
    user_id: int
    amount: float


class PaymentConsumer:

    def __init__(
        self,
        url: str,
        exchange_name: str,
        queue_name: str,
        routing_keys: list[str],
        cache: RedisCache,
    ) -> None:
        self._url = url
        self._exchange_name = exchange_name
        self._queue_name = queue_name
        self._routing_keys = routing_keys
        self._cache = cache
        self._connection: AbstractRobustConnection | None = None

    async def connect(self) -> None:
        self._connection = await aio_pika.connect_robust(self._url)
        channel = await self._connection.channel()
        # тип exchange (DIRECT) и параметры должны совпадать с PaymentProducer
        exchange = await channel.declare_exchange(self._exchange_name, ExchangeType.DIRECT)
        queue = await channel.declare_queue(self._queue_name, durable=True)
        for routing_key in self._routing_keys:
            await queue.bind(exchange, routing_key=routing_key)
        await queue.consume(self._on_message)

    async def close(self) -> None:
        if self._connection is not None:
            await self._connection.close()

    async def _on_message(self, message: AbstractIncomingMessage) -> None:
        async with message.process():
            try:
                event = PaymentEvent.model_validate_json(message.body)
            except ValidationError:
                logger.warning("Invalid payment event: %s", message.body)
                return

            async with SessionLocal() as session:
                repository = OrderRepository(session)
                updated = await repository.update(
                    event.order_id, OrderUpdate(status=event.status.value)
                )

            if updated is None:
                logger.warning("Order %s not found, skip payment event", event.order_id)
                return

            await self._invalidate_cache(updated)

    async def _invalidate_cache(self, order: Order) -> None:
        await self._cache.delete(ORDER_CACHE_KEY.format(order_id=order.id))
        await self._cache.delete(USER_ORDERS_CACHE_KEY.format(user_id=order.user_id))
