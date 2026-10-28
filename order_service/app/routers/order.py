from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from order_service.app.database import get_db

from order_service.app.schemas.order import OrderCreate, OrderResponse, OrderUpdate
from order_service.app.services.order_services import OrderService

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[OrderResponse])
async def get_all_orders(db: AsyncSession = Depends(get_db)):
    service = OrderService(db)
    return await service.get_all()

@router.get("/{order_id}", status_code=status.HTTP_200_OK, response_model=OrderResponse)
async def get_by_id(order_id: int, db: AsyncSession = Depends(get_db)):
    service = OrderService(db)
    return await service.get_by_id(order_id)

@router.get("/users/{user_id}", status_code=status.HTTP_200_OK, response_model=list[OrderResponse])
async def get_by_user_id(user_id: int, db: AsyncSession = Depends(get_db)):
    service = OrderService(db)
    return await service.get_by_user_id(user_id)

@router.get("/{status}", status_code=status.HTTP_200_OK, response_model=list[OrderResponse])
async def get_by_status(status: str, db: AsyncSession = Depends(get_db)):
    service = OrderService(db)
    return await service.get_by_status(status)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=OrderResponse)
async def create_order(order_data: OrderCreate, db: AsyncSession = Depends(get_db)):
    service = OrderService(db)
    return await service.create(order_data)

@router.patch("/{order_id}", status_code=status.HTTP_200_OK, response_model=OrderResponse)
async def update_order(order_id: int, order_data: OrderUpdate, db: AsyncSession = Depends(get_db)):
    service = OrderService(db)
    return await service.update(order_id, order_data)

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: int, db: AsyncSession = Depends(get_db)):
    service = OrderService(db)
    return await service.delete(order_id)