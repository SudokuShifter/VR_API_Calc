from pydantic import BaseModel
from typing import Optional


class VRSchedulerStatusBase(BaseModel):
    id: str
    description: Optional[str] = None

class VRSchedulerStatusCreate(VRSchedulerStatusBase):
    pass

class VRSchedulerStatusPyd(VRSchedulerStatusBase):
    class Config:
        orm_mode = True