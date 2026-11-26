from typing import Annotated

from fastapi import APIRouter, Query, status
from notification_service.app.deps import SessionDep, OrderClintDep
from notification_service.app.schemas.notification import NotificationResponse, OrderPaidNotificationCreate
from notification_service.app.services.notification_services import NotificationService

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=list[NotificationResponse],
)
async def get_notification_by_user_id(
    user_id: int,
    db: SessionDep,
    order_client: OrderClintDep,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[NotificationResponse]:
    notification_service = NotificationService(order_client, db)
    return await notification_service.get_notification_by_user_id(
        user_id, limit, offset
    )


@router.get(
    "/{notif_id}", status_code=status.HTTP_200_OK, response_model=NotificationResponse
)
async def get_notification_by_id(
    notif_id: int, db: SessionDep, order_client: OrderClintDep
) -> NotificationResponse:
    notification_service = NotificationService(order_client, db)
    return await notification_service.get_notification_by_id(notif_id)


@router.delete(
    "/notifications/{notif_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_notification(
    notif_id: int, db: SessionDep, order_client: OrderClintDep
) -> None:
    notification_service = NotificationService(order_client, db)
    await notification_service.delete_notification(notif_id)


@router.post(
    "/order-created",
    status_code=status.HTTP_201_CREATED,
    response_model=NotificationResponse,
)
async def create_order_created_notification(
    payload: OrderPaidNotificationCreate, db: SessionDep, order_client: OrderClintDep
) -> NotificationResponse:
    notification_service = NotificationService(order_client, db)
    return await notification_service.create_order_created_notification(
        order_id=payload.order_id,
        user_id=payload.user_id,
        amount=payload.amount,
    )


@router.post(
    "/order-paid", status_code=status.HTTP_201_CREATED, response_model=NotificationResponse
)
async def create_notification_for_pay(
    payload: OrderPaidNotificationCreate, db: SessionDep, order_client: OrderClintDep
) -> NotificationResponse:
    notification_service = NotificationService(order_client, db)
    return await notification_service.create_notification_for_pay(
        order_id=payload.order_id,
        user_id=payload.user_id,
        amount=payload.amount
    )
