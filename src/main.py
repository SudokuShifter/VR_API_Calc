from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI, Query

from containers.config_container import ConfigContainer
from ml_task_api.routers import ml_router
from pmm_task_api.routers import adapt_router, fmm_router
from dependencies import VRStorage


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    config_container = ConfigContainer()
    config_container.wire(packages=[__name__, 'pmm_task_api', 'ml_task_api', 'dependencies'])
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(ml_router, prefix='/ml', tags=['ml'])
app.include_router(adapt_router, prefix='/adapt_validate', tags=['adapt_validate'])
app.include_router(fmm_router, prefix='/fmm', tags=['fmms'])


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}


@app.get("/api/v1/type-calculation/all")
async def all_type_calculation(VRStorage: VRStorage):
    """
    Получает все типы расчетов, доступные в системе.
    """
    return VRStorage.get_all_main_objects()



@app.get("/api/v1/type-calculation/")
async def type_calculation(
        object_uid: str = Query(..., description='Идентификатор объекта')
):
    """
    Получает тип расчета по идентификатору объекта (object_uid).
    """
    return VRStorage.get_object_by_uid(object_uid)


@app.put('/api/v1/type-calculation/set/')
async def type_calculation_set(
        object_uid: str = Query(..., description='Идентификатор объекта'),
        type_value: str = Query(..., description='Значение типа расчета')
):
    """
    Устанавливает активный тип расчета для объекта по его идентификатору
    """
    obj = VRStorage.get_object_by_uid(object_uid)
    return VRStorage.set_type_calculation(obj, type_value)



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


