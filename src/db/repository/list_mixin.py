from sqlalchemy import Select, select

from db.repository import BaseRepository


class ListMixin[ModelType, FilterSet](BaseRepository):
    model: ModelType
    filter_set: FilterSet

    async def list(self, params: dict) -> list[ModelType]:
        query = select(self.model)
        filtered_query = self.filter_set(query).filter_query(params)
        results = (await self.session.execute(filtered_query)).unique().scalars().all()
        return results

