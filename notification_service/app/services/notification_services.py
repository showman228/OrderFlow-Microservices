from httpx import HTTPStatusError
from sqlalchemy.ext.asyncio import AsyncSession
from notification_service.app.api_clients.order_client import OrderClient
from notification_service.app.repository.notification_repository import NotificationRepository
from notification_service.app.schemas.notification import NotificationCreate, NotificationResponse
from fastapi import status, HTTPException

class NotificationService:
    def __init__(self, order_client: OrderClient, db: AsyncSession):
        self.client = order_client
        self.crud = NotificationRepository(db)

    async def get_notification_by_user_id(self, user_id: int) -> list[NotificationResponse]:
        notifs = await self.crud.get_notification_by_id(user_id)
        return [NotificationResponse.model_validate(notif) for notif in notifs]

    async def get_notification_by_id(self, notif_id: int) -> NotificationResponse | None:
        notif = await self.crud.get_notification_by_id(notif_id)
        if notif is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification by this id not found"
            )
        return NotificationResponse.model_validate(notif)

    async def create_order_created_notification(self, order_id: int, user_id: int) -> NotificationResponse | None:
        products, total_amount = await self._build_products_summary(order_id)

        items_text = ", ".join(
            f"{product['product_name']} x{product['quantity']}" for product in products
        )
        message = (
            f"Вы оформили заказ №{order_id}: {items_text} "
            f"на сумму {total_amount:.2f}"
        )

        notif_data = NotificationCreate(
            user_id=user_id,
            order_id=order_id,
            status="ORDER_CREATED",
            total_price=total_amount,
            message=message
        )

        notification = await self.crud.create(notif_data)
        return NotificationResponse.model_validate(notification)

    async def create_notification_for_pay(self, order_id: int, user_id: int) -> NotificationResponse | None:
        products, total_amount = await self._build_products_summary(order_id)

        message = (
            f"Вы оплатили заказ №{order_id} на сумму {total_amount:.2f}"
        )

        notif_data = NotificationCreate(
            user_id=user_id,
            order_id=order_id,
            status="ORDER_PAID",
            total_price=total_amount,
            message=message
        )

        notification = await self.crud.create(notif_data)
        return NotificationResponse.model_validate(notification)

    async def delete_notification(self, notif_id: int) -> bool:
        notif = await self.crud.delete(notif_id)
        if not notif:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification by this id not found"
            )
        return True

    async def _build_products_summary(self, order_id: int):
        try:
            order = await self.client.get_order(order_id)
        except HTTPStatusError as er:
            if er.response.status_code == 404:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Order this id not found"
                ) from er
            raise

        products = []
        total_amount = 0
        for item in order.items:
            total_price = item.price * item.quantity
            products.append({
                "product_name": item.product_name,
                "quantity": item.quantity,
                "total_price": total_price,
            })
            total_amount += total_price

        return products, total_amount

        