import aiohttp
from bs4 import BeautifulSoup
from constants.constants import my_constants

class GenesisInformation():
    def __init__(self, username, password):
        self.username=username
        self.password=password
        pass

    def get_cookie(self, session: aiohttp.ClientSession, highschool_name):
        data = my_constants["data"]
        data["j_username"] = self.username
        data["j_password"] = self.password
        self.fetch_response(session, "POST", url=my_constants[highschool_name], data=data)

    @staticmethod
    def fetch_response(session, method="GET", *args, **kwargs):
        if method == "GET":
            async with session.get(*args, **kwargs) as response:
                return response, await response.text()
        elif method == "POST":
            async with session.post(*args, **kwargs) as response:
                return response
