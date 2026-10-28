from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from catalog_service.app.schemas.product import ProductResponse, ProductCreate
from catalog_service.app.repositories.product_repository import ProductRepository

class ProductService:
    def __init__(self, crud: AsyncSession):
        self.crud = ProductRepository(crud)

    async def get_all(self) -> list[ProductResponse]:
        products = await self.crud.get_all()
        return [ProductResponse.model_validate(prod) for prod in products]

    async def get_by_id(self, product_id: int) -> ProductResponse:
        product = await self.crud.get_by_id(product_id)

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found by id"
            )

        return ProductResponse.model_validate(product)

    async def get_by_name(self, product_name: str) -> ProductResponse:
        product = await self.crud.get_by_name(product_name)

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found by name"
            )

        return ProductResponse.model_validate(product)

    async def get_product_by_category_id(self, category_id: int) -> list[ProductResponse]:
        products = await self.crud.get_by_category_id(category_id)
        return [ProductResponse.model_validate(prod) for prod in products]

    async def create(self, product_data: ProductCreate) -> ProductResponse:
        existing = await self.crud.get_by_name(product_data.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product already exist"
            )
        
        product = await self.crud.create(product_data)
        return ProductResponse.model_validate(product)

    async def update(self, product_data: ProductCreate) -> ProductResponse:
        product = await self.crud.update(product_data)

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product already exist"
            )

        return ProductResponse.model_validate(product)

    async def delete(self, product_id: int) -> bool:
        result = await self.crud.delete(product_id)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found by id"
            )

        return True
