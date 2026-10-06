from pathlib import Path
from typing import List, ClassVar, Union
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

class Settings(BaseSettings):

    DEBUG: bool = True
    APP_NAME: str = "OrderFlow_Microservices"
    load_dotenv()

    # POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    # POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    # POSTGRES_HOST: str = os.getenv("POSTGRES_HOST")
    # POSTGRES_PORT: int = os.getenv("POSTGRES_PORT")
    # POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    # MEGA_SUPER_PUPER_SECRET_KEY: str = os.getenv("SECRET_KEY")

    CORS_ORIGIN: Union[List[str], str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:5500",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5500",
    ]

    @property
    def get_url_db(self) -> str:
        return "Тут будет адрес"

settings = Settings()