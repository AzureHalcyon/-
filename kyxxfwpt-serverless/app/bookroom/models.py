import datetime
import sqlalchemy as sql
import sqlalchemy.orm as orm
from base import database

class Room(database.Base):
    __tablename__ = "rooms" 
    id = sql.Column(sql.Integer, primary_key=True, index=True)
    roomname = sql.Column(sql.String(20), index=True)

class BookRoomInfo(database.Base):
    __tablename__ = "bookroomsinfo" 
    id = sql.Column(sql.Integer, primary_key=True, index=True)
    user_id = sql.Column(sql.Integer)
    room_id = sql.Column(sql.Integer)
    user_name = sql.Column(sql.String(30))
    room_name = sql.Column(sql.String(30))
    yearmonthday = sql.Column(sql.DateTime)  
    time = sql.Column(sql.Integer)
    authorize = sql.Column(sql.Integer)
