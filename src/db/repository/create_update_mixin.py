from sqlalchemy import select
from db.repository import BaseRepository

IdType = int


class CreateUpdateMixin[ModelType](BaseRepository):
    model: ModelType

    async def create(self, data: dict) -> ModelType:
        obj = self.model(**data)
        self.session.add(obj)
        await self.session.flush()
        return await self._get_object(obj.id)

    async def _get_object(self, data_id: IdType) -> ModelType:
        query = (
            select(self.model)
            .where(self.model.id == data_id)
            .execution_options(populate_existing=True)
        )
        result = await self.session.scalar(query)
        return result
