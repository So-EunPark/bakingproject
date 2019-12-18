from flask import Flask, render_template, jsonify, request

import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.baking  # 'dbsparta'라는 이름의 db를 만듭니다.

@app.route('/baking', methods=['GET'])
def getbakingPage():
    return render_template("index.html")


if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)