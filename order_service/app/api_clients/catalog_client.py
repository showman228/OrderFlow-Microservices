import httpx

from order_service.app.schemas.catalog_product import CatalogProductResponse


class CatalogClient:

    def __init__(self, catalog_client):
        self.client = catalog_client

    async def get_product(self, product_id: int) -> CatalogProductResponse:
        response = await self.client.get(f"/products/{product_id}")
        response.raise_for_status()
        return CatalogProductResponse.model_validate(response.json())

    async def healthcheck(self) -> dict:
        try:
            response = await self.client.get("/health")
            response.raise_for_status()
            return {"status": "ok", "catalog": response.json()}
        except httpx.HTTPStatusError as exc:
            return {
                "status": "error",
                "detail": f"Catalog service returned {exc.response.status_code}",
            }
        except httpx.RequestError as exc:
            return {"status": "unavailable", "detail": str(exc)}
