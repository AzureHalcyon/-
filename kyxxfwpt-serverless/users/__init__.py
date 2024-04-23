import fastapi
from fastapi import Request,Header
import sqlalchemy.orm as orm
from users import services
from users import schemas
from typing import Optional,List

from fastapi import APIRouter

router = APIRouter()
@router.post("/create_user",response_model = schemas.OutSchema)
async def create_user(schema: schemas.CreateUserSchema,db: orm.Session = fastapi.Depends(services.get_db),x_wx_openid: Optional[str] = Header(None)):
    return await services.create_user(db, x_wx_openid, schema)
@router.post("/search_user",response_model = schemas.OutSchema)
async def search_user(db: orm.Session = fastapi.Depends(services.get_db),x_wx_openid: Optional[str] = Header(None)):
    return services.search_user(db, x_wx_openid)

