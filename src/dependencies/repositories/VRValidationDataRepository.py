from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.database.db_session import get_db
from dependencies.database.db_models import VRValidationData


class VRValidationDataRepository:

    @staticmethod
    async def save(
            data: VRValidationData,
            session: AsyncSession = Depends(get_db)
    ) -> VRValidationData:

        session.add(data)
        await session.commit()
        return data


    @staticmethod
    async def find_by_uid(
            object_id: int,
            session: AsyncSession = Depends(get_db)
    ) -> VRValidationData:

        result = await session.execute(
            select(VRValidationData).where(
                VRValidationData.vr_zif_objects_id == object_id
            )
        )
        data = result.scalars().first()
        if not data:
            raise HTTPException(status_code=404, detail="VR ZIF Object not found")
        return data
