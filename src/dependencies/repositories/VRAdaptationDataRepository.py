from datetime import datetime
from typing import Sequence

from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.db_session import get_db
from dependencies.db_models import VRAdaptationData, VRZifObjects



class VRAdaptationDataRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(
            self,
            object_id: int,
            name: str,
            choke_value_adapt: float,
            choke_percent_adapt: float,
            date_start: datetime,
            date_end: datetime,
    ):
        obj = VRAdaptationData(
            vr_zif_objects_id=object_id,
            name=name,
            choke_value_adapt=choke_value_adapt,
            choke_percent_adapt=choke_percent_adapt,
            date_start=date_start,
            date_end=date_end,
            creation_date=datetime.now(),
        )
        self.session.add(obj)
        await self.session.commit()
        return obj


    async def find_adapt_by_name(
            self,
            name: str,
    ) -> VRAdaptationData:

        result = await self.session.execute(
            select(VRAdaptationData).where(
                VRAdaptationData.name == name,
            )
        )
        data = result.scalars().first()
        if not data:
            raise HTTPException(status_code=404, detail=f"VRAdaptationDataRepository.find_by_name failed")
        return data


    async def find_all_by_object_id(
            self,
            object_id: int,
    ) -> Sequence[VRAdaptationData]:

        result = await self.session.execute(
            select(VRAdaptationData).where(
                VRAdaptationData.vr_zif_objects_id == object_id
            )
        )
        return result.scalars().all()


    async def find_active_by_object_id(
            self,
            object_uid: str,
    ) -> VRAdaptationData:

        result = await self.session.execute(
            select(VRAdaptationData)
            .join(VRZifObjects, VRAdaptationData.vr_zif_objects_id == VRZifObjects.id)
            .where(
                VRZifObjects.zif_uid == object_uid,
                VRAdaptationData.id == VRZifObjects.active_adaptation_value_id
            )
            .limit(1)
        )
        data = result.scalars().first()
        if not data:
            raise HTTPException(status_code=404, detail=f"VRAdaptationDataRepository.find_active_by_object_id failed")
        return data
