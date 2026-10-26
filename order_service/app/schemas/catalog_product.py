from pydantic import BaseModel, ConfigDict

class CatalogProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")
    
    product_id: int
    product_name: str
    quantity: int
    price: float
    