import bs4
from bs4 import BeautifulSoup
from constants.constants import my_constants

class DataExtractor(BeautifulSoup):
    def __init__(self, highschool_name, html, praser="html.parser", **kwargs):
        super().__init__(html, praser, **kwargs)
        self.highschool_name = highschool_name
        self.html = html
        self.praser = "html.praser"

    def both_where_sche(self):
        main_table = self.find("table", role="main")
        table_main_row = main_table.find_all("tr")[1]
        table_row = table_main_row.find("tr", valign="top")
        table_datas = table_row.find_all("td", valign="top")
        whereabouts = table_datas[0]
        schedule = table_datas[1]

        return whereabouts, schedule

    def whereabouts(self, whereabouts: bs4.element.Tag):
        table_rows = whereabouts.find_all("tr", class_="listroweven")
        img_url, counselor_name, age, locker = None, None, None, None
        for idx, table_row in enumerate(table_rows):
            if idx == 0:
                image_src = table_row.find("img").attrs['src']
                img_url = my_constants[self.highschool_name]['root'] + image_src
            if idx == 2:
                counselor_name = str(table_row.text).split(":")[1].strip()
            if idx == 3:
                age = str(table_row.text).split(":")[1].strip()
            if idx == 4:
                locker = str(table_row.text).split(":")[1].strip()
        return (img_url, counselor_name, age, locker)

    def schedule(self, schedule: bs4.element.Tag):
        name, grade, student_id, state_id = None, None, None, None

        table = schedule.find("table", style="margin: auto; min-width: 500px;")
        td_a = table.find_all("td", class_="cellLeft", style="border: 0;")[0].find("a")
        schedule_link = my_constants[self.highschool_name]['root'] + str(td_a.attrs['href'])

        table = schedule.find("table")
        rows = table.find_all("tr")
        for idx, row in enumerate(rows):
            if idx == 0:
                name_without_last = str(row.find("span").text).strip("\n")
                thing = str(row.text).split("Grade:")
                name_last = thing[0].strip("\n").strip(name_without_last).strip()
                name = name_without_last + " " + name_last
                grade = str(thing[1]).strip("0").strip()

            if idx == 1:
                merge = row.find_all("span")
                student_id = str(merge[0].text).strip()
                state_id = str(merge[1].text).strip()

        return (schedule_link, name, grade, student_id, state_id)

