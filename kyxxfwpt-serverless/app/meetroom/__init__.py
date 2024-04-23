import fastapi
from fastapi import Request,Header,File
from fastapi import APIRouter
import sqlalchemy.orm as orm
from typing import Optional,List
from app.meetroom import services,schemas

router = APIRouter()

# @router.post("/teacher/submit_book_room",response_model = schemas.OutSchema)
# async def submit_book_room(schema: schemas.SubmitBookRoomSchema,db: orm.Session = fastapi.Depends(services.get_db),x_wx_openid: Optional[str] = Header(None)):
#     return await services.submit_book_room(db, x_wx_openid,schema)

# @router.post("/teacher/get_book_room",response_model = List[schemas.OutBookRoomSchema])
# async def get_book_room(db: orm.Session = fastapi.Depends(services.get_db),x_wx_openid: Optional[str] = Header(None)):
#     return services.get_book_room(db, x_wx_openid)
# @router.post("/student/book_room",response_model = schemas.OutSchema)
# async def book_room(schema: schemas.BookRoomSchema,db: orm.Session = fastapi.Depends(services.get_db),x_wx_openid: Optional[str] = Header(None)):
#     return services.book_room(db, x_wx_openid, schema)

@router.post("/student/search_room",response_model = schemas.OutFreeRoomSchema)
async def search_room(schema: schemas.SearchRoomSchema,db: orm.Session = fastapi.Depends(services.get_db),x_wx_openid: Optional[str] = Header(None)):
    return await services.search_room(db, x_wx_openid, schema)