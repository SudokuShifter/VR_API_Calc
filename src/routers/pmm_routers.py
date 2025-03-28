from datetime import datetime

from fastapi import (
    APIRouter,
    Query
)


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
                  summary='Выполнить расчет данных для валидации за диапазон времени'
                  )
async def get_task_validate_value(
        vr_core: VRCoreDep,
        vr_storage: VRStorageDep,
        pmm_service: PMMServiceDep,
        date_start: datetime = Query(..., description="2021-01-01T00:00:00Z"),
        date_end: datetime = Query(..., description="2021-01-01T00:00:00Z"),
        well_id: str = Query(..., description='ID модели'),
):
    """
    Выполняет расчет данных для валидации на основе переданных параметров.
    """
    time_left = date_start.strftime('%Y-%m-%dT%H:%M:%SZ')
    time_right = date_end.strftime('%Y-%m-%dT%H:%M:%SZ')
    data = await vr_core.get_data_for_validate_by_range(
        time_left=time_left,
        time_right=time_right,
        well_id=well_id
    )
    vr_obj = await vr_storage.get_object_by_name(name=f'well_{well_id}')
    validate_data = await pmm_service.execute_validate_task(data=data)
    data_for_save = validate_data.get('solution')
    return validate_data
    if validate_data:
        await vr_storage.save_validation_data(
            object_id=vr_obj.id, wct=data_for_save['wct'],
            gas_condensate_factor=data_for_save['gas_condensate_factor'],
            is_user_value=False
        )
    return validate_data


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
        vr_storage: VRStorageDep,
        adapt_validate_service: PMMServiceDep,
        well_id: int = Query(..., description='Well ID'),
        date_start: datetime = Query(..., description="2021-01-01T00:00:00Z"),
        date_end: datetime = Query(..., description="2021-01-01T00:00:00Z"),
        name: str = Query(..., description='Имя адаптации')
):
    """
    Считает данные адаптации без их активации
    """
    time_left = date_start.strftime('%Y-%m-%dT%H:%M:%SZ')
    time_right = date_end.strftime('%Y-%m-%dT%H:%M:%SZ')
    vr_obj = await vr_storage.get_object_by_name(name=f'well_{well_id}')
    data = await vr_core.get_data_for_adapt_by_range(time_left=time_left, time_right=time_right, well_id=well_id)
    return data
    adapt_data = await adapt_validate_service.execute_adapt_task(data=data)
    adapt_data_for_save = adapt_data.get('solution')
    await vr_storage.save_adaptation_data(object_id=vr_obj.id, name=name,
                                          choke_value_adapt=adapt_data_for_save['c_choke_adapt'],
                                          choke_percent_adapt=adapt_data_for_save['d_choke_percent_adapt'],
                                          date_start=date_start.replace(tzinfo=None),
                                          date_end=date_end.replace(tzinfo=None)
                                          )
    return adapt_data


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
        well_id: str = Query(..., description='Object ID'),
        name: str = Query(..., description='Имя адаптации')
):
    return await vr_storage.set_adaptation_data(well_id, name)


############################# FMM-routers


fmm_router = APIRouter()


@fmm_router.get('/api/v1/fmm')
async def execute_fmm_task(
        pmm_service: PMMServiceDep,
        vr_storage: VRStorageDep,
        vr_core: VRCoreDep,
        well_id: int = Query(..., description='Well ID'),
        time: datetime = Query(..., description='Момент времени, 2021-01-01T00:00:00Z')
):
    """
    Выполняет задачу FMM
    для указанного объекта в определенный момент времени.
    """
    time = time.strftime('%Y-%m-%dT%H:%M:%SZ')
    adapt_data = await vr_storage.find_active_adaptation_data_by_object_name(name=f'well_{well_id}')
    main_obj = await vr_storage.get_object_by_name(name=f'well_{well_id}')
    validate_data = await vr_storage.find_validation_data_by_object_id(object_id=main_obj.id)
    data = await vr_core.get_data_for_adapt_by_time_point(time=time, well_id=well_id)
    data['d_choke_percent_adapt'] = adapt_data.choke_percent_adapt
    data['c_choke_adapt'] = adapt_data.choke_value_adapt
    data['gas_condensate_factor'] = validate_data.gas_condensate_factor
    data['wct'] = validate_data.wct
    # Нихера не доделано (Завтра спросить Алексея)
    return await pmm_service.execute_fmm_task(data=data)


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