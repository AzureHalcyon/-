import pydantic
from typing import List
class CreateSignSchema(pydantic.BaseModel):
    data: str
    classroom_id: int
    location: str
class GetSignsSchema(pydantic.BaseModel):
    aftertime: str
    classroom_id: int

class OutSchema(pydantic.BaseModel):
    code: int
    tip: str
    class Config():
        orm_mode = True
class OutClassroomSchema(OutSchema):
    classroom: str
    class Config():
        orm_mode = True

class OutSignsSchema(OutSchema):
    name: str
    xsxh: str
    time: str
    data: str
    location: str
    class Config():
        orm_mode = True