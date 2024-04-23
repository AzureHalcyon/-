import pydantic
from typing import List
class approveRoomSchema(pydantic.BaseModel):
    book_id: int
    book_code: int
class BookRoomSchema(pydantic.BaseModel):
    room_id: int
    room_name: str
    yearmonthday: str
    time: int
class SearchRoomSchema(pydantic.BaseModel):
    room_id: int
    yearmonthday: str
class RoomSchema(pydantic.BaseModel):
    roomname: str
class OutBookRoomSchema(pydantic.BaseModel):
    room_id: int
    time: int
    class Config():
        orm_mode = True


# 建立一个schema 和bookroominfo相等
class outdetailschema(pydantic.BaseModel):
    id: int
    user_id: int
    room_id: int
    user_name: str
    room_name: str
    yearmonthday: str
    time: int
    authorize: int

class OutmyBookRoomSchema(BookRoomSchema):
    authorize: int
    class Config():
        orm_mode = True
class OutSchema(pydantic.BaseModel):
    code: int
    tip: str
    class Config():
        orm_mode = True
