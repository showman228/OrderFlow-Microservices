from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from order_service.app.models.order import Order
from order_service.app.models.order_item import OrderItem
from typing import List
from httpx import AsyncClient

class OrderItemRepository:
    def __init__(self, db: AsyncSession, catalog_client: AsyncClient) -> None:
        self.db = db
        self.catalog_client = catalog_client

    async def get_all(self) -> List[OrderItem]:
        order_items = await self.db.execute(select(OrderItem))
        return order_items.scalars().all()

    async def get_by_id(self, order_item_id: int) -> OrderItem | None:
        order_item = await self.db.execute(select(OrderItem).where(OrderItem.id == order_item_id))
        return order_item.scalars().one_or_none()

    async def get_by_order_id(self, order_id: int) -> List[OrderItem]:
        order_items = await self.db.execute(select(OrderItem).where(OrderItem.order_id == order_id))
        return order_items.scalars().all()


    async def create(self,
            order_id: int,
            product_id: int,
            product_name: str,
            quantity: int,
            price: float
        ) -> Order:

        order_item = OrderItem(
            order_id=order_id,
            product_id=product_id,
            product_name=product_name,
            quantity=quantity,
            price=price
        )

        self.db.add(order_item)
        self.db.commit()
        self.db.refresh(order_item)

        return order_item

    # Дореализовать
    async def update(self,
            order_id: int, 
            product_id: int,
            product_name: str,
            quantity: int,
            price: float
        ) -> Order:

        pass

    
    # Дореализовать
    async def delete(self):
        pass