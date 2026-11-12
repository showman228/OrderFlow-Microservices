from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from payment_service.app.database import get_db
from payment_service.app.schemas.payment import PaymentCreate, PaymentResponse
from payment_service.app.services.payment_service import PaymentService

router = APIRouter(
    prefix="/payments",
    tags=["Payment"],
)

PaymentIdPath = Annotated[int, Path(ge=1, description="Payment id")]
UserIdPath = Annotated[int, Path(ge=1, description="User id")]
OrderIdPath = Annotated[int, Path(ge=1, description="Order id")]


@router.get("/", response_model=list[PaymentResponse], status_code=status.HTTP_200_OK)
async def get_all(db: AsyncSession = Depends(get_db)) -> list[PaymentResponse]:
    return await PaymentService(db).get_all_payments()


@router.get(
    "/{payment_id}", response_model=PaymentResponse, status_code=status.HTTP_200_OK
)
async def get_by_payment_id(
    payment_id: PaymentIdPath, db: AsyncSession = Depends(get_db)
) -> PaymentResponse:
    return await PaymentService(db).get_by_id(payment_id)


@router.get(
    "/users/{user_id}",
    response_model=list[PaymentResponse],
    status_code=status.HTTP_200_OK,
)
async def get_by_user_id(
    user_id: UserIdPath, db: AsyncSession = Depends(get_db)
) -> list[PaymentResponse]:
    return await PaymentService(db).get_by_user_id(user_id)


@router.get(
    "/orders/{order_id}", response_model=PaymentResponse, status_code=status.HTTP_200_OK
)
async def get_by_order_id(
    order_id: OrderIdPath, db: AsyncSession = Depends(get_db)
) -> PaymentResponse:
    return await PaymentService(db).get_by_order_id(order_id)


@router.post(
    "/create", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED
)
async def create(
    payment_data: PaymentCreate, db: AsyncSession = Depends(get_db)
) -> PaymentResponse:
    return await PaymentService(db).create(payment_data)


@router.post(
    "/{payment_id}/pay", response_model=PaymentResponse, status_code=status.HTTP_200_OK
)
async def pay(
    payment_id: PaymentIdPath, db: AsyncSession = Depends(get_db)
) -> PaymentResponse:
    return await PaymentService(db).pay(payment_id)


@router.post(
    "/{payment_id}/fail", response_model=PaymentResponse, status_code=status.HTTP_200_OK
)
async def fail(
    payment_id: PaymentIdPath, db: AsyncSession = Depends(get_db)
) -> PaymentResponse:
    return await PaymentService(db).fail(payment_id)


@router.post(
    "/{payment_id}/cancel",
    response_model=PaymentResponse,
    status_code=status.HTTP_200_OK,
)
async def cancel(
    payment_id: PaymentIdPath, db: AsyncSession = Depends(get_db)
) -> PaymentResponse:
    return await PaymentService(db).cancel(payment_id)
