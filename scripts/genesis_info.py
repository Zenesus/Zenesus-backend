import aiohttp
from constants.constants import my_constants
from urllib.parse import urlparse
from urllib.parse import parse_qs
from scripts.data import DataExtractor

class GenesisInformation():
    def __init__(self):
        pass

    @staticmethod
    async def get_cookie(email, password, session: aiohttp.ClientSession, highschool_name):
        data = my_constants[highschool_name]["data"]
        data["j_username"] = email
        data["j_password"] = password
        async with session as my_session:
            async with my_session.post(url=my_constants[highschool_name]['j_check'], data=data) as response:
                cookie = my_session.cookie_jar.filter_cookies(my_constants[highschool_name]['j_check'])
                j_id = str(cookie["JSESSIONID"]).split("=")[1]

                url = str(response.url)
                parsed_url = urlparse(url)
                captured_data = parse_qs(parsed_url.query)

                return j_id, captured_data, url

    @staticmethod
    async def front_page_data(highschool_name, j_session_id, url):
        async with aiohttp.ClientSession(cookies={"JSESSIONID": j_session_id}) as session:
            response = await session.get(url=url)
            html = await response.text()

            soup = DataExtractor(highschool_name, html, "html.parser")
            whereabouts, schedule = soup.both_where_sche()
            img_url, counselor_name, age, locker = soup.whereabouts(whereabouts)
            schedule_link, name, grade, student_id, state_id = soup.schedule(schedule)
            return (img_url, counselor_name, age, locker, schedule_link, name, grade, student_id, state_id)
