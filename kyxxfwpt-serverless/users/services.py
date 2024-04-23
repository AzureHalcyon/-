import sqlalchemy.orm as orm
from users import models
from users import schemas
import json
from typing import List
from base import database
from autoserver import getJwxtTicketFromAutoServer
from users.utils import cipher_suite
class SimpleRedis:
    def __init__(self):
        self.data = {}

    def set(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)

    def delete(self, key):
        if key in self.data:
            del self.data[key]

    def exists(self, key):
        return key in self.data
redis = SimpleRedis()


async def create_user(db: orm.Session,openid: str,schema: schemas.CreateUserSchema) -> schemas.OutSchema:
    try:
        success, _ = getJwxtTicketFromAutoServer(schema.xsxh, schema.password)
        if schema.authcode == 25535:
            level = 1
        elif schema.authcode == 25536:
            level = 2
        else:
            level = 0
        if success:
            new_user = models.User(
                openid = openid,
                name = schema.name,
                xsxh = schema.xsxh,
                password = cipher_suite.encrypt(schema.password.encode()),
                level = level
            )
            db.add(new_user)
            db.commit()
            return schemas.OutSchema(
                code = 0,
                tip = "创建用户成功",
                level = new_user.level,
                name = "",
                xsxh = "",
            )
        else:
            return schemas.OutSchema(
                    code = 1,
                    tip = "创建用户失败",
                    level = 0,
                    name = "",
                    xsxh = ""
                )
    except Exception as e:
        return schemas.OutSchema(
            code = 1,
            tip = f"创建用户失败 {e}",
            level = 0,
            name = "",
            xsxh = ""
        )
def search_user(db: orm.Session,openid: str) -> schemas.OutSchema:
    try:
        user = db.query(models.User).filter(models.User.openid == openid).first()
        if user is None:
            return schemas.OutSchema(
                code = 1,
                tip = "用户不存在",
                name = "",
                xsxh = "",
                level = 0
            )
        return schemas.OutSchema(
            code = 0,
            tip = "",
            name = user.name,
            xsxh = user.xsxh,
            level = user.level
        )
    except:
        return schemas.OutSchema(
            code = 1,
            tip = "查询用户失败",
            name = "",
            xsxh = "",
            level = 0
        )
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()