from datetime import datetime

from sqlalchemy import update

from db.repository import BaseRepository

IdType = int


class DeleteMixin[ModelType](BaseRepository):
    model: ModelType

    async def delete(self, object_id: IdType) -> None:
        await self.session.execute(
            update(self.model)
            .where(self.model.id == object_id)
            .values(deleted_at=datetime.utcnow())
        )
        await self.session.flush()
