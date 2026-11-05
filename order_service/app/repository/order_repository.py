from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from order_service.app.models.order import Order
from order_service.app.models.order_item import OrderItem
from order_service.app.schemas.order import OrderUpdate
from order_service.app.schemas.order_item import OrderItemCreate


class OrderRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, order_id: int) -> Order | None:
        order = await self.db.execute(
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.id == order_id)
        )
        return order.scalars().one_or_none()

    async def get_all(self) -> list[Order]:
        orders = await self.db.execute(select(Order).options(selectinload(Order.items)))
        return orders.scalars().all()

    async def get_by_user_id(self, user_id: int) -> list[Order]:
        orders = await self.db.execute(
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.user_id == user_id)
        )
        return orders.scalars().all()

    async def get_by_status(self, order_status: str) -> list[Order]:
        orders = await self.db.execute(
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.status == order_status)
        )
        return orders.scalars().all()

    async def create(
        self,
        user_id: int,
        total_price: float,
        items: list[OrderItemCreate],
    ) -> Order:
        order = Order(
            user_id=user_id,
            status="pending",
            total_price=total_price,
            items=[
                OrderItem(
                    product_id=item.product_id,
                    product_name=item.product_name,
                    quantity=item.quantity,
                    price=item.price,
                )
                for item in items
            ],
        )

        self.db.add(order)
        await self.db.commit()
        return order

    async def update(self, order_id: int, order_data: OrderUpdate) -> Order | None:
        order = await self.get_by_id(order_id)

        if order is None:
            return None

        for field, value in order_data.model_dump(exclude_unset=True).items():
            setattr(order, field, value)

        await self.db.commit()
        return order

    async def delete(self, order_id: int) -> bool:
        order = await self.get_by_id(order_id)
        if not order:
            return False

        await self.db.delete(order)
        await self.db.commit()
        return True
