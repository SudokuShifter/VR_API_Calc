from typing import Sequence

from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.db_session import get_db
from dependencies.db_models import VRType, VRZifObjects


class VRTypeRepository:

    def __init__(self, session: AsyncSession):
        self.session = session


    async def find_all(
            self,
    ) -> Sequence[VRType]:

        result = await self.session.execute(select(VRType))
        return result.scalars().all()


    async def find_by_uid(
            self,
            uid: str,
    ) -> VRType:

        result = await self.session.execute(
            select(VRType).where(
                VRType == uid
            )
        )
        obj = result.scalars().first()
        if not obj:
            raise HTTPException(status_code=404, detail="Object not found")
        return obj


    async def set_type_calculation(
            self,
            obj: VRZifObjects,
            type_value: str
    ):
        stmt = select(VRType).where(VRType.id == type_value)
        result = await self.session.execute(stmt)
        vr_type = result.scalars().first()

        if not vr_type:
            raise HTTPException(status_code=404, detail="Object not found")
        obj.type = vr_type
        self.session.add(obj)
        await self.session.commit()
        return type_value
