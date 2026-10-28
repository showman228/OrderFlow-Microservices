import httpx

from order_service.app.schemas.catalog_product import CatalogProductResponse
from order_service.app.services.catalog_client import CatalogClient

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from order_service.app.repository.order_item_repository import OrderItemRepository
from order_service.app.schemas.order_item import OrderItemCreate, OrderItemResponse, OrderItemUpdate


class OrderItemService:
    def __init__(self, db: AsyncSession, catalog_client: CatalogClient):
        self.crud = OrderItemRepository(db)
        self.catalog_client = catalog_client

    async def get_all(self) -> list[OrderItemResponse]:
        order_items = await self.crud.get_all()
        return [OrderItemResponse.model_validate(item) for item in order_items]

    async def get_by_id(self, order_item_id: int) -> OrderItemResponse:
        order_item = await self.crud.get_by_id(order_item_id)

        if order_item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order item not found by id"
            )

        return OrderItemResponse.model_validate(order_item)

    async def get_by_order_id(self, order_id: int) -> list[OrderItemResponse]:
        order_items = await self.crud.get_by_order_id(order_id)
        return [OrderItemResponse.model_validate(item) for item in order_items]


    async def create(self, order_id: int, item_data: OrderItemCreate) -> OrderItemResponse:
        try:
            product = await self.catalog_client.get_product(item_data.product_id)
        except httpx.HTTPStatusError as er:
            if er.response.status_code == 404:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Product not found by id"
                )
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Catalog service error"
            )
        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Catalog service unavailable"
            )

        item = await self.crud.create(
            order_id=order_id,
            product_id=product.id,
            product_name=product.name,
            quantity=item_data.quantity,
            price=product.price,
        )

        return OrderItemResponse.model_validate(item)

    async def update(self, order_item_id: int, order_item_data: OrderItemUpdate) -> OrderItemResponse:
        order_item = await self.crud.update(order_item_id, order_item_data)

        if order_item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found by id"
            )

        return OrderItemResponse.model_validate(order_item)

    async def delete(self, order_item_id: int) -> bool:
        order_item = await self.crud.delete(order_item_id)

        if order_item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found by id"
            )     

        return True
   
