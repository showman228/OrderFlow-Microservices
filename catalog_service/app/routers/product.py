from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from typing import List

from catalog_service.app.services.product_service import ProductService
from catalog_service.app.schemas.product import ProductResponse, ProductCreate
from catalog_service.app.database import get_db

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.get("/", response_model=List[ProductResponse], status_code=status.HTTP_200_OK)
async def get_all_products(db: AsyncSession = Depends(get_db)):
    products_service = ProductService(db)
    return await products_service.get_all()

@router.get("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def get_by_id(product_id: int, db: AsyncSession = Depends(get_db)):
    product_service = ProductService(db)
    return await product_service.get_by_id(product_id)

@router.get("/{product_name}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def get_by_name(product_name: str, db: AsyncSession = Depends(get_db)):
    product_service = ProductService(db)
    return await product_service.get_by_name(product_name)




