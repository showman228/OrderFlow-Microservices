from typing import TYPE_CHECKING

from datetime import datetime, UTC
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from order_service.app.database import Base

if TYPE_CHECKING:
    from order_service.app.models.order_item import OrderItem


class Order(Base):
    __tablename__ = "orders"

    user_id: Mapped[int]
    status: Mapped[str]
    total_price: Mapped[float] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    

    def __repr__(self):
        return f"Order id: {self.id}, User id: {self.user_id}, status: {self.status}, total_price: {self.total_price}, created_at: {self.created_at}"
