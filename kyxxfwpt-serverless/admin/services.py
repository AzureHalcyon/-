import sqlalchemy.orm as orm
import users.models
import json
from typing import List
from base import database
from admin import models,schemas
from app.sign.models import Classroom
import json
from datetime import datetime
from sqlalchemy import and_

def add_signclassroom(db: orm.Session,openid: str,schema: schemas.AddClassroom) -> schemas.OutSchema:
    try:
        user = db.query(users.models.User).filter_by(openid = openid).first()
        if user.level == 2:
            new_classroom = Classroom(
                classroomname = schema.classroom
            )
            db.add(new_classroom)
            db.commit()
            return schemas.OutSchema(
                code = 0,
                tip = "添加成功"
            )
        else:
            return schemas.OutSchema(
                code = 1,
                tip = "权限不足"
            )
    except Exception as e:
        return schemas.OutSchema(
            code = 1,
            tip = f"添加失败 {e}"
        )

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()