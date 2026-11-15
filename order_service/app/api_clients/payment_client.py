from order_service.app.config import settings
from pydantic import BaseModel

class PaymentResponse(BaseModel):
    order_id: int
    user_id: int
    amount: float

class PaymentClient:
    def __init__(self, payment_client):
        self.client = payment_client

    async def create_payment(self, order_id: int, user_id: int, amount: float):
        json_data = {
            "order_id": order_id,
            "user_id": user_id,
            "amount": amount
        }
        response = await self.client.post(f"{settings.PAYMENT_SERVICE_URL}/payments/create", json=json_data)
        response.raise_for_status()
        return PaymentResponse.model_validate(response.json())