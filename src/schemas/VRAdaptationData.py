from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class VRAdaptationDataBase(BaseModel):
    id: int
    vr_zif_objects_id: int
    name: Optional[str] = None
    choke_percent_adapt: List[float]
    choke_value_adapt: List[float]
    date_start: datetime
    date_end: datetime
    creation_date: datetime

class VRAdaptationDataCreate(VRAdaptationDataBase):
    pass

class VRAdaptationDataPyd(VRAdaptationDataBase):
    class Config:
        from_attributes = True