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

    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = False
    DEBUG: bool = False
    WORKERS: int = 4
    ALLOWED_HOSTS: Sequence[str] = ["*"]



class AppSettings(BaseSettings):
    infrastructure: InfrastructureSettings = InfrastructureSettings()
    api_settings: APISettings = APISettings()



settings = AppSettings()
