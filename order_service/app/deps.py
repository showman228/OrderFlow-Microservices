from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from order_service.app.database import get_db
from order_service.app.services.catalog_client import CatalogClient

SessionDep = Annotated[AsyncSession, Depends(get_db)]


def get_catalog_client(request: Request) -> CatalogClient:
    return CatalogClient(request.app.state.catalog_client)


CatalogClientDep = Annotated[CatalogClient, Depends(get_catalog_client)]
