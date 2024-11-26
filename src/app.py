from flask import Flask,jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route('/hello',methods=['GET'])
def test():
    return jsonify("connected")

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)


