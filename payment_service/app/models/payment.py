from datetime import datetime, UTC
from enum import StrEnum

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from payment_service.app.database import Base


class PaymentStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    PAID = "paid"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Payment(Base):
    __tablename__ = "payments"

    order_id: Mapped[int] = mapped_column(index=True)
    user_id: Mapped[int] = mapped_column(index=True)
    status: Mapped[str] = mapped_column(
        String(20), default=PaymentStatus.PENDING.value, nullable=False
    )
    amount: Mapped[float] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
