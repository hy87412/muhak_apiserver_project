import datetime
from flask import Flask, jsonify
import requests
import json
app = Flask(__name__)

requestform = {'KEY':'322f1dd4d7da4766a9c6828c4d861880',
               'Type':'json',
               'plndex':1,
               'pSize':100}
basicform1 = 'https://open.neis.go.kr/hub/mealServiceDietInfo?KEY=322f1dd4d7da4766a9c6828c4d861880&MLSV_YMD='
basicform2 = '&Type=json&pIndex=1&pSize=100&ATPT_OFCDC_SC_CODE=R10&SD_SCHUL_CODE=8750594'
def getdate() :
    time = datetime.datetime.now()
    time = datetime.datetime.now()
    year = str(time.year).zfill(2)
    month = str(time.month).zfill(2)
    day = str(time.day).zfill(2)
    todaydate = year + month + day
    result = str(todaydate)
    return result
niceurl = 'https://open.neis.go.kr/hub/mealServiceDietInfo?KEY=322f1dd4d7da4766a9c6828c4d861880&MLSV_YMD=20241016&Type=json&pIndex=1&pSize=100&ATPT_OFCDC_SC_CODE=R10&SD_SCHUL_CODE=8750594'



@app.route('/')
def lobby():
    return 'on running'

@app.route('/test', methods=['GET'])
def test():
    return jsonify(requestform)

@app.route('/request', methods=['GET'])
def sendData():

    respone = requests.post(basicform1 + getdate() + basicform2)
    data = respone.json()
    return data

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')