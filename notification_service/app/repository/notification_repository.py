from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from notification_service.app.models.notification import Notification
from notification_service.app.schemas.notification import NotificationCreate


class NotificationRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_notification_by_id(self, notif_id: int) -> Notification | None:
        notif = await self.db.execute(select(Notification).where(Notification.id == notif_id))
        return notif.scalars().one_or_none()

    async def get_notification_by_user_id(self, user_id: int) -> list[Notification]:
        notif = await self.db.execute(
            select(Notification).where(Notification.user_id == user_id)
        )

        return notif.scalars().one_or_none()

    async def get_all_notification(self) -> list[Notification]:
        notifs = await self.db.execute(
            select(Notification)
        )

        return notifs.scalars().all()

    async def create(self, notif_data: NotificationCreate) -> Notification:
        pass

    async def delete(self, notif_id: int) -> bool:
        pass
    