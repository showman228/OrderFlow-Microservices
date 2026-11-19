from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from notification_service.app.database import init_db
from notification_service.app.config import settings
import httpx

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    app.state.order_client = httpx.AsyncClient(base_url=settings.ORDER_SERVICE_URL)
    yield
    await app.state.order_client.aclose()


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=settings.static_dir), name="static")


@app.get("/")
async def main():
    return {"message": "Welcome to Notification-Service", "docs": "/docs"}


@app.get("/health")
async def health():
    return {"status": "200"}