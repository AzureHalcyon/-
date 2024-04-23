import sqlalchemy.orm as orm
from users.models import User
import json
from typing import List
from base.database import engine
from base import database
from app.search_info import models,schemas
import json
from datetime import datetime

def search_info_all(db: orm.Session,openid,schema: schemas.SearchInfoSchema):
    users = db.query(User).filter_by(openid = openid).first()
    if users.level > 0:
        query = f"""
            SELECT *
            FROM test_information
            WHERE name LIKE '%%{schema.name}%%'
                OR student_id LIKE '%%{schema.student_id}%%'
                OR qq LIKE '%%{schema.qq}%%'
                OR campus_phone LIKE '%%{schema.campus_phone}%%';
        """
    else:
        query = f"""
            SELECT name, student_id, qq
            FROM test_information
            WHERE name LIKE '%%{schema.name}%%'
                OR student_id LIKE '%%{schema.student_id}%%'
                OR qq LIKE '%%{schema.qq}%%'
                OR campus_phone LIKE '%%{schema.campus_phone}%%';
        """
    with engine.connect() as connection:
        result = connection.execute(query)
        records = result.fetchall()
    return records

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()