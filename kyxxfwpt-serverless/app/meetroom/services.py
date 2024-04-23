import sqlalchemy.orm as orm
import users.models
# from jwxt.app import redis
from users.services import redis
import json
from typing import List
from base import database
from app.meetroom import models,schemas
from datetime import datetime
from sqlalchemy import and_
from autoserver import getJwxtTicketFromAutoServer
from jwxt import checkJwxtCookies,getJwxtCookieFromTicketUrl
from users.utils import cipher_suite
import httpx

import requests
from jwxt.getHeader import jwxtHedaer
from jwxt.getUrl import freeRoomUrl

from bs4 import BeautifulSoup
import re
async def submit_book_room(db: orm.Session,openid: str,schema: schemas.SubmitBookRoomSchema) -> schemas.OutSchema:
    if redis.exists(openid):
        cookies = redis.get(openid)
        retn = await checkJwxtCookies(cookies)
        if retn != False:
            pass
        else:
            existing_item = db.query(users.models.User).filter_by(openid = openid).first()
            success, locationUrl = getJwxtTicketFromAutoServer(existing_item.xsxh,cipher_suite.decrypt(existing_item.password).decode())
            if success:
                success, cookies =  getJwxtCookieFromTicketUrl(locationUrl)
                redis.set(openid,cookies)
    else:
        existing_item = db.query(users.models.User).filter_by(openid = openid).first()
        success, locationUrl = getJwxtTicketFromAutoServer(existing_item.xsxh,cipher_suite.decrypt(existing_item.password).decode())
        if success:
            success, cookies = getJwxtCookieFromTicketUrl(locationUrl)
            redis.set(openid,cookies)
    book_info = db.query(models.BookRoom).filter(models.BookRoom.id == schema.book_id).first()
    ret = await get_user_id_from_jwxt(openid,book_info.xsxh)
    return schemas.OutSchema(
        code = 0,
        tip = str(ret)
    )

def get_book_room(db: orm.Session,openid: str) -> List[schemas.OutBookRoomSchema]:
    try:
        books = db.query(models.BookRoom).filter(models.BookRoom.finished == 0).all()
        out_list = [
            schemas.OutBookRoomSchema(
                _id = item.id,
                code = 0,
                tip = "",
                name = item.name,
                phone = item.phone,
                reason = item.reason,
                roomname = item.roomname,
                week = item.week,
                week1 = item.week1,
                section = item.section
            )
            for item in books
        ]
        return out_list
    except Exception as e:
        return []
def book_room(db: orm.Session,openid: str,schema: schemas.BookRoomSchema) -> schemas.OutSchema:
    try:
        
        user = db.query(users.models.User).filter_by(openid = openid).first()
        new_book = models.BookRoom(
            openid = openid,
            xsxh = user.xsxh,
            name = user.name,
            phone = schema.phone,
            roomname = schema.roomname,
            reason = schema.reason,
            week = schema.week,
            week1 = schema.week1,
            section = schema.section,
            finished = 0
        )
        db.add(new_book)
        db.commit()
        return schemas.OutSchema(
            code = 0,
            tip = "预定成功 等待审批"
        )
    except Exception as e:
        return schemas.OutSchema(
            code = 1,
            tip = f"预定失败 {e}"
        )
async def search_room(db: orm.Session,openid: str,schema: schemas.SearchRoomSchema) -> schemas.OutFreeRoomSchema:
    try:
        if redis.exists(openid):
            cookies = redis.get(openid)
            retn = await checkJwxtCookies(cookies)
            if retn != False:
                pass
            else:
                existing_item = db.query(users.models.User).filter_by(openid = openid).first()
                success, locationUrl = getJwxtTicketFromAutoServer(existing_item.xsxh,cipher_suite.decrypt(existing_item.password).decode())
                if success:
                    success, cookies =  getJwxtCookieFromTicketUrl(locationUrl)
                    redis.set(openid,cookies)
        else:
            existing_item = db.query(users.models.User).filter_by(openid = openid).first()
            success, locationUrl = getJwxtTicketFromAutoServer(existing_item.xsxh,cipher_suite.decrypt(existing_item.password).decode())
            if success:
                success, cookies = getJwxtCookieFromTicketUrl(locationUrl)
                retn = await checkJwxtCookies(cookies)
                redis.set(openid,cookies)
    except Exception as e:
        print(e)
    free_room_list = await get_freeroom_from_jwxt(openid,schema.date,schema.section)
    # return schemas.OutFreeRoomSchema(
    #     code = 0,
    #     tip = "",
    #     classroom = json.dumps(free_room_list,ensure_ascii=False)
    # )
    return schemas.OutFreeRoomSchema(
        code = 0,
        tip = "",
        classroom = free_room_list
    )
async def get_user_id_from_jwxt(openid,xsxh):
    cookies = redis.get(openid)
    try:
        async with httpx.AsyncClient() as client:
            url = 'https://jwxt.neuq.edu.cn/eams/classroom/apply/teacher-activity!getBorrowers.action?pageNo=1&pageSize=10&term='+ str(xsxh)
            response = await client.get(url, headers=jwxtHedaer,cookies=cookies)
            if response.status_code == 200:
                print(response.text["users"])
                return response.text
    except Exception as e:
        return e

async def get_freeroom_from_jwxt(openid,date,section):
    cookies = redis.get(openid)
    try:
        async with httpx.AsyncClient() as client:
            data = {
                'classroom.type.id': '',
                'classroom.campus.id': '',
                'classroom.building.id': '1',
                'seats': '',
                'classroom.name': '',
                'cycleTime.cycleCount': '1',
                'cycleTime.cycleType': '1',
                'cycleTime.dateBegin': date, # '2024-03-26'
                'cycleTime.dateEnd': date,
                'roomApplyTimeType': '0',
                'timeBegin': str(section),
                'timeEnd': str(section+1)
            }
            response = await client.post(freeRoomUrl, headers=jwxtHedaer,cookies=cookies,data=data)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                table = soup.find("table")
                if table:
                    body = table.find("tbody")
                    tr = body.find_all("tr")
                    free_room = []
                    for item in tr:
                        _ = str(item.find_all('td')).replace(" ",'')
                        temp = re.findall("<td>(.*?)</td>",_,re.S)
                        free_room.append(temp[1])
                    return free_room[:-2]
                else:
                    return False
            else:
                return False
    except Exception as e:
        print(e)
        return False

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()