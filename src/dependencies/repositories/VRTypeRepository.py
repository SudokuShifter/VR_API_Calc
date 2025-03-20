from typing import Sequence

from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.database.db_session import get_db
from dependencies.database.db_models import VRType


class VRTypeRepository:

    def __init__(self, alchemy_model):
        self.model = alchemy_model


    async def find_all(
            self,
            session: AsyncSession = Depends(get_db)
    ) -> Sequence[VRType]:
        
        result = await session.execute(select(self.model))
        return result.scalars().all()


    async def find_by_uid(
            self,
            uid: str,
            session: AsyncSession = Depends(get_db)
    ) -> VRType:

        result = await session.execute(
            select(self.model).where(self.model.id == uid)
        )
        obj = result.scalars().first()
        if not obj:
            raise HTTPException(status_code=404, detail="Object not found")
        return obj
