import datetime
import sqlalchemy as sql
import sqlalchemy.orm as orm

from base import database

class BookRoom(database.Base):
    __tablename__ = "bookrooms"
    id = sql.Column(sql.Integer, primary_key=True, index=True)
    # openid
    openid = sql.Column(sql.String(50), index=True)
    # 姓名
    name = sql.Column(sql.String(20), index=True)
    # 学生学号
    xsxh = sql.Column(sql.String(20))
    # 电话
    phone = sql.Column(sql.String(20))
    # 房间名
    roomname = sql.Column(sql.String(20))
    # 预定原因
    reason = sql.Column(sql.String(100))
    # 教学周 指教学周
    week = sql.Column(sql.Integer)
    # 预定星期 指星期一 星期二
    week1 = sql.Column(sql.Integer)
    # 课节 1-2 9-10
    section = sql.Column(sql.String(10))
    # 是否通过
    finished = sql.Column(sql.Integer)
