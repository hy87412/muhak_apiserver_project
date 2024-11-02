import datetime
from flask import Flask, jsonify, render_template
import requests
import json

app = Flask(__name__)

bobkey = '322f1dd4d7da4766a9c6828c4d861880'
datekey = '49fb1d96db7144808dfcb388fb0cc326'
urlform1 = 'https://open.neis.go.kr/hub/mealServiceDietInfo?KEY=' + bobkey + '&MLSV_YMD='
urlform2 = '&Type=json&pIndex=1&pSize=100&ATPT_OFCDC_SC_CODE=R10&SD_SCHUL_CODE=8750594'
niceboburl = 'https://open.neis.go.kr/hub/mealServiceDietInfo?KEY=322f1dd4d7da4766a9c6828c4d861880&MLSV_YMD=20241016&Type=json&pIndex=1&pSize=100&ATPT_OFCDC_SC_CODE=R10&SD_SCHUL_CODE=8750594'
dateform = 'https://open.neis.go.kr/hub/SchoolSchedule?KEY=' + datekey + '&Type=json&pIndex=1&pSize=100&ATPT_OFCDC_SC_CODE=R10&SD_SCHUL_CODE=8750594'

originpageform = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>오늘의 식단</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f9f9f9;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        h1 {
            margin-top: 20px;
            color: #333;
        }
        .meal-container {
            display: flex;
            justify-content: space-between;
            width: 80%;
            margin-top: 30px;
            gap: 40px; /* 섹션 사이 간격 추가 */
        }
        .meal {
            background-color: white;
            width: 30%;
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
    </style>
</head>
<body>

    <h1>오늘의 식단</h1>

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
    </div>

    <div class="meal-container">
        <!-- 하단 0열 -->
        <div class="meal">
            <h2>학사일정</h2>
            <p>{flow0valuef}</p>
        </div>

        <!-- 하단 1열 -->
        <div class="meal">
            <h2>D-day</h2>
            <p>{flow1valuef}</p>
        </div>

        <!-- 하단 2열 -->
        <div class="meal">
            <h2>Jaewon Foundation</h2>
            <p>{flow2valuef}</p>
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

def updatepage():
    response = requests.get(urlform1 + getdate() + urlform2)
    # response = requests.get(niceboburl)
    bobdata = response.json()
    boblist = []
    for item in bobdata["mealServiceDietInfo"][1]["row"]:
        boblist.append(item["DDISH_NM"])
    kcallist = []
    for item in bobdata["mealServiceDietInfo"][1]["row"]:
        kcallist.append(item["CAL_INFO"])
    editpageform = originpageform
    for i in range(3) :
        try :
            editpageform = editpageform.replace(f'{{fbob{i}f}}', boblist[i])
            editpageform = editpageform.replace(f'{{fkcal{i}f}}', kcallist[i])
        except :
            editpageform = editpageform.replace(f'{{fbob{i}f}}', '밥없어')
            editpageform = editpageform.replace(f'{{fkcal{i}f}}', '밥없어')
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

@app.route('/')
def page():
    updatepage()
    return render_template('bobpage.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')