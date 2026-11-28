from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from json import dumps
from typing import cast

import pytest
import pytest_asyncio
from aio_pika.abc import AbstractIncomingMessage
from httpx import ASGITransport, AsyncClient, MockTransport, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from notification_service.app import consumer as consumer_module
from notification_service.app.api_clients.order_client import OrderClient
from notification_service.app.consumer import NotificationConsumer
from notification_service.app.database import Base, get_db
from notification_service.app.deps import get_order_client
from notification_service.app.main import app
from notification_service.app.schemas.order import OrderResponse
from tests.db import create_test_session_factory, reset_schema
from tests.notification_service.seed import seed_order

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@127.0.0.1:5440/notification_test"


class EventDelivery:
    """Подменяет доставку брокера; обработчик и все записи в БД остаются реальными."""

    def __init__(self, routing_key: str, order_id: int, user_id: int, amount: float) -> None:
        self.routing_key = routing_key
        self.body = dumps({"order_id": order_id, "user_id": user_id, "amount": amount}).encode()

    @asynccontextmanager
    async def process(self) -> AsyncIterator[None]:
        yield


@pytest.fixture
def order() -> OrderResponse:
    return seed_order()


@pytest_asyncio.fixture
async def sessions() -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    engine, factory = create_test_session_factory(TEST_DATABASE_URL)
    try:
        await reset_schema(engine, Base)
        yield factory
    finally:
        await engine.dispose()


@pytest_asyncio.fixture
async def order_client(order: OrderResponse) -> AsyncIterator[OrderClient]:
    def respond(request: Request) -> Response:
        assert request.method == "GET"
        assert request.url.path == f"/orders/{order.id}"
        return Response(200, json=order.model_dump(mode="json"))

    async with AsyncClient(
        transport=MockTransport(respond), base_url="http://order.test"
    ) as client:
        yield OrderClient(client)


@pytest_asyncio.fixture
async def client(
    sessions: async_sessionmaker[AsyncSession], order_client: OrderClient
) -> AsyncIterator[AsyncClient]:
    async def override_get_db() -> AsyncIterator[AsyncSession]:
        async with sessions() as session:
            yield session

    def override_order_client() -> OrderClient:
        return order_client

    overrides = app.dependency_overrides.copy()
    app.dependency_overrides.update(
        {get_db: override_get_db, get_order_client: override_order_client}
    )
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            yield client
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(overrides)


@pytest.fixture
def consumer(
    sessions: async_sessionmaker[AsyncSession],
    order_client: OrderClient,
    monkeypatch: pytest.MonkeyPatch,
) -> NotificationConsumer:
    monkeypatch.setattr(consumer_module, "SessionLocal", sessions)
    return NotificationConsumer(
        url="amqp://rabbit.test",
        exchange_name="order.events",
        queue_name="notification.orders",
        routing_keys=["order.created", "order.paid"],
        order_client=order_client,
    )


@pytest.fixture
def deliver_event(
    consumer: NotificationConsumer,
) -> Callable[[str, int, int, float], Awaitable[None]]:
    async def deliver(routing_key: str, order_id: int, user_id: int, amount: float) -> None:
        delivery = EventDelivery(routing_key, order_id, user_id, amount)
        await consumer._on_message(cast(AbstractIncomingMessage, delivery))

    return deliver
