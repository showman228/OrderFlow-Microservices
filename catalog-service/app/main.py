from fastapi import FastAPI
from contextlib import asynccontextmanager
# from app.database import init_db
from app.config import settings

# async def lifespan(_: FastAPI):
#     await init_db
#     yield


app = FastAPI(title=settings.APP_NAME) # lifespan=lifespan


@app.get("/")
async def main():
    return {"message": "Welcome to Category-Service", "docs": "/docs"}


@app.get("/health")
async def health():
    return {"status": "200"}
