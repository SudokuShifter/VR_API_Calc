from typing import Annotated

from fastapi import Depends

from services.pmm_service import AdaptationAndValidationService
from services.vr_storage_service import VRStorageService


async def get_adapt_validate_service():
    return AdaptationAndValidationService()


async def get_vr_storage_service() -> VRStorageService:
    return VRStorageService()


VRStorage = Annotated[VRStorageService, Depends(get_vr_storage_service)]
AdaptValidateService = Annotated[AdaptationAndValidationService, Depends(get_adapt_validate_service)]