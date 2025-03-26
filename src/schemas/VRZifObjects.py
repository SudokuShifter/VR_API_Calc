from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class VRZifObjectsBase(BaseModel):
    id: int
    name: Optional[str] = None
    hole_project_id: int
    active_adaptation_value_id: int = 0
    creation_date: datetime
    active_vr_type: Optional[str] = None
    current_date_scheduler: Optional[datetime] = None
    scheduler_status: Optional[str] = None

class VRZifObjectsCreate(VRZifObjectsBase):
    pass

class VRZifObjectsPyd(VRZifObjectsBase):
    class Config:
        from_attributes = True