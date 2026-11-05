from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from order_service.app.cache.redis import RedisCache
from order_service.app.services.catalog_client import CatalogClient
from order_service.app.database import get_db

SessionDep = Annotated[AsyncSession, Depends(get_db)]


def get_catalog_client(request: Request) -> CatalogClient:
    return CatalogClient(request.app.state.catalog_client)

def get_cache(request: Request) -> RedisCache:
    return request.app.state.cache

CatalogClientDep = Annotated[CatalogClient, Depends(get_catalog_client)]
CacheDep = Annotated[RedisCache, Depends(get_cache)]