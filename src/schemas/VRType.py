from pydantic import BaseModel
from typing import Optional


class VRTypeBase(BaseModel):
    id: str
    description: Optional[str] = None

class VRTypeCreate(VRTypeBase):
    pass

class VRTypePyd(VRTypeBase):
    class Config:
        from_attributes = True