import asyncio
import httpx
from fastapi import HTTPException, status

from order_service.app.schemas.cart import CartItem, CartResponse
from order_service.app.schemas.catalog_product import CatalogProductResponse
from order_service.app.services.catalog_client import CatalogClient

# Делаем запрос (_fetch_product) -> делаем item (_build_cart_item) -> собираем items вместе (_build_cart_items) -> делаем ответ в корректной форме (_build_response)
class CartService:
    def __init__(self, catalog_client: CatalogClient):
        self.catalog_client = catalog_client

    async def get_cart(self, cart: dict[int, int]) -> CartResponse:
        if not cart:
            return CartResponse(items=[], total=0.0, items_count=0)

        items = await self._fetch_items(cart)
        return self._build_response(items)

    async def add_item(
        self, cart: dict[int, int], product_id: int, quantity: int
    ) -> CartResponse:
        if quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantity must be positive",
            )

        await self._ensure_product_exists(product_id)
        cart[product_id] = cart.get(product_id, 0) + quantity
        return await self.get_cart(cart)

    async def update_item(
        self, cart: dict[int, int], product_id: int, quantity: int
    ) -> CartResponse:
        if product_id not in cart:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found in cart",
            )

        if quantity <= 0:
            del cart[product_id]
        else:
            cart[product_id] = quantity

        return await self.get_cart(cart)

    async def remove_item(
        self, cart: dict[int, int], product_id: int
    ) -> CartResponse:
        cart.pop(product_id, None)
        return await self.get_cart(cart)

    async def clear_cart(self) -> CartResponse:
        return CartResponse(items=[], total=0.0, items_count=0)

    async def check_catalog(self) -> dict:
        return await self.catalog_client.healthcheck()

    # проверка на существование товара
    async def _ensure_product_exists(self, product_id: int) -> None:
        await self._fetch_product(product_id)

    async def _fetch_items(self, cart: dict[int, int]) -> list[CartItem]:
        tasks = [
            self._build_cart_item(product_id, quantity)
            for product_id, quantity in cart.items()
        ]
        return await asyncio.gather(*tasks)

    async def _build_cart_item(self, product_id: int, quantity: int) -> CartItem:
        product = await self._fetch_product(product_id)
        price = float(product.price)
        subtotal = price * quantity
        return CartItem(
            product_id=product_id,
            product_name=product.name,
            price=price,
            quantity=quantity,
            image_url=product.image_url,
            subtotal=subtotal,
        )

    async def _fetch_product(self, product_id: int) -> CatalogProductResponse:
        try:
            return await self.catalog_client.get_product(product_id)
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Product not found by id",
                )
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Catalog service error",
            )
        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Catalog service unavailable",
            )

    def _build_response(self, items: list[CartItem]) -> CartResponse:
        total = sum(item.subtotal for item in items)
        items_count = len(items)
        return CartResponse(items=items, total=total, items_count=items_count)
