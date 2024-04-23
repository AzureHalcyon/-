import datetime
import sqlalchemy as sql
import sqlalchemy.orm as orm

from base import database
class Classroom(database.Base):
    __tablename__ = "signs_classroom" 
    id = sql.Column(sql.Integer, primary_key=True, index=True)
    classroomname = sql.Column(sql.String(20), index=True)

class Sign(database.Base):
    __tablename__ = "signs"
    id = sql.Column(sql.Integer, primary_key=True, index=True)
    # openid
    openid = sql.Column(sql.String(50), index=True)
    # 姓名
    name = sql.Column(sql.String(20), index=True)
    # 学生学号
    xsxh = sql.Column(sql.String(20))
    # 签到时间
    time = sql.Column(sql.DateTime, default=datetime.datetime.now)
    # 签到数据
    data = sql.Column(sql.String(50))
    # 签到位置
    location = sql.Column(sql.String(20))
    # 签到教室(ID)
    classroom = sql.Column(sql.Integer)