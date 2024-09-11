from flask import Flask, request, jsonify, jsonify
app = Flask(__name__)

requestform = {'KEY' : '322f1dd4d7da4766a9c6828c4d861880',
               'Type' : 'json',
               'plndex' : 1,
               'pSize' : 100}
niceurl = 'https://open.neis.go.kr/hub/mealServiceDietInfo?KEY=322f1dd4d7da4766a9c6828c4d861880&Type=json&pIndex=1&pSize=100&ATPT_OFCDC_SC_CODE=R10&SD_SCHUL_CODE=8750594'
@app.route('/')
def lobby():
    return 'on running'

@app.route('/request', methods=['GET'])
def sendData():

    respone = request.get_json(niceurl)

    return respone


if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')