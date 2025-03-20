from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.database.db_session import get_db
from dependencies.database.db_models import VRZifAdditionalObjects


class VRZifAdditionalObjectsRepository:

    def __init__(self, alchemy_model):
        self.model = alchemy_model


    async def find_by_name_and_main_object(
            self,
            object_uid: str,
            object_name: str,
            session: AsyncSession = Depends(get_db)
    ) -> VRZifAdditionalObjects:

        result = await session.execute(
            select(self.model).where(
                self.model.zif_uid == object_uid,
                self.model.name == object_name
            )
        )
        obj = result.scalars().first()
        if not obj:
            raise HTTPException(status_code=404, detail="Object not found")
        return obj
