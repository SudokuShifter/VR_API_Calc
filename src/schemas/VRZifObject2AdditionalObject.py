from pydantic import BaseModel
from typing import Optional


class VRZifObject2AdditionalObjectBase(BaseModel):
    id: int
    vr_zif_objects_id: int
    vr_zif_additional_objects_id: int
    name_train: Optional[str] = None

class VRZifObject2AdditionalObjectCreate(VRZifObject2AdditionalObjectBase):
    pass

class VRZifObject2AdditionalObjectPyd(VRZifObject2AdditionalObjectBase):
    class Config:
        orm_mode = True