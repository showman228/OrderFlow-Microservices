from pydantic import BaseModel, ConfigDict

class Notification(BaseModel):
    user_id: int
    order_id: int
    status: str
    total_price: float
    message: str

class NotificationCreate(Notification):
    pass

class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    order_id: int
    status: str
    total_price: float
    message: str

