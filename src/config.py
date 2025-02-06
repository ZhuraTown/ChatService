from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from sqlalchemy import URL

load_dotenv()


class InfrastructureSettings(BaseSettings):
    db_user: str
    db_password: str
    db_name: str
    db_host: str
    db_port: int

    @property
    def postgres_dsn(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
        ).render_as_string(hide_password=False)


class AuthenticationSetting(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str


class Settings(BaseSettings):
    infrastructure: InfrastructureSettings = InfrastructureSettings()
    authentication: AuthenticationSetting = AuthenticationSetting()


settings = Settings()


def get_auth_data():
    return {"secret_key": settings.authentication.SECRET_KEY, "algorithm": settings.authentication.ALGORITHM}