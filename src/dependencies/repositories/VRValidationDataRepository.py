from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.database.db_session import get_db
from dependencies.database.db_models import VRValidationData


class VRValidationDataRepository:

    def __init__(self, alchemy_model):
        self.model = alchemy_model


    async def save(
            self,
            data: VRValidationData,
            session: AsyncSession = Depends(get_db)
    ) -> VRValidationData:

        session.add(data)
        await session.commit()
        return data


    async def find_by_uid(
            self,
            object_id: int,
            session: AsyncSession = Depends(get_db)
    ) -> VRValidationData:

        result = await session.execute(
            select(self.model).where(self.model.vr_zif_objects_id == object_id)
        )
        data = result.scalars().first()
        if not data:
            raise HTTPException(status_code=404, detail="VR ZIF Object not found")
        return data
