from typing import Sequence, Annotated

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
        print(main_objs)
        if not main_objs:
            for i in self.WELL_IDS:
                self.session.add(VRZifObjects(name=f'well_{i}', hole_project_id=i))

        if not await self.get_all_addi():
            for i in self.OTHER_IDS:
                self.session.add(VRZifAdditionalObjects(name=i))

        await self.session.commit()

    async def save_adaptation_data(self, data: VRAdaptationData) -> VRAdaptationData:
        return await self.adaptation_repo.save(data)


    async def set_adaptation_data(self, object_id: int, name: str) -> VRAdaptationData:
        obj = self.get_object_by_id(_id=object_id)
        data = self.find_adaptation_data_by_name_and_object_id(name=name, object_id=object_id)
        obj.active_adaptation_value_id = data.id
        return await self.zif_objects_repo.save(obj)


    async def set_validation_data(self, object_id: int, is_user_value: bool,
                                  wct: float, gas_condensate_factor: float) -> VRAdaptationData:
        return await self.validation_repo.save(object_id, is_user_value,
                                                wct, gas_condensate_factor)


    async def save_validation_data(self, data: VRValidationData) -> VRValidationData:
        return await self.validation_repo.save(data)


    async def save_main_object(self, obj: VRZifObjects) -> VRZifObjects:
        return await self.zif_objects_repo.save(obj)


    async def get_all_active_objects(self) -> Sequence[VRZifObjects]:
        return await self.zif_objects_repo.find_all_active()


    async def get_all_main_objects(self) -> Sequence[VRZifObjects]:
        return await self.zif_objects_repo.find_all()

    async def get_all_addi(self) -> Sequence[VRZifAdditionalObjects]:
        return await self.additional_objects_repo.find_all()

    async def get_object_by_uid(self, zif_uid: str) -> VRZifObjects:
        return await self.zif_objects_repo.find_by_uid(zif_uid)


    async def get_object_by_id(self, _id: int) -> VRZifObjects:
        return await self.zif_objects_repo.find_by_id(_id)


    async def get_additional_object_by_name_and_main_object(self, object_uid: str, object_name: str) -> VRZifAdditionalObjects:
        return await self.additional_objects_repo.find_by_name_and_main_object(object_uid, object_name)


    async def find_all_adaptation_data_by_object_id(self, object_id: int) -> Sequence[VRAdaptationData]:
        return await self.adaptation_repo.find_all_by_object_id(object_id)


    async def find_active_adaptation_data_by_object_id(self, object_id: int) -> VRAdaptationData:
        return await self.adaptation_repo.find_active_by_object_id(object_id)


    async def find_adaptation_data_by_name_and_object_id(self, name: str, object_id: int) -> VRAdaptationData:
        return await self.adaptation_repo.find_by_name_and_object_id(name, object_id)


    async def find_validation_data_by_object_id(self, object_id: int) -> VRValidationData:
        return await self.validation_repo.find_by_uid(object_id)


    async def find_all_vr_types(self) -> Sequence[VRType]:
        return await self.type_repo.find_all()


    async def find_vr_type_by_uid(self, uid: str) -> VRType:
        return await self.type_repo.find_by_uid(uid)




