from typing import Sequence

from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.database.db_session import get_db
from dependencies.database.db_models import VRZifObjects


# Репозитории
class VRZifObjectsRepository:

    def __init__(self, alchemy_model):
        self.model = alchemy_model


    async def save(
            self,
            obj: VRZifObjects,
            session: AsyncSession = Depends(get_db)
    ) -> VRZifObjects:

        session.add(obj)
        await session.commit()
        return obj


    async def find_by_uid(
            self,
            zif_uid: str,
            session: AsyncSession = Depends(get_db)
    ) -> VRZifObjects:

        result = await session.execute(
            select(self.model).where(self.model.zif_uid == zif_uid)
        )
        obj = result.scalars().first()
        if not obj:
            raise HTTPException(status_code=404, detail="Object not found")
        return obj


    async def find_by_id(
            self,
            _id: int,
            session: AsyncSession = Depends(get_db)
    ) -> VRZifObjects:

        result = await session.execute(
            select(self.model).where(self.model.id == _id)
        )
        obj = result.scalars().first()
        if not obj:
            raise HTTPException(status_code=404, detail="Object not found")
        return obj


    async def find_all_active(
            self,
            session: AsyncSession = Depends(get_db)
    ) -> Sequence[VRZifObjects]:

        result = await session.execute(
            select(self.model).where(
                self.model.active_adaptation_value_id.is_not(None)
            )
        )
        return result.scalars().all()


    async def find_all(
            self,
            session: AsyncSession = Depends(get_db)
    ) -> Sequence[VRZifObjects]:

        result = await session.execute(select(self.model))
        return result.scalars().all()