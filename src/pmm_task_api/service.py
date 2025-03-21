
from pydantic import BaseModel, Field

from src.dependencies import VRStorageService


class VRValidationData(BaseModel):
    id: int = Field(...)
    object_id: int = Field(...)
    wct: float = Field(...)
    gas_condensate_factor: float = Field(...)



class VRFmmWebApiService:
    pass


class AdaptationAndValidationService:
    def __init__(self):
        self.vr_storage_service = VRStorageService()
        self.vr_fmm_web_api_service = VRFmmWebApiService()


    async def execute_task_validation(
            self,
            object_id: int,
            date_start: str,
            date_end: str
    ):

        # Получаем объект по ID
        vr_zif_object = await self.vr_storage_service.get_object_by_uid(
            object_id=object_id
        )

        # Получаем данные валидации или создаем новую запись
        vr_validation_data = await self.vr_storage_service.find_validation_data_without_check(object_id)
        if not vr_validation_data:
            vr_validation_data = VRValidationData(id=0, object_id=vr_zif_object.id, wct=0.0, gas_condensate_factor=0.0)

        # Выполняем задачу валидации через API
        validate_task_solution = await self.vr_fmm_web_api_service.exec_validate_task_ns(
            {"object_id": object_id, "date_start": date_start, "date_end": date_end},
            vr_zif_object.name
        )

        # Сохраняем или обновляем данные валидации
        vr_validation_data.wct = validate_task_solution.solution.wct
        vr_validation_data.gas_condensate_factor = validate_task_solution.solution.gas_condensate_factor
        await self.vr_storage_service.save_validation_data(vr_validation_data)

        # Возвращаем результат валидации
        # return VRValidationDataResponse(
        #     wct=validate_task_solution.solution.wct,
        #     gas_condensate_factor=validate_task_solution.solution.gas_condensate_factor,
        #     object_name=vr_zif_object.name
        # )

