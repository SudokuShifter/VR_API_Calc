from datetime import datetime

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
            object_id, is_user_value,
            wct, gas_condensate_factor,
    ) -> VRValidationData:

        obj = VRValidationData(vr_zif_objects_id = object_id,
                               wct = wct,
                               gas_condensate_factor = gas_condensate_factor,
                               is_user_value = is_user_value,
                               date = datetime.now())
        self.session.add(obj)
        await self.session.commit()
        return obj


    async def find_by_obj_id(
            self,
            object_id: int
    ) -> VRValidationData:

        result = await self.session.execute(
            select(VRValidationData).where(
                VRValidationData.vr_zif_objects_id == object_id
            )
        )
        data = result.scalars().first()
        if not data:
            raise HTTPException(status_code=404, detail="Adaptation object not found")
        return data


    async def set_validation_data(
            self,
            object_id: int,
            is_user_value: bool,
            wct: float,
            gas_condensate_factor: float
    ):
        self.save(object_id=object_id, is_user_value=is_user_value,
            wct=wct, gas_condensate_factor=gas_condensate_factor)
        return {'success': True, 'detail': object_id}
