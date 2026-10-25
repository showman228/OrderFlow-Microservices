from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from order_service.app.database import Base

if TYPE_CHECKING:
    from order_service.app.models.order import Order

class OrderItem(Base):
    __tablename__ = "order_items"

    product_id: Mapped[int]
    product_name: Mapped[str] = mapped_column(nullable=False)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    quantity: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)

    order: Mapped["Order"] = relationship("Order", back_populates="items")
