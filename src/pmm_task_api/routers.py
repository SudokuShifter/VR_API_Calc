from fastapi import APIRouter, Query


adapt_router = APIRouter()


############################# Adapt-routers


@adapt_router.get('/api/v1/validate')
async def get_task_validate_value(
        object_id: str = Query(..., description='Object ID'),
        time_left: str = Query(..., description='Time left'),
        time_right: str = Query(..., description='Time right'),
):
    """
    Выполняет расчет данных для валидации на основе переданных параметров.
    """
    pass


@adapt_router.get('/api/v1/validate/get')
async def get_validate_data(
        object_id: str = Query(..., description='Object ID'),
):
    """
    Получает данные валидации из базы данных по идентификатору объекта.
    """
    pass


@adapt_router.put('/api/v1/validate/set')
async def put_validate_data(
        object_id: str = Query(..., description='Object ID'),
        is_user_value: bool = Query(..., description='Is user value'),
        wct: float = Query(..., description='Значение обводненности'),
        gas_condensate_factor: float = Query(..., description='Газовый конденсатный фактор')
):
    """
    Устанавливает данные валидации для объекта.
    """
    pass


@adapt_router.get('/api/v1/adaptation')
async def get_adaptation_value(
        object_id: str = Query(..., description='Object ID'),
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
        object_id: str = Query(..., description='Object ID'),
):
    """
    Получает все данные адаптации для объекта по его идентификатору.
    """
    pass


@adapt_router.get('/api/v1/adaptation/active')
async def get_active_adaptation_data(
        object_id: str = Query(..., description='Object ID'),
):
    """
    Получает активные данные адаптации для объекта по его идентификатору.
    """
    pass


@adapt_router.put('/api/v1/adaptation/set')
async def set_active_adaptation_value(
        object_id: str = Query(..., description='Object ID'),
        name: str = Query(..., description='Имя адаптации')
):
    """
    Устанавливает активные данные адаптации для объекта по имени адаптации.
    """
    pass


############################# FMM-routers


fmm_router = APIRouter()


@fmm_router.get('/api/v1/fmm')
async def execute_fmm_task(
        object_id: str = Query(..., description='Object ID'),
        time: str = Query(..., description='Момент времени, для которого выполняется задача')
):
    """
    Выполняет задачу FMM (вероятно, какую-то математическую или вычислительную задачу)
    для указанного объекта в определенный момент времени.
    """
    pass


@fmm_router.get('/api/v1/fmm/duration')
async def execute_fmm_duration(
        object_id: str = Query(..., description='Object ID'),
        time_left: str = Query(..., description='Time left'),
        time_right: str = Query(..., description='Time right')
):
    """
    Выполняет задачу FMM для указанного объекта в течение заданного временного интервала
    """
    pass


@fmm_router.get('/api/v1/fmm/duration/parallel')
async def execute_fmm_duration_parallel(
        object_id: str = Query(..., description='Object ID'),
        time_left: str = Query(..., description='Time left'),
        time_right: str = Query(..., description='Time right')
):
    """
    Выполняет задачу FMM для указанного объекта в течение заданного временного интервала параллельно
    (с использованием многопоточности или распределенных вычислений).
    """
    pass