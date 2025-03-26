from contextlib import asynccontextmanager
from typing import AsyncGenerator
import uvicorn
from dependency_injector.wiring import Provide
from fastapi import FastAPI


from routers.additional_router import additional_router
from routers.ml_router import ml_router
from routers.pmm_routers import adapt_router, fmm_router
from dependencies.database import session_manager
from services.dependencies import VRStorageDep
from src.services.vr_storage_service import VRStorageService


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    session_manager.init_db()
    storage_service = VRStorageService(session=session_manager.session)
    await storage_service.init_db_script()
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


@app.get('/check_rout')
async def check_rout(vr_storage: VRStorageDep):
    return await vr_storage.get_all_addi()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)


