from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from ..app.database import init_db
from ..app.config import settings

from order_service.app.routers.cart import router as cart_router
from order_service.app.routers.order import router as order_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=settings.static_dir), name="static")

app.include_router(...)
app.include_router(...)


@app.get("/")
async def main():
    return {"message": "Welcome to Order-Service", "docs": "/docs"}


@app.get("/health")
async def health():
    return {"status": "200"}
