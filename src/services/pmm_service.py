import datetime
from importlib.metadata import always_iterable
from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel, Field

from services.vr_storage_service import VRStorageService


class VRFmmWebApiService:

    async def exec_validate_task_ns(self, data, obj_name):
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
        vr_validation_data = await self.vr_storage_service.find_validation_data_by_object_id(
            object_id=object_id
        )
        if not vr_validation_data:
            vr_validation_data = {'id': 0, 'object_id': vr_zif_object.id, 'wct': 0.0,
                                  'gas_condensate_factor': 0.0, 'date': datetime.datetime.now()}
        """
        Понять где брать подобный json
        {
          "q_gas_timed": [
            9.25925925925926,
            10.185185185185185,
            11.11111111111111,
            12.037037037037036,
            12.962962962962962
          ],
          "q_gc_timed": [
            0.00011574074074074075,
            0.00012731481481481483,
            0.00013888888888888892,
            0.000150462962962963,
            0.0001620370370370371
          ],
          "q_wat_timed": [
            0.00011574074074074075,
            0.00012731481481481483,
            0.00013888888888888892,
            0.000150462962962963,
            0.0001620370370370371
          ]
        }
        """
        # Выполняем задачу валидации через API
        validate_task_solution = await self.vr_fmm_web_api_service.exec_validate_task_ns(
            {"object_id": object_id, "date_start": date_start, "date_end": date_end},
            vr_zif_object.name
        )

        vr_validation_data.wct = validate_task_solution.solution.wct
        vr_validation_data.gas_condensate_factor = validate_task_solution.solution.gas_condensate_factor
        await self.vr_storage_service.save_validation_data(vr_validation_data)

        # Возвращаем результат валидации
        # return VRValidationDataResponse(
        #     wct=validate_task_solution.solution.wct,
        #     gas_condensate_factor=validate_task_solution.solution.gas_condensate_factor,
        #     object_name=vr_zif_object.name
        # )


    async def get_validate_data(
            self,
            object_id: int
    ):
        return await self.vr_storage_service.find_validation_data_by_object_id(
            object_id=object_id
        )


    async def get_all_adaptation_data(
            self,
            object_id: int
    ):
        return await self.vr_storage_service.find_all_adaptation_data_by_object_id(
            object_id=object_id
        )


    async def get_active_adaptation_data(
            self,
            object_id: int
    ):
        return await self.vr_storage_service.find_active_adaptation_data_by_object_id(
            object_id=object_id
        )


    async def set_validation_data(
            self,
            object_id: int,
            is_user_value: bool,
            wct: float,
            gas_condensate_factor: float
    ):
        validation_data = await self.vr_storage_service.find_validation_data_by_object_id(
            object_id=object_id
        )
        if validation_data:
            validation_data.wct = wct
            validation_data.gas_condensate_factor = gas_condensate_factor
            validation_data.is_user_value = is_user_value
        await self.vr_storage_service.save_validation_data(validation_data)


    async def set_active_adaptation_value(
            self,
            object_id: int,
            name: str
    ):
        obj = await self.vr_storage_service.get_object_by_id(
            _id=object_id
        )
        vr_adapt_data = await self.vr_storage_service.find_adaptation_data_by_name_and_object_id(
            name=name, object_id=object_id
        )
        if obj and vr_adapt_data:
            obj.active_adaptation_value_id = vr_adapt_data.id
        await self.vr_storage_service.save_main_object(obj)







