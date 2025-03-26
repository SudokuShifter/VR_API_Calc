from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from dependency_injector.wiring import inject, Provide

from dependencies.db_session import get_db
from services.vr_storage_service import VRStorageService
from services.external_api_service import PMMAPIService, MLAPIService, VRAPICore
from config import TSDBAPIConfig, PMMAPIConfig, MLAPIConfig


@inject
def get_vr_service(
) -> VRAPICore:
    return VRAPICore()


@inject
def get_pmm_service(
) -> PMMAPIService:
    return PMMAPIService()


@inject
def get_ml_service(
) -> MLAPIService:
    return MLAPIService()


async def get_vr_storage_service(
    session: AsyncSession = Depends(get_db)
) -> VRStorageService:
    return VRStorageService(session)


VRStorageDep = Annotated[VRStorageService, Depends(get_vr_storage_service)]
VRCoreDep = Annotated[VRAPICore, Depends(get_vr_service)]
PMMServiceDep = Annotated[PMMAPIService, Depends(get_pmm_service)]
MLServiceDep = Annotated[MLAPIService, Depends(get_ml_service)]