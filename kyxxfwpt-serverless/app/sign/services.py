import sqlalchemy.orm as orm
import users.models
import json
from typing import List
from base import database
from app.sign import models,schemas
import json
from datetime import datetime
from sqlalchemy import and_
import pandas as pd
from io import BytesIO
import requests
def create_sign(db: orm.Session,openid: str,schema: schemas.CreateSignSchema) -> schemas.OutSchema:
    try:
        user = db.query(users.models.User).filter_by(openid = openid).first()
        new_sign = models.Sign(
            openid = openid,
            name = user.name,
            xsxh = user.xsxh,
            data = schema.data,
            location = schema.location,
            classroom = schema.classroom_id
        )
        db.add(new_sign)
        db.commit()
        return schemas.OutSchema(
            code = 0,
            tip = "签到成功"
        )
    except Exception as e:
        return schemas.OutSchema(
            code = 1,
            tip = f"签到失败 {e}"
        )
def get_classroom(db: orm.Session):
    # 获取数据库内所有数据
    classrooms = db.query(models.Classroom).all()
    result_dict = {}
    # 将查询结果转换为字典
    for classroom in classrooms:
        result_dict[classroom.classroomname] = classroom.id
    return result_dict
    # 将字典转换为 JSON
    # json_text = json.dumps(result_dict, ensure_ascii=False)
    # return schemas.OutClassroomSchema(
    #     code = 0,
    #     tip = "获取成功",
    #     classroom = json_text
    # )
def upload_to_bashupload(excel_file):
    files = {'file': ('output.xlsx', excel_file.getvalue())}
    response = requests.post('https://bashupload.com', files=files)
    if response.status_code == 200:
        parts = response.text.split()
        url = None
        for part in parts:
            if part.startswith("https://"):
                url = part
                break

        return url
    else:
        return False
def get_signs(db: orm.Session,aftertime,id):
    datetime_after = datetime.strptime(aftertime, "%Y-%m-%d %H:%M:%S")
    signs_after_datetime = db.query(models.Sign).filter(and_(models.Sign.classroom == id)).filter(models.Sign.time >= datetime_after).all()
    signs_dict_list = [{"姓名": sign.name, "学号": sign.xsxh, "签到时间": sign.time, "数据": sign.data, "经纬度": sign.location} for sign in signs_after_datetime]
    df = pd.DataFrame(signs_dict_list)
    excel_file = BytesIO()
    df.to_excel(excel_file, index=False)
    excel_file.seek(0)
    url = upload_to_bashupload(excel_file)
    return url
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 

# # 假设 datetime_after 是你指定的日期时间
# datetime_after = datetime(2024, 3, 25)

# # 查询指定签到时间后的数据库数据
# signs_after_datetime = session.query(Sign).filter(Sign.time >= datetime_after).all()

# # signs_after_datetime 现在是一个包含所有在指定日期时间之后的签到记录的列表