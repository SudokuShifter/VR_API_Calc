from typing import Sequence

from dependencies.repositories.VRZifObjectsRepository import VRZifObjectsRepository
from dependencies.repositories.VRAdaptationDataRepository import VRAdaptationDataRepository
from dependencies.repositories.VRValidationDataRepository import VRValidationDataRepository
from dependencies.repositories.VRZifAdditionalObjectsRepository import VRZifAdditionalObjectsRepository
from dependencies.repositories.VRTypeRepository import VRTypeRepository


from dependencies.database.db_models import (
    VRZifObjects,
    VRAdaptationData,
    VRZifAdditionalObjects,
    VRValidationData,
    VRZifObject2AdditionalObject,
    VRType,
    VRSchedulerStatus
)


class VRStorageService:
    def __init__(self):
        self.zif_objects_repo = VRZifObjectsRepository()
        self.adaptation_repo = VRAdaptationDataRepository()
        self.validation_repo = VRValidationDataRepository()
        self.additional_objects_repo = VRZifAdditionalObjectsRepository()
        self.type_repo = VRTypeRepository()


    async def save_adaptation_data(self, data: VRAdaptationData) -> VRAdaptationData:
        return await self.adaptation_repo.save(data)


    async def save_validation_data(self, data: VRValidationData) -> VRValidationData:
        return await self.validation_repo.save(data)


    async def save_main_object(self, obj: VRZifObjects) -> VRZifObjects:
        return await self.zif_objects_repo.save(obj)


    async def get_all_active_objects(self) -> Sequence[VRZifObjects]:
        return await self.zif_objects_repo.find_all_active()


    async def get_all_main_objects(self) -> Sequence[VRZifObjects]:
        return await self.zif_objects_repo.find_all()


    async def get_object_by_uid(self, zif_uid: str) -> VRZifObjects:
        return await self.zif_objects_repo.find_by_uid(zif_uid)


    async def get_object_by_id(self, _id: int) -> VRZifObjects:
        return await self.zif_objects_repo.find_by_id(id)


    async def get_additional_object_by_name_and_main_object(self, object_uid: str, object_name: str) -> VRZifAdditionalObjects:
        return await self.additional_objects_repo.find_by_name_and_main_object(object_uid, object_name)


    async def find_all_adaptation_data_by_object_id(self, object_id: int) -> Sequence[VRAdaptationData]:
        return await self.adaptation_repo.find_all_by_object_id(object_id)


    async def find_active_adaptation_data_by_object_id(self, object_id: int) -> VRAdaptationData:
        return await self.adaptation_repo.find_active_by_object_id(object_id)


    async def find_adaptation_data_by_name_and_object_id(self, name: str, object_id: int) -> VRAdaptationData:
        return await self.adaptation_repo.find_by_name_and_object_id(name, object_id)


    async def find_validation_data_by_object_id(self, object_uid: str) -> VRValidationData:
        return await self.validation_repo.find_by_uid(object_uid)


    async def find_all_vr_types(self) -> Sequence[VRType]:
        return await self.type_repo.find_all()


    async def find_vr_type_by_uid(self, uid: str) -> VRType:
        return await self.type_repo.find_by_uid(uid)