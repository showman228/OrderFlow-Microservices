from datetime import UTC, datetime

from notification_service.app.schemas.order import OrderItemResponse, OrderResponse


def seed_order() -> OrderResponse:
    return OrderResponse(
        id=12,
        user_id=7,
        status="pending",
        total_price=200.0,
        created_at=datetime(2026, 11, 28, tzinfo=UTC),
        items=[
            OrderItemResponse(
                id=1,
                product_id=3,
                product_name="Клавиатура",
                order_id=12,
                quantity=2,
                price=100.0,
            )
        ],
    )
