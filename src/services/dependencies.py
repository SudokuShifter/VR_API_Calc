from typing import Annotated
from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.db_session import get_db
from containers.config_container import ConfigContainer
from config import TSDBAPIConfig, PMMAPIConfig, MLAPIConfig
from services.vr_storage_service import VRStorageService
from services.external_api_service import PMMAPIService, MLAPIService, VRAPICore


@inject
async def get_vr_storage_service(
    session: AsyncSession = Depends(get_db)
) -> VRStorageService:
    return VRStorageService(session)


@inject
async def get_vr_service(
    config: TSDBAPIConfig = Provide[ConfigContainer.tsdb_config]
) -> VRAPICore:
    return VRAPICore(config)


@inject
async def get_pmm_service(
    config: PMMAPIConfig = Provide[ConfigContainer.pmm_config]
) -> PMMAPIService:
    return PMMAPIService(config)

@inject
async def get_ml_service(
    config: MLAPIConfig = Provide[ConfigContainer.ml_config]
) -> MLAPIService:
    return MLAPIService(config)


VRStorageDep = Annotated[VRStorageService, Depends(get_vr_storage_service)]
VRCoreDep = Annotated[VRAPICore, Depends(get_vr_service)]
PMMServiceDep = Annotated[PMMAPIService, Depends(get_pmm_service)]
MLServiceDep = Annotated[MLAPIService, Depends(get_ml_service)]