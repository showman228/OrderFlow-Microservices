from fastapi import APIRouter, status

from order_service.app.deps import CatalogClientDep
from order_service.app.schemas.cart import (
    AddToCartRequest,
    CartDetailsRequest,
    CartResponse,
    RemoveFromCartRequest,
    UpdateCartRequest,
)
from order_service.app.services.cart import CartService

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.post("/add", response_model=CartResponse, status_code=status.HTTP_200_OK)
async def add_item(request: AddToCartRequest, client: CatalogClientDep) -> CartResponse:
    service = CartService(client)
    return await service.add_item(request.cart, request.product_id, request.quantity)


@router.post("/update", response_model=CartResponse, status_code=status.HTTP_200_OK)
async def update_item(request: UpdateCartRequest, client: CatalogClientDep) -> CartResponse:
    service = CartService(client)
    return await service.update_item(request.cart, request.product_id, request.quantity)


@router.post("/remove", response_model=CartResponse, status_code=status.HTTP_200_OK)
async def remove_item(request: RemoveFromCartRequest, client: CatalogClientDep) -> CartResponse:
    service = CartService(client)
    return await service.remove_item(request.cart, request.product_id)


@router.post("/clear", response_model=CartResponse, status_code=status.HTTP_200_OK)
async def clear_cart(client: CatalogClientDep) -> CartResponse:
    service = CartService(client)
    return await service.clear_cart()


@router.post("/details", response_model=CartResponse, status_code=status.HTTP_200_OK)
async def cart_details(request: CartDetailsRequest, client: CatalogClientDep) -> CartResponse:
    service = CartService(client)
    return await service.get_cart(request.cart_data)
