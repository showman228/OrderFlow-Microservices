from fastapi import APIRouter, Depends, status, Request

from order_service.app.config import settings
from order_service.app.schemas.cart import (
    AddToCartRequest,
    CartDetailsRequest,
    CartResponse,
    RemoveFromCartRequest,
    UpdateCartRequest,
)
from order_service.app.services.cart import CartService
from order_service.app.services.catalog_client import CatalogClient

router = APIRouter(prefix="/cart", tags=["Cart"])


def get_catalog_client(request: Request) -> CatalogClient:
    return CatalogClient(request.app.state.catalog_client)


@router.post("/add",response_model=CartResponse, status_code=status.HTTP_200_OK)
async def add_item(request: AddToCartRequest, client: CatalogClient = Depends(get_catalog_client),) -> CartResponse:
    service = CartService(client)
    return await service.add_item(request.cart, request.product_id, request.quantity)


@router.post("/update", response_model=CartResponse, status_code=status.HTTP_200_OK)
async def update_item(request: UpdateCartRequest, client: CatalogClient = Depends(get_catalog_client)) -> CartResponse:
    service = CartService(client)
    return await service.update_item(request.cart, request.product_id, request.quantity)


@router.post("/remove", response_model=CartResponse, status_code=status.HTTP_200_OK)
async def remove_item(request: RemoveFromCartRequest, client: CatalogClient = Depends(get_catalog_client)) -> CartResponse:
    service = CartService(client)
    return await service.remove_item(request.cart, request.product_id)


@router.post("/clear", response_model=CartResponse, status_code=status.HTTP_200_OK)
async def clear_cart(client: CatalogClient = Depends(get_catalog_client)) -> CartResponse:
    service = CartService(client)
    return await service.clear_cart()


@router.post("/details", response_model=CartResponse, status_code=status.HTTP_200_OK)
async def cart_details(request: CartDetailsRequest, client: CatalogClient = Depends(get_catalog_client)) -> CartResponse:
    service = CartService(client)
    return await service.get_cart(request.cart_data)
