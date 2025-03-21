from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI, Query

from containers.config_container import ConfigContainer
from ml_task_api.routers import ml_router
from pmm_task_api.routers import adapt_router, fmm_router
from dependencies.VRStorageService import VRStorage


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
async def all_type_calculation(vr_storage: VRStorage):
    """
    Получает все типы расчетов, доступные в системе.
    """
    return await vr_storage.get_all_main_objects()


@app.get("/api/v1/type-calculation/")
async def type_calculation(
        vr_storage: VRStorage,
        object_uid: str = Query(..., description='Идентификатор объекта')
):
    """
    Получает тип расчета по идентификатору объекта (object_uid).
    """
    return await vr_storage.get_object_by_uid(object_uid)


@app.put('/api/v1/type-calculation/set/')
async def type_calculation_set(
        vr_storage: VRStorage,
        object_uid: str = Query(..., description='Идентификатор объекта'),
        type_value: str = Query(..., description='Значение типа расчета')
):
    """
    Устанавливает активный тип расчета для объекта по его идентификатору
    """
    obj = await vr_storage.get_object_by_uid(object_uid)
    await vr_storage.set_type_calculation(obj, type_value)
    return {'message': f'Тип расчета обновлён {type_value} для {obj}'}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


