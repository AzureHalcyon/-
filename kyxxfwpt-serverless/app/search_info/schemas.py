import pydantic
from typing import List
class SearchInfoSchema(pydantic.BaseModel):
    name: str
    student_id: str
    qq: str
    campus_phone :str

class OutSchema(pydantic.BaseModel):
    code: int
    tip: str
    class Config():
        orm_mode = True
