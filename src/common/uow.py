import logging

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyUoW:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def commit(self) -> None:
        try:
            await self._session.commit()
        except SQLAlchemyError as err:
            logging.critical(f"Error commit. {err}")
            raise err
        except IntegrityError as err:
            logging.critical(f"Error commit. {err}")
            raise err
        finally:
            await self._session.close()

    async def rollback(self) -> None:
        try:
            await self._session.rollback()
        except SQLAlchemyError as err:
            logging.critical(f"Error rollback. {err}")
            raise err
        finally:
            await self._session.close()
