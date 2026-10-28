from pydantic import BaseModel, ConfigDict


class CatalogProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")

    id: int
    name: str
    price: float
    image_url: str | None = None
