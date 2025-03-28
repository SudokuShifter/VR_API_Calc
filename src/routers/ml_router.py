from datetime import datetime

from fastapi import (
    APIRouter,
    Query, Depends
)
from pyexpat import features

from services.dependencies import (
    MLServiceDep,
    VRCoreDep
)

ml_router = APIRouter()


@ml_router.get("/api/v1/ml")
async def execute_ml_task(
        vr_core: VRCoreDep,
        ml_service: MLServiceDep,
        well_id: str = Query(..., description='Well ID'),
        time: datetime = Query(..., description="2021-01-01T00:00:00Z"),
        target_name: str = Query(..., description='Тип расчета')
):
    """
    Запускает ml-task за метку времени
    """
    time = time.strftime('%Y-%m-%dT%H:%M:%SZ')
    data = await vr_core.get_data_for_ml_by_time_point(
        time=time, well_id=well_id
    )
    data = {'well_id': well_id, 'target_name': target_name, 'features': data}
    return await ml_service.execute_ml_task(
        data=data
    )


@ml_router.get("/api/v1/ml/duration")
async def execute_ml_duration_task(
        vr_core: VRCoreDep,
        ml_service: MLServiceDep,
        well_id: str = Query(..., description='Object ID'),
        date_start: datetime = Query(..., description="2021-01-01T00:00:00Z"),
        date_end: datetime = Query(..., description="2021-01-01T00:00:00Z"),
        target_name: str = Query(..., description='Тип расчета')
):
    """
    Запускает ml-task за диапазон времени
    """
    time_left = date_start.strftime('%Y-%m-%dT%H:%M:%SZ')
    time_right = date_end.strftime('%Y-%m-%dT%H:%M:%SZ')
    data = await vr_core.get_data_for_ml_by_range(
        time_left=time_left, time_right=time_right, well_id=well_id
    )
    data = {'well_id': well_id, 'target_name': target_name, 'features': data}
    return await ml_service.execute_ml_task(
        data=data
    )