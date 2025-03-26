from datetime import datetime

from fastapi import (
    APIRouter,
    Query
)

from src.schemas.VRZifObjects import VRZifObjectsPyd
from src.schemas.VRValidationData import VRValidationDataPyd
from src.schemas.VRAdaptationData import VRAdaptationDataPyd
from services.dependencies import (
    PMMServiceDep,
    VRCoreDep,
    VRStorageDep
)
from starlette import status

adapt_router = APIRouter()


############################# Adapt-routers


@adapt_router.get('/api/v1/validate',
                  status_code=status.HTTP_200_OK,
                  summary='Выполнить расчет данных для валидации за метку времени'
                  )
async def get_task_validate_value(
        vr_core: VRCoreDep,
        vr_storage: VRStorageDep,
        pmm_service: PMMServiceDep,
        time_left: datetime = Query(..., description="2021-01-01T00:00:00Z"),
        time_right: datetime = Query(..., description="2021-01-01T00:00:00Z"),
        well_id: str = Query(..., description='ID модели'),
):
    """
    Выполняет расчет данных для валидации на основе переданных параметров.
    """
    time_left = time_left.strftime('%Y-%m-%dT%H:%M:%SZ')
    time_right = time_right.strftime('%Y-%m-%dT%H:%M:%SZ')
    data = await vr_core.get_data_for_validate_by_range(
        time_left=time_left,
        time_right=time_right,
        well_id=well_id
    )
    vr_storage.set_validation_data(VRValidationDataPyd(**data))
    # Сделать сохранение данных валидации
    return await pmm_service.execute_validate_task(data=data)


@adapt_router.get('/api/v1/validate/get')
async def get_validate_data(
        vr_storage: VRStorageDep,
        object_id: int = Query(..., description='Object ID'),
):
    """
    Получает данные валидации из базы данных по идентификатору объекта.
    """
    return await vr_storage.find_validation_data_by_object_id(object_id=object_id)


@adapt_router.put('/api/v1/validate/set')
async def put_validate_data(
        vr_storage: VRStorageDep,
        object_id: int = Query(..., description='Object ID'),
        is_user_value: bool = Query(..., description='Is user value'),
        wct: float = Query(..., description='Значение обводненности'),
        gas_condensate_factor: float = Query(..., description='Газовый конденсатный фактор')
):
    """
    Устанавливает данные валидации для объекта.
    """
    return await vr_storage.set_validation_data(object_id=object_id, is_user_value=is_user_value,
                                                wct=wct, gas_condensate_factor=gas_condensate_factor)


@adapt_router.get('/api/v1/adaptation',
                  status_code=status.HTTP_200_OK,
                  summary='Выполнить задачу адаптации')
async def get_adaptation_value(
        vr_core: VRCoreDep,
        adapt_validate_service: PMMServiceDep,
        well_id: int = Query(..., description='Object ID'),
        time_left: datetime = Query(..., description="2021-01-01T00:00:00Z"),
        time_right: datetime = Query(..., description="2021-01-01T00:00:00Z"),
        name: str = Query(..., description='Имя адаптации')
):
    """
    Считает данные адаптации без их активации
    """
    time_left = time_left.strftime('%Y-%m-%dT%H:%M:%SZ')
    time_right = time_right.strftime('%Y-%m-%dT%H:%M:%SZ')
    data = await vr_core.get_data_for_adapt_by_range(time_left=time_left, time_right=time_right, well_id=well_id)
    # Сделать сохранение данных адаптации
    return await adapt_validate_service.execute_adapt_task(data=data)


@adapt_router.get('/api/v1/adaptation/all')
async def get_all_adaptation_data(
        vr_storage: VRStorageDep,
        object_id: int = Query(..., description='Object ID'),
):
    """
    Получает все данные адаптации для объекта по его идентификатору.
    """
    return await vr_storage.find_all_adaptation_data_by_object_id(object_id=object_id)


@adapt_router.get('/api/v1/adaptation/active')
async def get_active_adaptation_data(
        vr_storage: VRStorageDep,
        object_id: int = Query(..., description='Object ID'),
):
    """
    Получает активные данные адаптации для объекта по его идентификатору.
    """
    return await vr_storage.find_active_adaptation_data_by_object_id(object_id=object_id)


@adapt_router.put('/api/v1/adaptation/set')
async def set_active_adaptation_value(
        vr_storage: VRStorageDep,
        object_id: int = Query(..., description='Object ID'),
        name: str = Query(..., description='Имя адаптации')
):
    return await vr_storage.set_adaptation_data(object_id, name)


############################# FMM-routers


fmm_router = APIRouter()


@fmm_router.get('/api/v1/fmm')
async def execute_fmm_task(
        adapt_validate_service: PMMServiceDep,
        object_id: int = Query(..., description='Object ID'),
        time: str = Query(..., description='Момент времени, для которого выполняется задача')
):
    """
    Выполняет задачу FMM
    для указанного объекта в определенный момент времени.
    """
    pass


@fmm_router.get('/api/v1/fmm/duration')
async def execute_fmm_duration(
        adapt_validate_service: PMMServiceDep,
        object_id: int = Query(..., description='Object ID'),
        time_left: str = Query(..., description='Time left'),
        time_right: str = Query(..., description='Time right')
):
    """
    Выполняет задачу FMM для указанного объекта в течение заданного временного интервала
    """
    pass


@fmm_router.get('/api/v1/fmm/duration/parallel')
async def execute_fmm_duration_parallel(
        adapt_validate_service: PMMServiceDep,
        object_id: int = Query(..., description='Object ID'),
        time_left: str = Query(..., description='Time left'),
        time_right: str = Query(..., description='Time right')
):
    """
    Выполняет задачу FMM для указанного объекта в течение заданного временного интервала параллельно
    (с использованием многопоточности или распределенных вычислений).
    """
    pass