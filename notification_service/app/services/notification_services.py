from httpx import HTTPStatusError, RequestError, TimeoutException
from sqlalchemy.ext.asyncio import AsyncSession
from notification_service.app.api_clients.order_client import OrderClient
from notification_service.app.repository.notification_repository import (
    NotificationRepository,
)
from notification_service.app.schemas.notification import (
    NotificationCreate,
    NotificationResponse,
)
from fastapi import status, HTTPException


class NotificationService:
    def __init__(self, order_client: OrderClient, db: AsyncSession):
        self.client = order_client
        self.crud = NotificationRepository(db)

    async def get_notification_by_user_id(
        self, user_id: int, limit: int = 20, offset: int = 0
    ) -> list[NotificationResponse]:
        notifs = await self.crud.get_notification_by_user_id(user_id, limit, offset)
        return [NotificationResponse.model_validate(notif) for notif in notifs]

    async def get_notification_by_id(self, notif_id: int) -> NotificationResponse:
        notif = await self.crud.get_notification_by_id(notif_id)
        if notif is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification by this id not found",
            )
        return NotificationResponse.model_validate(notif)

    async def create_order_created_notification(
        self, order_id: int, user_id: int, amount: float
    ) -> NotificationResponse:
        products, user_id_from_order = await self._build_products_summary(order_id)

        if user_id != user_id_from_order:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User id does not match",
            )

        items_text = ", ".join(
            f"{product['product_name']} x{product['quantity']}" for product in products
        )
        message = (
            f"Вы оформили заказ №{order_id}: {items_text} "
            f"на сумму {amount:.2f}"
        )

        notif_data = NotificationCreate(
            user_id=user_id,
            order_id=order_id,
            status="created",
            total_price=amount,
            message=message,
        )

        notification = await self.crud.create(notif_data)
        return NotificationResponse.model_validate(notification)

    async def create_notification_for_pay(
        self, order_id: int, user_id: int, amount: float
    ) -> NotificationResponse:
        message = f"Вы оплатили заказ №{order_id} на сумму {amount:.2f}"

        notif_data = NotificationCreate(
            user_id=user_id,
            order_id=order_id,
            status="paid",
            total_price=amount,
            message=message,
        )

        notification = await self.crud.create(notif_data)
        return NotificationResponse.model_validate(notification)

    async def delete_notification(self, notif_id: int) -> bool:
        notif = await self.crud.delete(notif_id)
        if not notif:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification by this id not found",
            )
        return True

    async def _build_products_summary(self, order_id: int):
        try:
            order = await self.client.get_order(order_id)
        except TimeoutException as exc:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Order service did not respond in time",
            ) from exc
        except RequestError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Could not connect to order service",
            ) from exc
        except HTTPStatusError as exc:
            if exc.response.status_code == status.HTTP_404_NOT_FOUND:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Order with this id not found",
                ) from exc

            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Order service returned an unsuccessful response",
            ) from exc


        products = []
        for item in order.items:
            products.append(
                {
                    "product_name": item.product_name,
                    "quantity": item.quantity,
                }
            )

        return products, order.user_id
