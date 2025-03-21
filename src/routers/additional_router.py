from fastapi import (
    APIRouter,
    Query
)

from services.dependencies import VRStorage


additional_router = APIRouter()


@additional_router.get("/api/v1/type-calculation/all")
async def all_type_calculation(vr_storage: VRStorage):
    """
    Получает все типы расчетов, доступные в системе.
    """
    return await vr_storage.get_all_main_objects()


@additional_router.get("/api/v1/type-calculation/")
async def type_calculation(
        vr_storage: VRStorage,
        object_uid: str = Query(..., description='Идентификатор объекта')
):
    """
    Получает тип расчета по идентификатору объекта (object_uid).
    """
    return await vr_storage.get_object_by_uid(object_uid)


@additional_router.put('/api/v1/type-calculation/set/')
async def type_calculation_set(
        vr_storage: VRStorage,
        object_uid: str = Query(..., description='Идентификатор объекта'),
        type_value: str = Query(..., description='Значение типа расчета')
):
    """
    Устанавливает активный тип расчета для объекта по его идентификатору
    """
    obj = await vr_storage.get_object_by_uid(object_uid)
    await vr_storage.set_type_calculation(obj, type_value)
    return {'message': f'Тип расчета обновлён {type_value} для {obj}'}