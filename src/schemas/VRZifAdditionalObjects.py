from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class VRZifAdditionalObjectsBase(BaseModel):
    id: int
    name: Optional[str] = None
    creation_date: datetime

class VRZifAdditionalObjectsCreate(VRZifAdditionalObjectsBase):
    pass

class VRZifAdditionalObjectsPyd(VRZifAdditionalObjectsBase):
    class Config:
        from_attributes = True