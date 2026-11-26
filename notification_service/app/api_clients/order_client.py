from notification_service.app.schemas.order import OrderResponse

class OrderClient:

    def __init__(self, order_client):
        self.client = order_client

    async def get_order(self, order_id: int) -> OrderResponse:
        response = await self.client.get(f"/orders/{order_id}")
        response.raise_for_status()
        return OrderResponse.model_validate(response.json())

