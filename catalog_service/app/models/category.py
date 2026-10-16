from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from catalog_service.app.database import Base
from catalog_service.app.models.product import Product


class Category(Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    products = List["Product"] = relationship(back_populates="category")

    def __repr__(self):
        return f"<Category id: {self.id}, name: {self.name}, slug: {self.slug}>"
