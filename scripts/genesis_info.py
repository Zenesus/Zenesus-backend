import aiohttp
from bs4 import BeautifulSoup
from constants.constants import my_constants

class GenesisInformation():
    def __init__(self):
        pass

    async def get_cookie(self, email, password, session: aiohttp.ClientSession, highschool_name):
        data = my_constants[highschool_name]["data"]
        data["j_username"] = email
        data["j_password"] = password
        async with session as my_session:
            async with my_session.post(url=my_constants[highschool_name]['j_check'], data=data) as response:
                return response, my_session.cookie_jar.filter_cookies(my_constants[highschool_name]['j_check'])
