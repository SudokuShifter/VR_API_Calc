from typing import Sequence

from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.database.db_session import get_db
from dependencies.database.db_models import VRZifObjects


class VRZifObjectsRepository:

    @staticmethod
    async def save(
            obj: VRZifObjects,
            session: AsyncSession = Depends(get_db)
    ) -> VRZifObjects:

        session.add(obj)
        await session.commit()
        return obj


    @staticmethod
    async def find_by_uid(
            zif_uid: str,
            session: AsyncSession = Depends(get_db)
    ) -> VRZifObjects:

        result = await session.execute(
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