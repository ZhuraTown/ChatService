from dotenv import load_dotenv
from pydantic import field_validator, MongoDsn
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings

load_dotenv()


class InfrastructureSettings(BaseSettings):
    # MONGO CONFIG
    db_user: str
    db_password: str
    db_name: str
    db_host: str
    db_port: int
    mongo_dsn: MongoDsn | None = None

    @field_validator("mongo_dsn", mode="before")  # noqa
    @classmethod
    def get_mongo_dsn(cls, _, info: ValidationInfo):
        return MongoDsn.build(
            scheme="mongodb+srv",
            username=info.data["db_user"],
            password=info.data["db_password"],
            host=info.data["db_host"],
            port=info.data["db_port"],
            path=info.data["db_name"],
        )

    # REDIS CONFIG
    # redis_host: str
    # redis_port: int
    # redis_db: str
    # redis_dsn: RedisDsn | None = None
    #
    # @field_validator('redis_dsn', mode='before')  # noqa
    # @classmethod
    # def get_redis_dsn(cls, _, info: ValidationInfo):
    #     return RedisDsn.build(
    #         scheme='redis',
    #         host=info.data['redis_host'],
    #         port=info.data['redis_port'],
    #         path=info.data['redis_db'],
    #     )


class Settings(BaseSettings):
    infrastructure: InfrastructureSettings = InfrastructureSettings()


settings = Settings()
