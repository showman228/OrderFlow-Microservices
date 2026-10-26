import httpx
from order_service.app.schemas.catalog_product import CatalogProductResponse


class CatalogClient:

    def __init__(self, base_url: str):
        self.base_url = base_url

    async def get_product(self, product_id: int) -> CatalogProductResponse:
        async with httpx.AsyncClient(base_url=self.base_url) as client:
            response = await client.get(f"/products/{product_id}")
            response.raise_for_status()
            return CatalogProductResponse.model_validate(response.json())
