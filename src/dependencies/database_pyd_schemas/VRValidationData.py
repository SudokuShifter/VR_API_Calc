from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class VRValidationDataBase(BaseModel):
    id: int
    vr_zif_objects_id: int
    wct: float
    gas_condensate_factor: float
    is_user_value: bool
    date: datetime

class VRValidationDataCreate(VRValidationDataBase):
    pass

class VRValidationDataPyd(VRValidationDataBase):
    class Config:
        orm_mode = True