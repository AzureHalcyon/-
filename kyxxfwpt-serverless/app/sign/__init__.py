import fastapi
from fastapi import Request,Header,File, Response,Query
import sqlalchemy.orm as orm
from typing import Optional,List
from app.sign import services,schemas
from fastapi import APIRouter
from fastapi.responses import FileResponse
router = APIRouter()
@router.post("/student/create_sign",response_model = schemas.OutSchema)
async def create_sign(schema: schemas.CreateSignSchema,db: orm.Session = fastapi.Depends(services.get_db),x_wx_openid: Optional[str] = Header(None)):
    return services.create_sign(db, x_wx_openid, schema)
@router.get("/student/get_classroom")
async def get_classroom(db: orm.Session = fastapi.Depends(services.get_db)):
    return services.get_classroom(db)

@router.get("/teacher/get_signs")
async def get_signs(
    aftertime: str = Query(..., description="查询指定时间之后的签到记录"),
    classroom_id: int = Query(..., description="教室ID"),
    db: orm.Session = fastapi.Depends(services.get_db)
):
    url = services.get_signs(db,aftertime,classroom_id)
    
    return Response(content=url)

