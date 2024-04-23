import datetime
import sqlalchemy as sql
import sqlalchemy.orm as orm

from base import database


class User(database.Base):
    __tablename__ = "users"
    id = sql.Column(sql.Integer, primary_key=True, index=True)
    # openid
    openid = sql.Column(sql.String(50), index=True)
    # 姓名
    name = sql.Column(sql.String(20), index=True)
    # 学生学号
    xsxh = sql.Column(sql.String(20))
    # 教务处系统密码
    password = sql.Column(sql.LargeBinary)
    # 用户等级
    level = sql.Column(sql.Integer, default=0)