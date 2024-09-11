from flask import Flask, request, jsonify, jsonify
app = Flask(__name__)

@app.route('/')
def lobby():
    return 'on running'

@app.route('/get', methods=['GET'])
def sendData():


    response = {
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')