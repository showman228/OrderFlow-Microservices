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
        notifs = await self.db.execute(
            select(Notification)
            .where(Notification.user_id == user_id)
            .limit(5)
            .offset(5)
            .order_by(Notification.id.desc())
        )

        return list(notifs.scalars().all())

    async def get_all_notification(self) -> list[Notification]:
        notifs = await self.db.execute(
            select(Notification)
            .order_by(Notification.id.desc())
        )

        return notifs.scalars().all()

    async def create(self, notif_data: NotificationCreate) -> Notification:
        notif = Notification(
            user_id=notif_data.user_id,
            order_id=notif_data.order_id,
            status=notif_data.status,
            total_price=notif_data.total_price,
            message=notif_data.message,
        )

        self.db.add(notif)
        await self.db.commit()
        return notif

    async def delete(self, notif_id: int) -> bool:
        notif = await self.db.execute(select(Notification).where(Notification.id == notif_id))
        if notif is None:
            return False

        await self.db.delete(notif)
        await self.db.commit()
        return True

    