from typing import Annotated

from dependencies.VRStorageService import VRStorageService


async def get_vr_storage_service() -> VRStorageService:
    return VRStorageService()


VRStorage = Annotated[VRStorageService, get_vr_storage_service()]
