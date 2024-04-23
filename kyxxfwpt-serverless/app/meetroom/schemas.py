import pydantic
from typing import List

class SearchRoomSchema(pydantic.BaseModel):
    date: str
    section: int # 1-2 9-10
class SubmitBookRoomSchema(pydantic.BaseModel):
    book_id: int
class BookRoomSchema(pydantic.BaseModel):
    phone: str
    reason: str
    roomname: str
    week: int
    week1: int
    section: str
class OutSchema(pydantic.BaseModel):
    code: int
    tip: str
    class Config():
        orm_mode = True
class OutBookRoomSchema(OutSchema):
    _id: int
    name: str
    phone: str
    reason: str
    roomname: str
    week: int
    week1: int
    section: str
class OutFreeRoomSchema(OutSchema):
    classroom: List[str]