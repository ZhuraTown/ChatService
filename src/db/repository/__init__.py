from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from db.orm import Base


class BaseRepository:
    model: Base
    session: AsyncSession
    query: Select | None = None

    def __init__(self, session):
        self.session = session

