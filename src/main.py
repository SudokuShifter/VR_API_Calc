from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI, Query

from containers.config_container import ConfigContainer
from ml_task_api.routers import ml_router
from pmm_task_api.routers import pmm_router


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    config_container = ConfigContainer()
    config_container.wire(packages=[__name__, 'pmm_task_api', 'ml_task_api', 'additional_services'])
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(ml_router, prefix='/ml')
app.include_router(pmm_router, prefix='/pmm')


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}


@app.get("/api/v1/type-calculation/all")
async def all_type_calculation():
    """
    Получает все типы расчетов, доступные в системе.
    """
    pass


@app.get("/api/v1/type-calculation/{object_uid}")
async def type_calculation(
        object_uid: str = Query(..., description='Идентификатор объекта')
):
    """
    Получает тип расчета по идентификатору объекта (object_uid).
    """
    pass


@app.put('/api/v1/type-calculation/set/{object_uid}')
async def type_calculation_set(
        object_uid: str = Query(..., description='Идентификатор объекта'),
        type_value: str = Query(..., description='Значение типа расчета')
):
    """
    Устанавливает активный тип расчета для объекта по его идентификатору
    """
    pass



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


