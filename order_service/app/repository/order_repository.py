from venv import create

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from order_service.app.models.order import Order
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

    # Дописать
    async def create(self, order_data: OrderCreate) -> Order | None:
        order = Order(
                user_id=order_data.user_id,
                status=order_data.status,
                total_price=order_data.total_price,
            )
    async def update(self, order_data: OrderUpdate) -> Order:
        pass


    async def delete(self, order_id: int) -> bool:
        pass
