from typing import Sequence

from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.database.db_session import get_db
from dependencies.database.db_models import VRAdaptationData



class VRAdaptationDataRepository:

    def __init__(self, alchemy_model):
        self.model = alchemy_model


    async def save(
            self,
            data: VRAdaptationData,
            session: AsyncSession = Depends(get_db)
    ) -> VRAdaptationData:

        session.add(data)
        await session.commit()
        return data


    async def find_by_name_and_object_id(
            self,
            name: str,
            object_id: int,
            session: AsyncSession = Depends(get_db)
    ) -> VRAdaptationData:

        result = await session.execute(
            select(self.model).where(
                self.model.name == name,
                self.model.vr_zif_objects_id == object_id
            )
        )
        data = result.scalars().first()
        if not data:
            raise HTTPException(status_code=404, detail=f"VRAdaptationDataRepository.find_by_name_and_object_id failed")
        return data


    async def find_all_by_object_id(
            self,
            object_id: int,
            session: AsyncSession = Depends(get_db)
    ) -> Sequence[VRAdaptationData]:

        result = await session.execute(
            select(self.model).where(self.model.vr_zif_objects_id == object_id)
        )
        return result.scalars().all()


    async def find_active_by_object_id(
            self,
            object_id: int,
            session: AsyncSession = Depends(get_db)
    ) -> VRAdaptationData:

        result = await session.execute(
            select(self.model).where(
                self.model.vr_zif_objects_id == object_id,
                self.model.is_active == True  # Пример поля is_active
            )
        )
        data = result.scalars().first()
        if not data:
            raise HTTPException(status_code=404, detail=f"VRAdaptationDataRepository.find_active_by_object_id failed")
        return data