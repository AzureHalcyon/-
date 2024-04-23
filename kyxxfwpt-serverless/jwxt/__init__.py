
from lxml import etree
from jwxt.getHeader import jwxtHedaer
from jwxt.getUrl import myActionUrl
import httpx
from requests.utils import dict_from_cookiejar
import requests
async def checkJwxtCookies(cookies):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(myActionUrl, headers=jwxtHedaer,cookies=cookies)
            if response.status_code == 200:
                tree = etree.HTML(response.text)
                UserInfoTableElements = tree.xpath('//*[@id="user-info"]/div/div[2]/table')
                if UserInfoTableElements:
                    info_table_html = etree.tostring(UserInfoTableElements[0], method='html', pretty_print=True, encoding='utf-8').decode('utf-8')
                    return info_table_html
                else:
                    return False
            else:
                return False
    except Exception as e:
        print(e)
        return False
# httpx这里获取的cookies不全
# async def getJwxtCookieFromTicketUrl(TicketUrl: str):
#     try:
#         async with httpx.AsyncClient() as client:
#             response = await client.get(TicketUrl, headers=jwxtHedaer)
#             cookies = client.cookies
#             print(cookies)
#             return True, cookies
#     except Exception as e:
#         return False, str(e)
def getJwxtCookieFromTicketUrl(TicketUrl: str):
    try:
        session = requests.Session()
        response = session.get(TicketUrl,headers = jwxtHedaer)
        return True, session.cookies
    except Exception as e:
        return False, str(e)
# async def update_cookies(openid):
#     if redis.exists(openid):
#         cookies = redis.get(openid)
#         retn = await checkJwxtCookies(cookies)
#         if retn != False:
#             pass
#         else:
#             existing_item = db.query(users.models.User).filter_by(openid = openid).first()
#             success, locationUrl = getJwxtTicketFromAutoServer(existing_item.xsxh,cipher_suite.decrypt(existing_item.password).decode())
#             if success:
#                 success, cookies = await getJwxtCookieFromTicketUrl(locationUrl)
#                 redis.set(openid,cookies)
#     else:
#         existing_item = db.query(users.models.User).filter_by(openid = openid).first()
#         success, locationUrl = getJwxtTicketFromAutoServer(existing_item.xsxh,cipher_suite.decrypt(existing_item.password).decode())
#         if success:
#             success, cookies = await getJwxtCookieFromTicketUrl(locationUrl)
#             redis.set(openid,cookies)