import asyncio

import httpx
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from order_service.app.repository.order_repository import OrderRepository
from order_service.app.schemas.catalog_product import CatalogProductResponse
from order_service.app.schemas.order import OrderCreate, OrderResponse, OrderUpdate
from order_service.app.schemas.order_item import OrderItemCreate
from order_service.app.services.catalog_client import CatalogClient


class OrderService:
    def __init__(self, db: AsyncSession, catalog_client: CatalogClient) -> None:
        self.crud = OrderRepository(db)
        self.catalog_client = catalog_client

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

    async def get_by_status(self, order_status: str) -> list[OrderResponse]:
        orders = await self.crud.get_by_status(order_status)
        return [OrderResponse.model_validate(od) for od in orders]

    async def create(self, order_data: OrderCreate) -> OrderResponse:
        products = await self._fetch_products(order_data)

        items = [
            OrderItemCreate(
                product_id=product.id,
                product_name=product.name,
                price=product.price,
                quantity=requested.quantity,
            )
            for product, requested in zip(products, order_data.items, strict=True)
        ]
        total_price = sum(item.price * item.quantity for item in items)

        order = await self.crud.create(
            user_id=order_data.user_id,
            total_price=total_price,
            items=items,
        )
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

    async def _fetch_products(self, order_data: OrderCreate) -> list[CatalogProductResponse]:
        return await asyncio.gather(
            *[self._fetch_product(item.product_id) for item in order_data.items]
        )

    async def _fetch_product(self, product_id: int) -> CatalogProductResponse:
        try:
            return await self.catalog_client.get_product(product_id)
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with id={product_id} not found",
                ) from exc
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Catalog service error",
            ) from exc
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Catalog service unavailable",
            ) from exc
