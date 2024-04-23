import sqlalchemy.orm as orm
import json
from typing import List
from base import database
import users.utils as utils
import users.models
# from jwxt.app import redis
from users.services import redis
from autoserver import getJwxtTicketFromAutoServer
from jwxt import checkJwxtCookies,getJwxtCookieFromTicketUrl
from jwxt.app.score import schemas
from jwxt.app.score.utils import semester_mapping
from bs4 import BeautifulSoup
import httpx
from users.utils import cipher_suite
async def search_score(db: orm.Session,openid: str,schema: schemas.SearchScoreSchema) -> schemas.OutScoreSchema:
    if redis.exists(openid):
        cookies = redis.get(openid)
        retn = await checkJwxtCookies(cookies)
        if retn != False:
            pass
        else:
            existing_item = db.query(users.models.User).filter_by(openid = openid).first()
            success, locationUrl = getJwxtTicketFromAutoServer(existing_item.xsxh,cipher_suite.decrypt(existing_item.password).decode())
            if success:
                success, cookies = getJwxtCookieFromTicketUrl(locationUrl)
                redis.set(openid,cookies)
    else:
        existing_item = db.query(users.models.User).filter_by(openid = openid).first()
        success, locationUrl = getJwxtTicketFromAutoServer(existing_item.xsxh,cipher_suite.decrypt(existing_item.password).decode())
        if success:
            success, cookies = getJwxtCookieFromTicketUrl(locationUrl)
            redis.set(openid,cookies)
    gdp,table = await search_score_from_jwxt(schema.semester,openid)
    if gdp and table:
        return schemas.OutScoreSchema(
            code = 0,
            tip = "cookie获取有效 执行查询函数",
            gdp_string = gdp,
            table = table
        )
    else:
        return schemas.OutScoreSchema(
            code = 1,
            tip = "查询失败",
            gdp_string = '',
            table = ''
        )

async def search_score_from_jwxt(semester,openid):
    cookies = redis.get(openid)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
    }
    try:
        async with httpx.AsyncClient() as client:
            url = 'https://jwxt.neuq.edu.cn/eams/teach/grade/course/person!search.action?semesterId={0}&projectType={1}'.format(semester,None)
            response = await client.get(url, headers=headers,cookies=cookies)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                gdp_string = soup.find('div', string=lambda text: '总平均绩点' in text and '校内专用绩点' in text)
                
                table = soup.find('table', class_='gridtable')
                table_data = []
                for row in table.find_all('tr'):
                    row_data = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
                    table_data.append(','.join(row_data))
                
                return gdp_string.get_text(strip=True),table_data[1:]
            else:
                return False,False
    except Exception as e:
        return e,False


def get_semester():
    return semester_mapping
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()