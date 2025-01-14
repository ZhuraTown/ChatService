from sqlalchemy import select

from db.repository import BaseRepository

IdType = int | str


class RetrieveMixin[ModelType](BaseRepository):
    model: ModelType

    async def find_by_id(self, data_id: IdType) -> ModelType | None:
        data_id = data_id if isinstance(data_id, int) else int(data_id)
        result = await self.session.execute(
            select(self.model).filter_by(id=data_id)
        )
        obj = result.unique().scalars().one()
        return obj

    async def find_by(self, filter_by: dict) -> ModelType | None:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
