from flask import Flask,jsonify
import requests
from flask_cors import CORS
from .main import latest_updates()

app = Flask(__name__)
CORS(app)
@app.route('/hello',methods=['GET'])
def test():
    return jsonify("connected")

@app.route('latest',methods=['GET'])
def latest():
    api = latest_updates()
    return api



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)


