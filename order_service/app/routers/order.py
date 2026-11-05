from typing import Annotated

from fastapi import APIRouter, Path, status

from order_service.app.deps import CatalogClientDep, SessionDep, CacheDep
from order_service.app.schemas.order import OrderCreate, OrderResponse, OrderUpdate
from order_service.app.services.order_services import OrderService

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

OrderIdPath = Annotated[int, Path(ge=1, description="Order id")]
UserIdPath = Annotated[int, Path(ge=1, description="User id")]


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[OrderResponse])
async def get_all_orders(
    db: SessionDep, catalog_client: CatalogClientDep, cache: CacheDep
) -> list[OrderResponse]:
    service = OrderService(db, catalog_client, cache)
    return await service.get_all()


@router.get(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=list[OrderResponse],
)
async def get_by_user_id(
    user_id: UserIdPath, db: SessionDep, catalog_client: CatalogClientDep, cache: CacheDep
) -> list[OrderResponse]:
    service = OrderService(db, catalog_client, cache)
    return await service.get_by_user_id(user_id)


@router.get(
    "/status/{order_status}",
    status_code=status.HTTP_200_OK,
    response_model=list[OrderResponse],
)
async def get_by_status(
    order_status: str, db: SessionDep, catalog_client: CatalogClientDep, cache: CacheDep
) -> list[OrderResponse]:
    service = OrderService(db, catalog_client, cache)
    return await service.get_by_status(order_status)


@router.get("/{order_id}", status_code=status.HTTP_200_OK, response_model=OrderResponse)
async def get_by_id(
    order_id: OrderIdPath, db: SessionDep, catalog_client: CatalogClientDep, cache: CacheDep
) -> OrderResponse:
    service = OrderService(db, catalog_client, cache)
    return await service.get_by_id(order_id)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=OrderResponse)
async def create_order(
    order_data: OrderCreate, db: SessionDep, catalog_client: CatalogClientDep, cache: CacheDep
) -> OrderResponse:
    service = OrderService(db, catalog_client, cache)
    return await service.create(order_data)


@router.patch("/{order_id}", status_code=status.HTTP_200_OK, response_model=OrderResponse)
async def update_order(
    order_id: OrderIdPath, order_data: OrderUpdate, db: SessionDep, catalog_client: CatalogClientDep, cache: CacheDep
) -> OrderResponse:
    service = OrderService(db, catalog_client, cache)
    return await service.update(order_id, order_data)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    order_id: OrderIdPath, db: SessionDep, catalog_client: CatalogClientDep, cache: CacheDep
) -> None:
    service = OrderService(db, catalog_client, cache)
    await service.delete(order_id)
