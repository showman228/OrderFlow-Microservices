from sqlalchemy.ext.asyncio import AsyncSession
from notification_service.app.api_clients.order_client import OrderClient
from notification_service.app.repository.notification_repository import NotificationRepository
from notification_service.app.schemas.notification import NotificationCreate, NotificationResponse


class NotificationServices:
    def __init__(self, order_client: OrderClient, db: AsyncSession):
        self.client = order_client
        self.crud = NotificationRepository(db)

    async def get_notification_by_user_id(self, user_id: int) -> list[NotificationResponse]:
        pass

    async def get_notification_by_id(self, notif_id: int) -> NotificationResponse | None:
        pass

    async def create_notification_for_create_order(self, notif_data: NotificationCreate) -> NotificationResponse | None:
        pass

    async def create_notification_for_pay(self, notif_data: NotificationCreate) -> NotificationResponse | None:
        pass

    async def delete_notification(self, notif_id: int) -> bool:
        pass