from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from catalog_service.app.models.product import Product
from catalog_service.app.schemas.product import ProductCreate


class ProductRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, product_id: int) -> Product | None:
        product_repository = await self.db.execute(
            select(Product).where(product_id == Product.id)
        )
        return product_repository.scalars().one_or_none()

    async def get_all(self) -> list[Product]:
        product_repository = await self.db.execute(
            select(Product).options(selectinload(Product.category)).limit(100)
        )
        return product_repository.scalars().all()

    async def get_by_name(self, product_name: str) -> Product | None:
        product_repository = await self.db.execute(
            select(Product).where(Product.name == product_name)
        )
        return product_repository.scalars().one_or_none()

    async def get_by_category_id(self, category_id: int) -> list[Product]:
        product_repository = await self.db.execute(
            select(Product).where(Product.category_id == category_id)
        )
        return product_repository.scalars().all()

    async def create(self, product_data: ProductCreate) -> Product | None:
        product = Product(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            category_id=product_data.category_id,
        )

        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def update(
        self, product_id: int, product_data: ProductCreate
    ) -> Product | None:
        product = await self.get_by_id(product_id)

        if not product:
            return None

        for field, value in product_data.model_dump(exclude_unset=True).items():
            setattr(product, field, value)

        await self.db.commit()
        await self.db.refresh(product)

        return product

    async def delete(self, product_id: int) -> bool:
        product = await self.get_by_id(product_id)
        if not product:
            return False

        await self.db.delete(product)
        await self.db.commit()
        return True
