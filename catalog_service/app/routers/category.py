from fastapi import APIRouter, Depends, status
from catalog_service.app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from catalog_service.app.services.category_service import CategoryService
from catalog_service.app.schemas.category import CategoryCreate, CategoryResponse

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)

@router.get("/", response_model=list[CategoryResponse], status_code=status.HTTP_200_OK)
async def get_all_categories(db: AsyncSession = Depends(get_db)):
    category_service = CategoryService(db)
    return await category_service.get_all()

@router.get("/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
async def get_by_id(category_id: int, db: AsyncSession = Depends(get_db)):
    category_service = CategoryService(db)
    return await category_service.get_by_id(category_id)

@router.get("/{category_name}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
async def get_by_name(category_name: str, db: AsyncSession = Depends(get_db)):
    category_service = CategoryService(db)
    return await category_service.get_by_name(category_name)

@router.get("/{category_slug}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
async def get_by_slug(category_slug: str, db: AsyncSession = Depends(get_db)):
    category_service = CategoryService(db)
    return await category_service.get_by_slug(category_slug)
