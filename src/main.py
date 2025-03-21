from contextlib import asynccontextmanager
from typing import AsyncGenerator
import uvicorn
from fastapi import FastAPI

from containers.config_container import ConfigContainer
from routers.additional_router import additional_router
from routers.ml_router import ml_router
from routers.pmm_routers import adapt_router, fmm_router
from dependencies.database import session_manager


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    config_container = ConfigContainer()
    config_container.wire(packages=[__name__, 'dependencies', 'services'])

    session_manager.init_db()
    yield
    await session_manager.close()


app = FastAPI(lifespan=lifespan)
app.include_router(additional_router, prefix='/additional', tags=['additional'])
app.include_router(ml_router, prefix='/ml', tags=['ml'])
app.include_router(adapt_router, prefix='/adapt_validate', tags=['adapt_validate'])
app.include_router(fmm_router, prefix='/fmm', tags=['fmms'])



@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


