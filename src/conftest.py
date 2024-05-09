import asyncio

import pytest
from faker import Faker
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from src.infrastructure.db.models.users import User


pytest_plugins = [
    "src.tests.infrastructure.fixtures.fixture_user",
]


@pytest.fixture(scope='session', autouse=True)
async def init_db():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    client.get_io_loop = asyncio.get_event_loop
    db_name = client.chat_test
    await init_beanie(database=db_name, document_models=[User])
    yield client
    await client.drop_database(db_name)


@pytest.fixture()
def faker():
    return Faker("ru_RU")


@pytest.fixture(scope="session")
def event_loop():
    """
    Creates an instance of the default event loop for the test session.
    """
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
