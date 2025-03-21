from typing import Sequence

from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.db_session import get_db
from dependencies.db_models import VRZifObjects


class VRZifObjectsRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(
            self,
            obj: VRZifObjects
    ) -> VRZifObjects:

        self.session.add(obj)
        await self.session.commit()
        return obj


    async def find_by_uid(
            self,
            zif_uid: str
    ) -> VRZifObjects:

        result = await self.session.execute(
            select(VRZifObjects).where(
                VRZifObjects.zif_uid == zif_uid
            )
        )
        obj = result.scalars().first()
        if not obj:
            raise HTTPException(status_code=404, detail="Object not found")
        return obj


    @staticmethod
    async def find_by_id(
            _id: int,
            session: AsyncSession = Depends(get_db)
    ) -> VRZifObjects:

        result = await session.execute(
            select(VRZifObjects).where(
                VRZifObjects.id == _id
            )
        )
        obj = result.scalars().first()
        if not obj:
            raise HTTPException(status_code=404, detail="Object not found")
        return obj


    @staticmethod
    async def find_all_active(
            session: AsyncSession = Depends(get_db)
    ) -> Sequence[VRZifObjects]:

        result = await session.execute(
            select(VRZifObjects).where(
                VRZifObjects.active_adaptation_value_id.is_not(None)
            )
        )
        return result.scalars().all()


    @staticmethod
    async def find_all(
            session: AsyncSession = Depends(get_db)
    ) -> Sequence[VRZifObjects]:

        result = await session.execute(select(VRZifObjects))
        return result.scalars().all()