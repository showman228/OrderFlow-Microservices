from fastapi import APIRouter, HTTPException, status
from notification_service.app.deps import SessionDep, OrderClintDep
from notification_service.app.schemas.notification import NotificationCreate, NotificationResponse

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[NotificationResponse])
async def get_notification_by_user_id(user_id: int, db: SessionDep, order_client: OrderClintDep) -> NotificationResponse:
    pass

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[NotificationResponse])
async def get_notification_by_id(notif_id: int, db: SessionDep, order_client: OrderClintDep) -> NotificationResponse:
    pass

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[NotificationResponse])
async def create_notification_for_create_order(notif_data: NotificationCreate, db: SessionDep, order_client: OrderClintDep) -> NotificationResponse:
    pass

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[NotificationResponse])
async def create_notification_for_pay(notif_data: NotificationCreate, db: SessionDep, order_client: OrderClintDep) -> NotificationResponse:
    pass

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[NotificationResponse])
async def delete_notification(notif_id: int, db: SessionDep, order_client: OrderClintDep) -> NotificationResponse:
    pass
