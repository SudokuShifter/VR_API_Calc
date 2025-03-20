from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class VRZifAdditionalObjectsBase(BaseModel):
    id: int
    name: Optional[str] = None
    zif_uid: str
    creation_date: datetime

class VRZifAdditionalObjectsCreate(VRZifAdditionalObjectsBase):
    pass

class VRZifAdditionalObjectsPyd(VRZifAdditionalObjectsBase):
    class Config:
        orm_mode = True