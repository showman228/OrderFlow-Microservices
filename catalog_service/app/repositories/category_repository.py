from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from catalog_service.app.models.category import Category
from catalog_service.app.schemas.category import CategoryCreate


class CategoryRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, category_id: int) -> Category | None:
        category_crud = await self.db.execute(
            select(Category).where(Category.id == category_id)
        )
        return category_crud.scalars().one_or_none()

    async def get_by_slug(self, slug: str) -> Category | None:
        category_crud = await self.db.execute(
            select(Category).where(Category.slug == slug)
        )
        return category_crud.scalars().one_or_none()

    async def get_by_name(self, name: str) -> Category | None:
        category_crud = await self.db.execute(
            select(Category).where(Category.name == name)
        )
        return category_crud.scalars().one_or_none()

    async def get_all(self) -> list[Category]:
        category_crud = await self.db.execute(select(Category))
        return category_crud.scalars().all()

    async def create(self, category_data: CategoryCreate) -> Category | None:
        category = Category(
            name=category_data.name,
            slug=category_data.slug,
        )

        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def update(
        self, category_id: int, data: CategoryCreate
    ) -> Category | None:
        category = await self.get_by_id(category_id)

        if category is None:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(category, field, value)

        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def delete(self, category_id: int) -> bool:
        category = await self.get_by_id(category_id)

        if category is None:
            return False

        await self.db.delete(category)
        await self.db.commit()
        return True
