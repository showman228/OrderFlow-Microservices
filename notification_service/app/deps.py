from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from notification_service.app.database import get_db
from notification_service.app.api_clients.order_client import OrderClient

SessionDep = Annotated[AsyncSession, Depends(get_db)]

def get_order_client(request: Request) -> OrderClient:
    return OrderClient(request.app.state.order_client)

OrderClintDep = Annotated[OrderClient, Depends(get_order_client)]