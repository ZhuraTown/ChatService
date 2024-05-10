from typing import Sequence

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class ApiConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="API_")

    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = False
    WORKERS: int = 4
    ALLOWED_HOSTS: Sequence[str] = ["*"]


api_settings = ApiConfig()