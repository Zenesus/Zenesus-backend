from flask import Flask, session, url_for, make_response, jsonify, request
import aiohttp
import os
from dotenv import load_dotenv
from scripts.genesis_info import GenesisInformation
import json

load_dotenv()
myInfo = GenesisInformation()
email, password = None, None
app = Flask(__name__)
app.config["SECRET_KEY"] = f"{os.urandom(24).hex()}"

@app.route("/api/getgrade", methods=["GET", "POST"])
async def getgrade():

    global email, password

    if request.method == "POST":
        request_data = request.data
        request_data = json.loads(request_data.decode('utf-8'))
        email = request_data['email']
        password = request_data['password']
        return ""
    elif request.method == "GET":
        data = {}
        async with aiohttp.ClientSession() as session:
            j_session_id, parameter_data, url = await myInfo.get_cookie(email, password, session, "Montgomery Highschool")
            front_page_data = await myInfo.front_page_data("Montgomery Highschool", j_session_id, url)
            users, img_url, counselor_name, age, birthday, locker, schedule_link, name, grade, student_id, state_id = front_page_data
            # print(users, img_url, counselor_name, age, birthday, locker, schedule_link, name, grade, student_id, state_id)
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




if __name__ == '__main__':
    app.run(host="10.0.2.2", port=5000, debug=True)
