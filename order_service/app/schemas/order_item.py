
from pydantic import BaseModel, ConfigDict


class OrderItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_id: int
    product_id: int
    product_name: str
    quantity: int
    price: float


class OrderItemCreate(OrderItem):
    pass


class OrderItemUpdate(BaseModel):
    product_id: int | None = None
    product_name: str | None = None
    quantity: int | None = None
    price: float | None = None


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    product_name: str
    order_id: int
    quantity: int
    price: float
