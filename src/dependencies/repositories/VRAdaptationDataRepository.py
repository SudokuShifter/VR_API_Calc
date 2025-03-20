from typing import Sequence

from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.database.db_session import get_db
from dependencies.database.db_models import VRAdaptationData, VRZifObjects


class VRAdaptationDataRepository:

    @staticmethod
    async def save(
            data: VRAdaptationData,
            session: AsyncSession = Depends(get_db)
    ) -> VRAdaptationData:

        session.add(data)
        await session.commit()
        return data


    @staticmethod
    async def find_by_name_and_object_id(
            name: str,
            object_id: int,
            session: AsyncSession = Depends(get_db)
    ) -> VRAdaptationData:

        result = await session.execute(
            select(VRAdaptationData).where(
                VRAdaptationData == name,
                VRAdaptationData.vr_zif_objects_id == object_id
            )
        )
        data = result.scalars().first()
        if not data:
            raise HTTPException(status_code=404, detail=f"VRAdaptationDataRepository.find_by_name_and_object_id failed")
        return data


    @staticmethod
    async def find_all_by_object_id(
            object_id: int,
            session: AsyncSession = Depends(get_db)
    ) -> Sequence[VRAdaptationData]:

        result = await session.execute(
            select(VRAdaptationData).where(
                VRAdaptationData.vr_zif_objects_id == object_id
            )
        )
        return result.scalars().all()


    @staticmethod
    async def find_active_by_object_id(
            object_uid: str,
            session: AsyncSession = Depends(get_db)
    ) -> VRAdaptationData:

        result = await session.execute(
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