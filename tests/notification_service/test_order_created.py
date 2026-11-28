from collections.abc import Awaitable, Callable

import pytest
from httpx import AsyncClient

from notification_service.app.schemas.order import OrderResponse


@pytest.mark.asyncio
async def test_order_created_adds_notification_to_user_history(
    client: AsyncClient,
    deliver_event: Callable[[str, int, int, float], Awaitable[None]],
    order: OrderResponse,
) -> None:
    await deliver_event("order.created", order.id, order.user_id, order.total_price)

    response = await client.get(f"/notifications/users/{order.user_id}")

    assert response.status_code == 200
    notification, = response.json()
    assert notification["order_id"] == order.id
    assert notification["user_id"] == order.user_id
    assert notification["status"] == "created"
    assert notification["total_price"] == 200.0
    assert "Клавиатура x2" in notification["message"]
