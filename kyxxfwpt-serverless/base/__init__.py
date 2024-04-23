import fastapi
from fastapi import Request,Header
import sqlalchemy.orm as orm
from base import services
from base import schemas
from typing import Optional,List
import pymysql
from app import bookroom
import users
from app import meetroom
from jwxt.app import score
from app import sign
from app import search_info

import admin
pymysql.install_as_MySQLdb()

app = fastapi.FastAPI()
services.create_database()

# 添加各页面路由
app.include_router(bookroom.router)
app.include_router(meetroom.router)
app.include_router(users.router)
app.include_router(score.router)
app.include_router(sign.router)
app.include_router(search_info.router)
app.include_router(admin.router)
# 写一个不同用户等级返回不同接口地址的接口
@app.get("/",response_model = schemas.OutSchema)
async def main(db: orm.Session = fastapi.Depends(services.get_db),x_wx_openid: Optional[str] = Header(None)):
    return services.main(db, x_wx_openid)
@app.get("/get_menu")
async def get_menu(db: orm.Session = fastapi.Depends(services.get_db),x_wx_openid: Optional[str] = Header(None)):
    return services.get_menu(db, x_wx_openid)