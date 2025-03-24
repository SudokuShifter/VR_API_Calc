from typing import Annotated

from dependency_injector.wiring import Provide
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.db_session import get_db
from containers.config_container import ConfigContainer
from config import TSDBAPIConfig
from services.vr_storage_service import VRStorageService
from services.external_api_service import (
    PMMAPIService,
    MLAPIService,
    VRAPICore
)



async def get_vr_storage_service(session: AsyncSession=Depends(get_db)) -> VRStorageService:
    return VRStorageService(session)


async def get_pmm_service(config: ConfigContainer = Provide[ConfigContainer.pmm_config]) -> PMMAPIService:
    return PMMAPIService(config)


async def get_ml_service(config: ConfigContainer = Provide[ConfigContainer.ml_config]):
    return MLAPIService(config)


async def get_vr_service(config: TSDBAPIConfig = Provide[ConfigContainer.tsdb_config]):
    return VRAPICore(config)



VRStorage = Annotated[VRStorageService, Depends(get_vr_storage_service)]
PMMAPIService = Annotated[PMMAPIService, Depends(get_pmm_service)]
MLAPIService = Annotated[MLAPIService, Depends(get_ml_service)]
VRAPICore = Annotated[VRAPICore, Depends(get_vr_service)]