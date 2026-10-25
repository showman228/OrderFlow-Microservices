from pydantic import BaseModel, ConfigDict


class OrderItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: int
    product_name: str
    quantity: int
    price: float


class OrderItemCreate(OrderItem):
    pass


class OrderItemUpdate(OrderItem):
    pass


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    order_id: int
    quantity: int
    price: float
