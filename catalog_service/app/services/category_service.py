from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from catalog_service.app.repositories.category_repository import CategoryRepository

from typing import List

from catalog_service.app.schemas.category import CategoryCreate, CategoryResponse

class CategoryService:
    def __init__(self, crud: AsyncSession):
        self.crud = CategoryRepository(crud)

    async def get_all(self) -> List[CategoryResponse]:
        categories = await self.crud.get_all()
        return [CategoryResponse.model_validate(cat) for cat in categories]

    async def get_by_id(self, category_id: int) -> CategoryResponse:
        category = await self.crud.get_by_id(category_id)

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found by id"
                )

        return CategoryResponse.model_validate(category)

    async def get_by_name(self, category_name: str) -> CategoryResponse:
        category = await self.crud.get_by_name(category_name)

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found by name"
            )

        return CategoryResponse.model_validate(category)

    async def get_by_slug(self, category_slug: str) -> CategoryResponse:
        category = await self.crud.get_by_slug(category_slug)

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found by slug"
            )

        return CategoryResponse.model_validate(category)

    async def create(self, category_data: CategoryCreate) -> CategoryResponse:
        existing = await self.crud.get_by_name(category_data.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Category already exists"
            )

        category = await self.crud.create(category_data)
        return CategoryResponse.model_validate(category)

    async def update(self, category_id: int, category_data: CategoryCreate) -> CategoryResponse:
        category = await self.crud.update(category_id, category_data)

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found by id"
            )

        return CategoryResponse.model_validate(category)

    async def delete(self, category_id: int) -> bool:
        result = await self.crud.delete(category_id)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found by id"
            )

        return True

