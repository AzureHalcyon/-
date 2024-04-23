import fastapi
from fastapi import Header
import sqlalchemy.orm as orm
from typing import Optional
from app.bookroom import services,schemas
from fastapi import APIRouter
from typing import List
router = APIRouter()

@router.post("/get_all_rooms")
async def get_all_rooms(db: orm.Session = fastapi.Depends(services.get_db)):
    return services.get_room(db)
# book_room
@router.post("/book_room",response_model = schemas.OutSchema)
async def book_room(schema: schemas.BookRoomSchema,db: orm.Session = fastapi.Depends(services.get_db),x_wx_openid: Optional[str] = Header(None)):
    return services.book_room(db, x_wx_openid, schema)
# get_room_by_id 获取被占用的房间
@router.post("/get_room_by_id",response_model = List[schemas.OutBookRoomSchema])
async def get_room_by_id(schema: schemas.SearchRoomSchema,db: orm.Session = fastapi.Depends(services.get_db)):
    return services.get_room_by_id(db, schema)
# add_room
@router.post("/add_room",response_model = schemas.OutSchema)
async def add_room(schema: schemas.RoomSchema,db: orm.Session = fastapi.Depends(services.get_db)):
    return services.add_room(db, schema)
# get_room_by_user
@router.post("/get_room_by_user",response_model = List[schemas.OutmyBookRoomSchema])
async def get_room_by_user(db: orm.Session = fastapi.Depends(services.get_db),x_wx_openid: Optional[str] = Header(None)):
    return services.get_room_by_user(db, x_wx_openid)
# get_all_book_room
@router.post("/get_all_book_room",response_model = List[schemas.outdetailschema])
async def get_all_book_room(db: orm.Session = fastapi.Depends(services.get_db)):
    return services.get_all_book_room(db)
# approve_room
@router.post("/approve_room",response_model = schemas.OutSchema)
async def approve_room(schema: schemas.approveRoomSchema,db: orm.Session = fastapi.Depends(services.get_db)):
    return services.approve_room(db, schema)
