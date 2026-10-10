from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from ..app.database import init_db
from ..app.config import settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

app.mount("/static", StaticFiles(directory=settings.static_dir), name="static")


@app.get("/")
async def main():
    return {"message": "Welcome to Category-Service", "docs": "/docs"}


@app.get("/health")
async def health():
    return {"status": "200"}
