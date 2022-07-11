from flask import Flask, session, url_for, make_response, jsonify, request
import aiohttp
import os
from dotenv import load_dotenv
from scripts.genesis_info import GenesisInformation
import json


class Storage():
    def __init__(self):
        pass


load_dotenv()
myInfo = GenesisInformation()
app = Flask(__name__)
app.config["SECRET_KEY"] = f"{os.urandom(24).hex()}"
STORAGE = Storage()

def parse_request_data(request_data):
    email = request_data['email']
    password = request_data['password']
    highschool = request_data['highschool']
    STORAGE.email = email
    STORAGE.password = password
    STORAGE.highschool = highschool
    STORAGE.mp = request_data['mp']


def get():
    email = STORAGE.email
    password = STORAGE.password
    highschool = STORAGE.highschool
    mp = STORAGE.mp
    return email, password, highschool, mp


async def initialize(session, email, password, highschool):
    j_session_id, parameter_data, url = await myInfo.get_cookie(email, password, session, highschool)
    front_page_data = await myInfo.front_page_data(highschool, j_session_id, url)
    users, img_url, counselor_name, age, birthday, locker, schedule_link, name, grade, student_id, state_id = front_page_data
    return j_session_id, users, img_url, counselor_name, age, birthday, locker, schedule_link, name, grade, student_id, state_id


@app.route("/api/p/update", methods=["POST"])
async def update():
    request_data = request.data
    request_data = json.loads(request_data.decode('utf-8'))
    parse_request_data(request_data)
    return ""

@app.route("/api/login", methods=["GET", "POST"])
async def getgrade():
    if request.method == "POST":
        request_data = request.data
        request_data = json.loads(request_data.decode('utf-8'))
        parse_request_data(request_data)
        return ""
    elif request.method == "GET":
        data = {}
        async with aiohttp.ClientSession() as session:
            email, password, highschool, mp = get()
            j_session_id, users, img_url, counselor_name, age, birthday, locker, schedule_link, name, grade, student_id, state_id = await initialize(
                session, email, password, highschool)

            data['users'] = users
            data['img_url'] = img_url
            data['counselor_name'] = counselor_name
            data['age'] = age
            data['birthday'] = birthday
            data['locker'] = locker
            data['schedule_link'] = schedule_link
            data['name'] = name
            data['grade'] = grade
            data['student_id'] = student_id
            data['state_id'] = state_id

        return jsonify(data)


@app.route("/api/get/courseinfos", methods=["GET"])
async def getcourseinfo():
    async with aiohttp.ClientSession() as session:
        email, password, highschool, mp = get()
        j_session_id, users, img_url, counselor_name, age, birthday, locker, schedule_link, name, grade, student_id, state_id = await initialize(
            session, email, password, highschool)

        grade_page_data = await myInfo.grade_page_data(highschool, j_session_id, student_id, mp)

        return jsonify(grade_page_data)


@app.route("/api/get/currentgrades", methods=["GET"])
async def currentgrades():
    async with aiohttp.ClientSession() as session:
        email, password, highschool, mp = get()
        j_session_id, users, img_url, counselor_name, age, birthday, locker, schedule_link, name, grade, student_id, state_id = await initialize(
            session, email, password, highschool)


if __name__ == '__main__':
    app.run(host="10.0.2.2", port=5000, debug=True)
