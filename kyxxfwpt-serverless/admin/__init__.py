import fastapi
from fastapi import Request,Header,File, Response,Query
import sqlalchemy.orm as orm
from typing import Optional,List
from admin import services,schemas
from fastapi import APIRouter
from fastapi.responses import FileResponse
router = APIRouter()
@router.post("/admin/add_signclassroom",response_model = schemas.OutSchema)
async def add_signclassroom(schema: schemas.AddClassroom,db: orm.Session = fastapi.Depends(services.get_db),x_wx_openid: Optional[str] = Header(None)):
    return services.add_signclassroom(db,x_wx_openid,schema)
