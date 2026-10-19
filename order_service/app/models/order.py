from typing import TYPE_CHECKING

from datetime import datetime, UTC
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from order_service.app.database import Base
from typing import List

if TYPE_CHECKING:
    from ...app.models.order_item import OrderItem


class Order(Base):
    __tablename__ = "orders"

    user_id: Mapped[int]
    status: Mapped[str]
    total_price: Mapped[float] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(UTC)
    )
    items: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="order")
    

    def __repr__(self):
        return f""
