import sqlalchemy.orm as orm
from base import models
from base import database
from base import schemas
import users.models
import json
from typing import List

def main(db: orm.Session,openid: str) -> schemas.OutSchema:
    return schemas.OutSchema(
        code = 0,
        tip = "Hello World!"
    )
def get_menu(db: orm.Session,openid: str):
    user = db.query(users.models.User).filter_by(openid = openid).first()
    base = [
        {"title":"签到","nav":"/pages/sign/sign"},
        {"title":"成绩查询","nav":"/pages/score/score"},
        {"title":"空闲教室查询","nav":"/pages/freeroom/freeroom"},
        {"title":"信息查询","nav":"/pages/searchinfo/searchinfo"},
        {"title":"会议室预约","nav":"/pages/bookroom/bookroom"}
    ]
    if user.level >= 1:
        base.append({"title":"签到导出","nav":"/pages/signexport/signexport"})
    if user.level == 2:
        base.append({"title":"实验教室添加","nav":"/pages/addclassroom/addclassroom"})
        base.append({"title":"会议室预约审批","nav":"/pages/auth_room/auth_room"})
    return base
    
def create_database():
    return database.Base.metadata.create_all(bind=database.engine)
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
