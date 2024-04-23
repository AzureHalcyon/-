import fastapi
from fastapi import Request,Header,File, Response,Query
import sqlalchemy.orm as orm
from typing import Optional,List
from app.search_info import services,schemas
from fastapi import APIRouter
from fastapi.responses import FileResponse
router = APIRouter()
@router.post("/search_info")
async def search_info_all(schema: schemas.SearchInfoSchema,db: orm.Session = fastapi.Depends(services.get_db),x_wx_openid: Optional[str] = Header(None)):
    return services.search_info_all(db,x_wx_openid,schema)

