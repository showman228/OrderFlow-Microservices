from sqlalchemy.ext.asyncio import AsyncSession
from order_service.app.repository.order_repository import OrderRepository
from order_service.app.schemas.order import OrderResponse, OrderCreate, OrderUpdate
from fastapi import HTTPException, status


class OrderService:
    def __init__(self, db: AsyncSession):
        self.crud = OrderRepository(db)
        
    async def get_by_id(self, order_id: int) -> OrderResponse:
        order = await self.crud.get_by_id(order_id)

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Order not found by id"
            )

        return OrderResponse.model_validate(order)

    async def get_all(self) -> list[OrderResponse]:
        orders = await self.crud.get_all()
        return [OrderResponse.model_validate(od) for od in orders]

    async def get_by_user_id(self, user_id: int) -> list[OrderResponse]:
        orders = await self.crud.get_by_user_id(user_id)
        return [OrderResponse.model_validate(od) for od in orders]

    async def get_by_status(self, status: str) -> list[OrderResponse]:
        orders = await self.crud.get_by_status(status)
        return [OrderResponse.model_validate(od) for od in orders]

    async def create(self, order_data: OrderCreate) -> OrderResponse:
        order = await self.crud.create(order_data)
        return OrderResponse.model_validate(order)

    async def update(self, order_id: int, order_data: OrderUpdate) -> OrderResponse:
        order = await self.crud.update(order_id, order_data)

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found by id"
            )

        return OrderResponse.model_validate(order)

    async def delete(self, order_id: int) -> bool:
        order = await self.crud.delete(order_id)

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found by id"
            )

        return True
