import sqlalchemy.orm as orm
from users.models import User
from typing import List
from base.database import engine
from base import database
from app.bookroom import models,schemas
from datetime import datetime
from sqlalchemy import and_
# 查询所有未通过的会议室预约记录
def get_all_book_room(db: orm.Session):
    temp = db.query(models.BookRoomInfo).filter(models.BookRoomInfo.authorize == 0).all()
    out_list = [
            schemas.outdetailschema(
                id = item.id,
                user_id = item.user_id,
                room_id = item.room_id,
                user_name = item.user_name,
                room_name = item.room_name,
                yearmonthday = item.yearmonthday.strftime("%Y-%m-%d %H:%M:%S"),
                time = item.time,
                authorize = item.authorize
            )
            for item in temp
    ]
    return out_list
# 增加会议室
def add_room(db: orm.Session,schema: schemas.RoomSchema):
    new_room = models.Room(
        roomname = schema.roomname
    )
    db.add(new_room)
    db.commit()
    return schemas.OutSchema(
        code = 0,
        tip = "添加成功"
    )

# 查询会议室Room
def get_room(db: orm.Session) -> List[models.Room]:
    return db.query(models.Room).all()
# 预定会议室
def book_room(db: orm.Session,openid: str,schema: schemas.BookRoomSchema):
    user = db.query(User).filter_by(openid = openid).first()
    yearmonthday = datetime.strptime(schema.yearmonthday, "%Y-%m-%d")
    new_book = models.BookRoomInfo(
        user_id = user.id,
        user_name = user.name,
        room_id = schema.room_id,
        room_name = schema.room_name,
        yearmonthday = yearmonthday,
        time = schema.time,
        authorize = 0
    )
    db.add(new_book)
    db.commit()
    return schemas.OutSchema(
        code = 0,
        tip = "预定成功 等待审批"
    )
# 根据room_id查询当前被预定的会议室
def get_room_by_id(db: orm.Session,schema: schemas.SearchRoomSchema) -> List[schemas.OutBookRoomSchema]:
    yearmonthday = datetime.strptime(schema.yearmonthday, "%Y-%m-%d")
    print(yearmonthday)
    return db.query(models.BookRoomInfo).filter(and_(
        models.BookRoomInfo.room_id == schema.room_id,
        models.BookRoomInfo.authorize == 0,
        models.BookRoomInfo.yearmonthday == yearmonthday
    )).all()
# 通过房间审批
def approve_room(db: orm.Session,schema: schemas.approveRoomSchema):
    book = db.query(models.BookRoomInfo).filter(models.BookRoomInfo.id == schema.book_id).first()
    book.authorize = schema.book_code

    db.commit()
    return schemas.OutSchema(
        code = 0,
        tip = "成功"
    )

# 获取用户提交的会议室申请
def get_room_by_user(db: orm.Session,openid: str) -> List[schemas.OutmyBookRoomSchema]:
    user = db.query(User).filter_by(openid = openid).first()
    books = db.query(models.BookRoomInfo).filter(models.BookRoomInfo.user_id == user.id).all()
    out_list = [
            schemas.OutmyBookRoomSchema(
                room_id = item.id,
                room_name = item.room_name,
                yearmonthday = item.yearmonthday.strftime("%Y-%m-%d %H:%M:%S"),
                time = item.time,
                authorize = item.authorize
            )
            for item in books
        ]
    return out_list
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()