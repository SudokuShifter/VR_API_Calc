from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.db_session import get_db
from dependencies.db_models import VRValidationData


class VRValidationDataRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(
            self,
            data: VRValidationData,
    ) -> VRValidationData:

        self.session.add(data)
        await self.session.commit()
        return data


    async def find_by_uid(
            self,
            object_id: int
    ) -> VRValidationData:
        print(self.session)
        result = await self.session.execute(
            select(VRValidationData).where(
                VRValidationData.vr_zif_objects_id == object_id
            )
        )
        data = result.scalars().first()
        if not data:
            raise HTTPException(status_code=404, detail="VR ZIF Object not found")
        return data
