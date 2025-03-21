from typing import Sequence

from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.db_session import get_db
from dependencies.db_models import VRType, VRZifObjects


class VRTypeRepository:

    @staticmethod
    async def find_all(
            session: AsyncSession = Depends(get_db)
    ) -> Sequence[VRType]:

        result = await session.execute(select(VRType))
        return result.scalars().all()


    @staticmethod
    async def find_by_uid(
            uid: str,
            session: AsyncSession = Depends(get_db)
    ) -> VRType:

        result = await session.execute(
            select(VRType).where(
                VRType == uid
            )
        )
        obj = result.scalars().first()
        if not obj:
            raise HTTPException(status_code=404, detail="Object not found")
        return obj


    @staticmethod
    async def set_type_calculation(
            obj: VRZifObjects,
            type_value: str,
            session: AsyncSession = Depends(get_db)
    ):
        stmt = select(VRType).where(VRType.id == type_value)
        result = await session.execute(stmt)
        vr_type = result.scalars().first()

        if not vr_type:
            raise HTTPException(status_code=404, detail="Object not found")
        obj.type = vr_type
        session.add(obj)
        await session.commit()
        return type_value
