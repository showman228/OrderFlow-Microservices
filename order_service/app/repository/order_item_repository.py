from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from order_service.app.models.order_item import OrderItem
from typing import List


class OrderItemRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all(self) -> List[OrderItem]:
        order_items = await self.db.execute(select(OrderItem))
        return order_items.scalars().all()

    async def get_by_id(self, order_item_id: int) -> OrderItem | None:
        order_item = await self.db.execute(select(OrderItem).where(OrderItem.id == order_item_id))
        return order_item.scalars().one_or_none()

    async def get_by_product_id(self, product_id: int) -> List[OrderItem]:
        order_items = await self.db.execute(select(OrderItem).where(OrderItem.product_id == product_id))
        return order_items.scalars().all()

    async def get_by_product_name(self, product_name: str) -> List[OrderItem]:
        order_items = await self.db.execute(select(OrderItem).where(OrderItem.product_name == product_name))
        return order_items.scalars().all()

    async def get_by_order_id(self, order_id: int) -> List[OrderItem]:
        order_items = await self.db.execute(select(OrderItem).where(OrderItem.order_id == order_id))
        return order_items.scalars().all()
