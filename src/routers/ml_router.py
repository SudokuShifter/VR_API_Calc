from fastapi import (
    APIRouter,
    Query
)

from services.dependencies import MLAPIService

ml_router = APIRouter()


@ml_router.get("/api/v1/ml")
async def execute_ml_task(
        object_id: str = Query(..., description='Object ID'),
        time: str = Query(..., description='Момент времени, для которого выполняется задача')
):
    """
    Запускает ml-task за метку времени
    """
    return await MLAPIService.execute_ml_task(object_id, time)


@ml_router.get("/api/v1/ml/duration")
async def execute_ml_duration_task(
        object_id: int = Query(..., description='Object ID'),
        time_left: str = Query(..., description='Time left'),
        time_right: str = Query(..., description='Time right')
):
    """
    Запускает ml-task за диапазон времени
    """
    return await MLAPIService.execute_ml_task(object_id, time_left, time_right)
