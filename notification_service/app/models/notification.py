from enum import StrEnum

from datetime import datetime, UTC
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from notification_service.app.database import Base

class NotificationType(StrEnum):
    ORDER_CREATE = "create"
    ORDER_PAID = "paid"

class Notification(Base):
    __tablename__ = "notifications"

    user_id: Mapped[int]
    order_id: Mapped[int]
    status: Mapped[str] = mapped_column(
        String(20), default=NotificationType.ORDER_CREATE.value, nullable=False
    )
    message: Mapped[str] = mapped_column(
        String(100), nullable=False
    )
    total_price: Mapped[float] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    

    def __repr__(self):
        return f"Notification id: {self.id}, User id: {self.user_id}, Order_id: {self.order_id}, status: {self.status}, total_price: {self.total_price}, created_at: {self.created_at}"
