from datetime import datetime
from typing import Sequence, Annotated, List

from loguru import logger

from dependencies.repositories.VRZifObjectsRepository import VRZifObjectsRepository
from dependencies.repositories.VRAdaptationDataRepository import VRAdaptationDataRepository
from dependencies.repositories.VRValidationDataRepository import VRValidationDataRepository
from dependencies.repositories.VRZifAdditionalObjectsRepository import VRZifAdditionalObjectsRepository
from dependencies.repositories.VRTypeRepository import VRTypeRepository

from dependencies.db_session import get_db
from dependencies.db_models import (
    VRZifObjects,
    VRAdaptationData,
    VRZifAdditionalObjects,
    VRValidationData,
    VRZifObject2AdditionalObject,
    VRType,
    VRSchedulerStatus
)
from sqlalchemy.ext.asyncio import AsyncSession


class VRStorageService:

    WELL_IDS = [529, 508, 504, 524, 554, 521, 522, 528, 503, 517, 506,
                552, 501, 511, 507, 505, 502, 513, 516, 510, 525, 2]
    OTHER_IDS = ['ТЛ1 Сепаратор', 'ТЛ1 Манифольд', 'Train2',
                 'ТЛ2 Сепаратор', 'ТЛ2 Манифольд', 'ОБТК', 'СПГ']

    def __init__(self, session: AsyncSession):
        self.zif_objects_repo = VRZifObjectsRepository(session)
        self.adaptation_repo = VRAdaptationDataRepository(session)
        self.validation_repo = VRValidationDataRepository(session)
        self.additional_objects_repo = VRZifAdditionalObjectsRepository(session)
        self.type_repo = VRTypeRepository(session)
        self.session = session

    async def init_db_script(self):
        main_objs = await self.get_all_main_objects()

        if not main_objs:
            for i in self.WELL_IDS:
                self.session.add(VRZifObjects(name=f'well_{i}', hole_project_id=i))
                logger.success(f'Well obj {i} added in DB')
        if not await self.get_all_addi():
            for i in self.OTHER_IDS:
                self.session.add(VRZifAdditionalObjects(name=i))
                logger.success(f'Additional obj {i} added in DB')
        await self.session.commit()


    async def save_adaptation_data(
            self,
            object_id: int,
            name: str,
            choke_value_adapt: List[float],
            choke_percent_adapt: List[float],
            date_start: datetime,
            date_end: datetime
    ) -> VRAdaptationData:

        return await self.adaptation_repo.save(
            object_id=object_id, name=name,
            choke_value_adapt=choke_value_adapt,
            choke_percent_adapt=choke_percent_adapt,
            date_start=date_start, date_end=date_end
        )


    async def set_adaptation_data(self, well_id: str, name: str) -> VRAdaptationData:
        adapt_id = await self.adaptation_repo.find_adapt_by_name(name)
        return await self.zif_objects_repo.set_adaptation_data(
            well_id=well_id,
            adaptation_id=adapt_id.id
        )


    async def set_validation_data(self, object_id: int, is_user_value: bool,
                                  wct: float, gas_condensate_factor: float) -> VRAdaptationData:
        return await self.validation_repo.save(
            object_id=object_id,
            is_user_value=is_user_value,
            wct=wct, gas_condensate_factor=gas_condensate_factor
        )


    async def save_validation_data(self, object_id: int, is_user_value: bool,
                                  wct: float, gas_condensate_factor: float) -> VRValidationData:
        return await self.validation_repo.save(
            object_id=object_id,
            is_user_value=is_user_value,
            wct=wct,
            gas_condensate_factor=gas_condensate_factor
        )


    async def save_main_object(self, obj: VRZifObjects) -> VRZifObjects:
        return await self.zif_objects_repo.save(obj)


    async def get_all_active_objects(self) -> Sequence[VRZifObjects]:
        return await self.zif_objects_repo.find_all_active()


    async def get_all_main_objects(self) -> Sequence[VRZifObjects]:
        return await self.zif_objects_repo.find_all()

    async def get_all_addi(self) -> Sequence[VRZifAdditionalObjects]:
        return await self.additional_objects_repo.find_all()

    async def get_object_by_name(self, name: str) -> VRZifObjects:
        return await self.zif_objects_repo.find_by_name(name)


    async def get_object_by_id(self, _id: int) -> VRZifObjects:
        return await self.zif_objects_repo.find_by_id(_id)


    async def get_additional_object_by_name_and_main_object(self, object_uid: str, object_name: str) -> VRZifAdditionalObjects:
        return await self.additional_objects_repo.find_by_name_and_main_object(object_uid, object_name)


    async def find_all_adaptation_data_by_object_id(self, object_id: int) -> Sequence[VRAdaptationData]:
        return await self.adaptation_repo.find_all_by_object_id(object_id)


    async def find_active_adaptation_data_by_object_name(self, name: int) -> VRAdaptationData:
        return await self.adaptation_repo.find_active_by_object_name(name)


    async def find_adaptation_data_by_name_and_object_id(self, name: str, object_id: int) -> VRAdaptationData:
        return await self.adaptation_repo.find_by_name_and_object_id(name, object_id)


    async def find_validation_data_by_object_id(self, object_id: int) -> VRValidationData:
        return await self.validation_repo.find_by_obj_id(object_id)


    async def find_all_vr_types(self) -> Sequence[VRType]:
        return await self.type_repo.find_all()


    async def find_vr_type_by_uid(self, uid: str) -> VRType:
        return await self.type_repo.find_by_uid(uid)

