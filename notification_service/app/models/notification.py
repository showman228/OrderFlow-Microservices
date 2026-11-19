from enum import StrEnum

from datetime import datetime, UTC
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from notification_service.app.database import Base

class PaymentStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    PAID = "paid"
    FAILED = "failed"
    CANCELLED = "cancelled"
    
class Notification(Base):
    __tablename__ = "notifications"

    user_id: Mapped[int]
    status: Mapped[str] = mapped_column(
        String(20), default=PaymentStatus.PROCESSING.value, nullable=False
    )
    total_price: Mapped[float] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    

    def __repr__(self):
        return f"Notification id: {self.id}, User id: {self.user_id}, status: {self.status}, total_price: {self.total_price}, created_at: {self.created_at}"
