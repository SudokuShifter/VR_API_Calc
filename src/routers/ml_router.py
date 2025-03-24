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
    vr_zif_obj = MLAPIService.get_object_by_id(object_id)
    pass


@ml_router.get("/api/v1/ml/duration")
async def execute_ml_duration_task(
        object_id: int = Query(..., description='Object ID'),
        time_left: str = Query(..., description='Time left'),
        time_right: str = Query(..., description='Time right')
):
    vr_zif_obj = MLAPIService.get_object_by_id(object_id)
    pass
