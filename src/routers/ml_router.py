from fastapi import (
    APIRouter,
    Query, Depends
)

from services.dependencies import MLServiceDep

ml_router = APIRouter()


@ml_router.get("/api/v1/ml")
async def execute_ml_task(
        ml_service: MLServiceDep,
        object_id: int = Query(..., description='Object ID'),
        time: str = Query(..., description='Момент времени, для которого выполняется задача')
):
    """
    Запускает ml-task за метку времени
    """
    pass


@ml_router.get("/api/v1/ml/duration")
async def execute_ml_duration_task(
        ml_service: MLServiceDep,
        object_id: int = Query(..., description='Object ID'),
        time_left: str = Query(..., description='Time left'),
        time_right: str = Query(..., description='Time right')
):
    """
    Запускает ml-task за диапазон времени
    """
    pass