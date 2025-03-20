from typing import Sequence

from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.database.db_session import get_db
from dependencies.database.db_models import VRType


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
            select(VRType).where(VRType == uid)
        )
        obj = result.scalars().first()
        if not obj:
            raise HTTPException(status_code=404, detail="Object not found")
        return obj
