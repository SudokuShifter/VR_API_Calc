from typing import Sequence

from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.db_session import get_db
from dependencies.db_models import VRZifObjects, VRAdaptationData


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


    async def find_by_name(
            self,
            name: str
    ) -> VRZifObjects:

        result = await self.session.execute(
            select(VRZifObjects).where(
                VRZifObjects.name == name
            )
        )
        obj = result.scalars().first()
        if not obj:
            raise HTTPException(status_code=404, detail="Object not found")
        return obj


    async def find_by_id(
            self,
            _id: int,
    ) -> VRZifObjects:

        result = await self.session.execute(
            select(VRZifObjects).where(
                VRZifObjects.id == _id
            )
        )
        obj = result.scalars().first()
        if not obj:
            raise HTTPException(status_code=404, detail="Object not found")
        return obj


    async def find_all_active(
            self
    ) -> Sequence[VRZifObjects]:

        result = await self.session.execute(
            select(VRZifObjects).where(
                VRZifObjects.active_adaptation_value_id.is_not(None)
            )
        )
        return result.scalars().all()


    async def find_all(
            self
    ) -> Sequence[VRZifObjects]:

        result = await self.session.execute(select(VRZifObjects))
        return result.scalars().all()


    async def set_adaptation_data(
            self,
            well_id: str,
            adaptation_id: int
    ) -> VRAdaptationData:

        vr_obj = await self.find_by_name(f'well_{well_id}')
        vr_obj.active_adaptation_value_id = adaptation_id
        await self.session.commit()
        return vr_obj
