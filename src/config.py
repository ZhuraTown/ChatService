from typing import Sequence

from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv(find_dotenv(".env"))


class InfrastructureSettings(BaseSettings):

    db_user: str
    db_password: str
    db_name: str
    db_host: str
    db_port: int


class APISettings(BaseSettings):

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_RELOAD: bool = False
    API_DEBUG: bool = False
    API_WORKERS: int = 4
    API_ALLOWED_HOSTS: Sequence[str] = ["*"]
    API_VERSION: float | int = 0.0


class AppSettings(BaseSettings):
    infrastructure: InfrastructureSettings = InfrastructureSettings()
    api_settings: APISettings = APISettings()
    debug: bool = False


settings = AppSettings()
