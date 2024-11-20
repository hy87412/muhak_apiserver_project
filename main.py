import datetime
from flask import Flask, jsonify, render_template
import requests
import json

app = Flask(__name__)

with open('keys.json', 'r') as keys:
    json_dic = json.load(keys)
    bobkey = json_dic['key1']
    datekey = json_dic['key2']
urlform1 = 'https://open.neis.go.kr/hub/mealServiceDietInfo?KEY=' + bobkey + '&MLSV_YMD='
urlform2 = '&Type=json&pIndex=1&pSize=100&ATPT_OFCDC_SC_CODE=R10&SD_SCHUL_CODE=8750594'
niceboburl = 'https://open.neis.go.kr/hub/mealServiceDietInfo?KEY=322f1dd4d7da4766a9c6828c4d861880&MLSV_YMD=20241102&Type=json&pIndex=1&pSize=100&ATPT_OFCDC_SC_CODE=R10&SD_SCHUL_CODE=8750594'
planurlform = 'https://open.neis.go.kr/hub/SchoolSchedule?KEY=' + datekey + '&Type=json&pIndex=1&pSize=100&ATPT_OFCDC_SC_CODE=R10&SD_SCHUL_CODE=8750594'

#variables
latestupdatedate = "00000000"

originpageform = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>무학밥</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #354550;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        h1 {
            margin-top: 20px;
            color: #333;
        }
        .meal-container {
            width: 100%;
            max-width: 500px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 20px;
            margin-top: 20px;
            padding: 0 10px;
        }
        .meal {
            background-color: white;
            width: 100%;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        .meal h2 {
            margin-bottom: 10px;
            color: #007BFF;
        }
        .meal p {
            color: #555;
        }

        /* 이미지 스타일 */
        .meal img {
            width: 100%;
            height: auto;
            border-radius: 10px; /* 카드 모서리에 맞추어 이미지도 둥글게 */
            margin-top: 10px;
        }
    </style>
</head>
<body>

    <div class="meal-container">
        <!-- 조식 섹션 -->
        <div class="meal">
            <h2>조식 {fkcal0f}</h2>
            <p>{fbob0f}</p>
        </div>

        <!-- 중식 섹션 -->
        <div class="meal">
            <h2>중식 {fkcal1f}</h2>
            <p>{fbob1f}</p>
        </div>

        <!-- 석식 섹션 -->
        <div class="meal">
            <h2>석식 {fkcal2f}</h2>
            <p>{fbob2f}</p>
        </div>

        <!-- 학사일정 섹션 -->
        <div class="meal">
            <h2>학사일정</h2>
            <p>{frow0valuef}</p>
        </div>

        <!-- D-day 섹션 -->
        <div class="meal">
            <h2>D-day</h2>
            <p>{frow1valuef}</p>
        </div>

        <!-- JWS 섹션 -->
        <div class="meal">
            <h2>Who we are</h2>
            <a href="https://www.mubob.com/jws" target="_blank">
                <img src="{{ url_for('static', filename='images/JWSlogo.png')}}" alt="링크 아이콘" class="link-icon">
            </a>
        </div>
    </div>

</body>
</html>
"""

def getdate() :
    time = datetime.datetime.now()
    year = str(time.year).zfill(2)
    month = str(time.month).zfill(2)
    day = str(time.day).zfill(2)
    todaydate = year + month + day
    result = str(todaydate)
    return result

def determineyearrange(point) :
    if point == 'end' :
        nowymd = getdate()
        return nowymd[:4] + '1231'
    elif point == 'begin' :
        return getdate()

def calculate_dday(target_date_str):
    today = datetime.datetime.today().date()
    target_date = datetime.datetime.strptime(target_date_str, "%Y%m%d").date()
    dday = (target_date - today).days
    return dday

def updatepage():
    editpageform = originpageform
    response = requests.get(urlform1 + getdate() + urlform2)
    # response = requests.get(niceboburl)
    bobdata = response.json()
    boblist = []
    kcallist = []
    try :
        for item in bobdata["mealServiceDietInfo"][1]["row"]:
            boblist.append(item["DDISH_NM"])
        for item in bobdata["mealServiceDietInfo"][1]["row"]:
            kcallist.append(item["CAL_INFO"])
    except :
        boblist = ['오늘은 밥이 없어요...','오늘은 밥이 없어요...','오늘은 밥이 없어요...']
        kcallist = ['','','']
    for i in range(3) :
        try :
            editpageform = editpageform.replace(f'{{fbob{i}f}}', boblist[i])
            editpageform = editpageform.replace(f'{{fkcal{i}f}}', kcallist[i])
        except :
            editpageform = editpageform.replace(f'{{fbob{i}f}}', '밥없어')
            editpageform = editpageform.replace(f'{{fkcal{i}f}}', '밥없어')

    plandata = requests.get(planurlform + '&AA_FROM_YMD=' + getdate() + '&AA_TO_YMD=' + determineyearrange('end')).json()

    planlist = []
    count = 0
    for item in plandata["SchoolSchedule"][1]["row"] :
        if item["EVENT_NM"] != '토요휴업일' :
            planlist.append(item["AA_YMD"] + "-" + item["EVENT_NM"])
            count = count + 1
        if count == 15 :
            break
    editpageform = editpageform.replace('{frow0valuef}', '<br/>'.join(planlist))

    for item in plandata["SchoolSchedule"][1]["row"] :
        if item['EVENT_NM'] == '지필 1회(1,2년)' or item['EVENT_NM'] == '지필 2회(1,2년)' :
            grade12 = item['AA_YMD']
            break
    for item in plandata["SchoolSchedule"][1]["row"] :
        if item['EVENT_NM'] == '지필 1회(3년)' or item['EVENT_NM'] == '지필 2회(3년)' :
            grade3 = item['AA_YMD']
            break
    try :
        dday12 = calculate_dday(grade12)
    except :
        now = getdate()
        dday12 = '{}년 시험을 다쳤어요 :)'.format(now[:4])
    try :
        dday3 = calculate_dday(grade3)
    except :
        now = getdate()
        dday3 = '{}년 시험을 다쳤어요 :)'.format(now[:4])
    editpageform = editpageform.replace('{frow1valuef}',f'1,2학년 : {dday12} <br/>3학년 : {dday3}')
    with open('templates/bobpage.html', 'w', encoding='utf-8') as file:
        file.write(editpageform)

#server route code

@app.route('/state')
def lobby():
    return 'on running'

@app.route('/request')
def sendData():
    respone = requests.get(urlform1 + getdate() + urlform2)
    # respone = requests.get(niceurl)
    data = respone.json()
    return data

@app.route('/jws')
def sendjwspage():
    return render_template('JWSpage.html')

@app.route('/')
def sendlobbypage():
    global latestupdatedate
    if latestupdatedate != getdate() :
        updatepage()
        latestupdatedate = getdate()
    return render_template('bobpage.html')

if __name__ == "__main__":
    app.run(debug=False, port=5000, host='0.0.0.0')