from fastapi import (
    APIRouter,
    Query
)

from services.dependencies import AdaptValidateService


adapt_router = APIRouter()


############################# Adapt-routers


@adapt_router.get('/api/v1/validate')
async def get_task_validate_value(
        adapt_validate_service: AdaptValidateService,
        object_id: int = Query(..., description='Object ID'),
        time_left: str = Query(..., description='Time left'),
        time_right: str = Query(..., description='Time right'),
):
    """
    Выполняет расчет данных для валидации на основе переданных параметров.
    """
    return await adapt_validate_service.execute_task_validation(
        object_id=object_id, time_left=time_left, time_right=time_right
    )


@adapt_router.get('/api/v1/validate/get')
async def get_validate_data(
        adapt_validate_service: AdaptValidateService,
        object_id: int = Query(..., description='Object ID'),
):
    """
    Получает данные валидации из базы данных по идентификатору объекта.
    """
    return await adapt_validate_service.get_validate_data(
        object_id=object_id
    )


@adapt_router.put('/api/v1/validate/set')
async def put_validate_data(
        adapt_validate_service: AdaptValidateService,
        object_id: int = Query(..., description='Object ID'),
        is_user_value: bool = Query(..., description='Is user value'),
        wct: float = Query(..., description='Значение обводненности'),
        gas_condensate_factor: float = Query(..., description='Газовый конденсатный фактор')
):
    """
    Устанавливает данные валидации для объекта.
    """
    return await adapt_validate_service.set_validation_data(
        object_id=object_id, is_user_value=is_user_value,
        wct=wct, gas_condensate_factor=gas_condensate_factor
    )


@adapt_router.get('/api/v1/adaptation')
async def get_adaptation_value(
        object_id: int = Query(..., description='Object ID'),
        time_left: str = Query(..., description='Time left'),
        time_right: str = Query(..., description='Time right'),
        name: str = Query(..., description='Имя адаптации')
):
    """
    Выполняет расчет коэффициентов адаптации без их активации.
    """
    pass


@adapt_router.get('/api/v1/adaptation/all')
async def get_all_adaptation_data(
        adapt_validate_service: AdaptValidateService,
        object_id: int = Query(..., description='Object ID'),
):
    """
    Получает все данные адаптации для объекта по его идентификатору.
    """
    return await adapt_validate_service.get_all_adaptation_data(
        object_id=object_id
    )


@adapt_router.get('/api/v1/adaptation/active')
async def get_active_adaptation_data(
        adapt_validate_service: AdaptValidateService,
        object_id: int = Query(..., description='Object ID'),
):
    """
    Получает активные данные адаптации для объекта по его идентификатору.
    """
    return await adapt_validate_service.get_active_adaptation_data(
        object_id=object_id
    )


@adapt_router.put('/api/v1/adaptation/set')
async def set_active_adaptation_value(
        adapt_validate_service: AdaptValidateService,
        object_id: int = Query(..., description='Object ID'),
        name: str = Query(..., description='Имя адаптации')
):
    """
    Устанавливает активные данные адаптации для объекта по имени адаптации.
    """
    return await adapt_validate_service.set_active_adaptation_value(
        object_id=object_id, name=name
    )


############################# FMM-routers


fmm_router = APIRouter()


@fmm_router.get('/api/v1/fmm')
async def execute_fmm_task(
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
        object_id: int = Query(..., description='Object ID'),
        time_left: str = Query(..., description='Time left'),
        time_right: str = Query(..., description='Time right')
):
    """
    Выполняет задачу FMM для указанного объекта в течение заданного временного интервала параллельно
    (с использованием многопоточности или распределенных вычислений).
    """
    pass