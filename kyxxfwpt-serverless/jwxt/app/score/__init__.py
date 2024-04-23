import fastapi
from fastapi import Request,Header
import sqlalchemy.orm as orm
from typing import Optional,List
from fastapi import APIRouter

from jwxt.app.score import services,schemas

router = APIRouter()
@router.post("/student/search_score",response_model = schemas.OutScoreSchema)
async def search_score(schema: schemas.SearchScoreSchema,db: orm.Session = fastapi.Depends(services.get_db),x_wx_openid: Optional[str] = Header(None)):
    return await services.search_score(db, x_wx_openid, schema)

@router.post("/student/get_semester")
def get_semester():
    return services.get_semester()