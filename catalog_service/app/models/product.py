from typing import TYPE_CHECKING

from datetime import datetime, UTC
from sqlalchemy import ForeignKey, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from catalog_service.app.database import Base

if TYPE_CHECKING:
    from catalog_service.app.models.category import Category


class Product(Base):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(300), unique=True, index=True)
    price: Mapped[int] = mapped_column(nullable=False)

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    image_url: Mapped[str]

    category: Mapped["Category"] = relationship(back_populates="products")

    def __repr__(self):
        return f"Product: {self.id}, name: {self.name}, description: {self.description}, price: {self.price}"
