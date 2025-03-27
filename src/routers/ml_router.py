from datetime import datetime

from fastapi import (
    APIRouter,
    Query, Depends
)

from services.dependencies import (
    MLServiceDep,
    VRCoreDep
)

ml_router = APIRouter()


@ml_router.get("/api/v1/ml")
async def execute_ml_task(
        vr_core: VRCoreDep,
        ml_service: MLServiceDep,
        object_id: str = Query(..., description='Well ID'),
        time: datetime = Query(..., description="2021-01-01T00:00:00Z")
):
    """
    Запускает ml-task за метку времени
    """
    time = time.strftime('%Y-%m-%dT%H:%M:%SZ')
    return await vr_core.get_data_for_ml_by_time_point(
        time=time, well_id=object_id
    )


@ml_router.get("/api/v1/ml/duration")
async def execute_ml_duration_task(
        vr_core: VRCoreDep,
        ml_service: MLServiceDep,
        object_id: str = Query(..., description='Object ID'),
        date_start: datetime = Query(..., description="2021-01-01T00:00:00Z"),
        date_end: datetime = Query(..., description="2021-01-01T00:00:00Z")
):
    """
    Запускает ml-task за диапазон времени
    """
    time_left = date_start.strftime('%Y-%m-%dT%H:%M:%SZ')
    time_right = date_end.strftime('%Y-%m-%dT%H:%M:%SZ')
    return await vr_core.get_data_for_ml_by_range(
        time_left=time_left, time_right=time_right, well_id=object_id
    )