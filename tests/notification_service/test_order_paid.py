from collections.abc import Awaitable, Callable

import pytest
from httpx import AsyncClient

from notification_service.app.schemas.order import OrderResponse


@pytest.mark.asyncio
async def test_order_paid_adds_notification_with_event_amount_to_user_history(
    client: AsyncClient,
    deliver_event: Callable[[str, int, int, float], Awaitable[None]],
    order: OrderResponse,
) -> None:
    # Отличается от стоимости заказа, чтобы проверить именно сумму из события.
    await deliver_event("order.paid", order.id, order.user_id, 189.5)

    response = await client.get(f"/notifications/users/{order.user_id}")

    assert response.status_code == 200
    notification, = response.json()
    assert notification["order_id"] == order.id
    assert notification["user_id"] == order.user_id
    assert notification["status"] == "paid"
    assert notification["total_price"] == 189.5
    assert "189.50" in notification["message"]
