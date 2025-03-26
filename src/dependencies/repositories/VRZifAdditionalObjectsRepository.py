from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.db_session import get_db
from dependencies.db_models import VRZifAdditionalObjects
from typing_extensions import Sequence


class VRZifAdditionalObjectsRepository:

    def __init__(self, session: AsyncSession):
        self.session = session


    async def find_by_name_and_main_object(
            self,
            object_name: str,
    ) -> VRZifAdditionalObjects:

        result = await self.session.execute(
            select(VRZifAdditionalObjects).where(
                VRZifAdditionalObjects.name == object_name
            )
        )
        obj = result.scalars().first()
        if not obj:
            raise HTTPException(status_code=404, detail="Object not found")
        return obj

    async def find_all(self) -> Sequence[VRZifAdditionalObjects]:

        result = await self.session.execute(
            select(VRZifAdditionalObjects)
        )
        return result.scalars().all()

