import pydantic
from typing import List
class AddClassroom(pydantic.BaseModel):
    classroom: str
class OutSchema(pydantic.BaseModel):
    code: int
    tip: str
    class Config():
        orm_mode = True
class OutClassroomSchema(OutSchema):
    classroom: str
    class Config():
        orm_mode = True
