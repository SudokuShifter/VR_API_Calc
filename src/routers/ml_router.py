from fastapi import (
    APIRouter,
    Query
)

ml_router = APIRouter()


@ml_router.get("/api/v1/ml")
async def execute_ml_task(
        object_id: str = Query(..., description='Object ID'),
        time: str = Query(..., description='Момент времени, для которого выполняется задача')
):
    pass


@ml_router.get("/api/v1/ml/duration")
async def execute_ml_duration_task(
        object_id: str = Query(..., description='Object ID'),
        time_left: str = Query(..., description='Time left'),
        time_right: str = Query(..., description='Time right')
):
    pass
