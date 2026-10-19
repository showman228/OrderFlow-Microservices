from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ...app.database import Base

if TYPE_CHECKING:
    from ...app.models.order import Order

class OrderItem(Base):
    __tablename__ = "orders_items"

    product_id: Mapped[int]
    product_name: Mapped[str] = mapped_column(nullable=False)
    order_id = Mapped[int] = mapped_column(ForeignKey("order.id"))
    quantity: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)

    order: Mapped["Order"] = relationship("Order", back_populates="items")
