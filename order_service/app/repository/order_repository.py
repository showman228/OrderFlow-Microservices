from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from order_service.app.models.order import Order
from order_service.app.models.order_item import OrderItem
from order_service.app.schemas.order import OrderCreate, OrderUpdate
from typing import List


class OrderRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, order_id: int) -> Order | None:
        order = await self.db.execute(select(Order).where(Order.id == order_id))
        return order.scalars().one_or_none()

    async def get_all(self) -> List[Order]:
        orders = await self.db.execute(select(Order))
        return orders.scalars().all()

    async def get_by_user_id(self, user_id: int) -> List[Order]:
        orders = await self.db.execute(select(Order).where(Order.user_id == user_id))
        return orders.scalars().all()

    async def get_by_status(self, status: str) -> List[Order]:
        orders = await self.db.execute(select(Order).where(Order.status == status))
        return orders.scalars().all()

    async def create(self, order_data: OrderCreate) -> Order:
        total_price = sum(item.price * item.quantity for item in order_data.items)
        order = Order(
            user_id=order_data.user_id,
            status="pending",
            total_price=total_price,
        )

        self.db.add(order)
        await self.db.flush()

        for item in order_data.items:
            self.db.add(
                OrderItem(
                    product_id=item.product_id,
                    product_name=item.product_name,
                    quantity=item.quantity,
                    price=item.price,
                    order_id=order.id,
                )
            )

        await self.db.commit()
        await self.db.refresh(order)
        return order

    async def update(self, order_id: int, order_data: OrderUpdate) -> Order | None:
        order = await self.get_by_id(order_id)

        if not order:
            return None

        for field, value in order_data.model_dump(exclude_unset=True).items():
            setattr(order, field, value)

        await self.db.commit()
        await self.db.refresh(order)
        return order

    async def delete(self, order_id: int) -> bool:
        order = await self.get_by_id(order_id)
        if not order:
            return False

        await self.db.delete(order)
        await self.db.commit()
        return True
