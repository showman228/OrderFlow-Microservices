from sqlalchemy.ext.asyncio import AsyncSession

from order_service.app.models import Order, OrderItem

DEFAULT_ORDER_STATUS = "pending"


async def seed_orders(db: AsyncSession, count: int = 3) -> list[Order]:
    """Создаёт несколько заказов (со снапшотами товаров) и возвращает их.

    OrderItem хранит снапшот товара (product_id/product_name/price/quantity),
    FK на внешние сервисы нет, поэтому сидинг самодостаточен.
    """
    orders: list[Order] = []
    for i in range(count):
        items = [
            OrderItem(
                product_id=i + 1,
                product_name=f"Product-{i + 1}",
                quantity=i + 1,
                price=float(1000 + i + 1),
            )
        ]
        orders.append(
            Order(
                user_id=i + 1,
                status=DEFAULT_ORDER_STATUS,
                total_price=sum(item.price * item.quantity for item in items),
                items=items,
            )
        )

    db.add_all(orders)
    await db.commit()

    for order in orders:
        await db.refresh(order)

    return orders
