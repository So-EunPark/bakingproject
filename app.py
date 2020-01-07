from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
import requests
from bs4 import BeautifulSoup



app = Flask(__name__)



client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.baking  # 'dbsparta'라는 이름의 db를 만듭니다.


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def home():
    text = request.form['text']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(
        'https://search.naver.com/search.naver?date_from=&date_option=0&date_to=&dup_remove=1&nso=&post_blogurl=&post_blogurl_without=&query='+text+'&sm=tab_pge&srchby=all&st=sim&where=post&start=1',
        headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')
    # select를 이용해서, dismissable들을 불러오기
    nvbakingPost = soup.select('#elThumbnailResultArea > li.sh_blog_top')

    # 네이버 검색창 블로그 검색결과
    for nvPost in nvbakingPost:
        nvPost_thumbnail_tag = nvPost.select_one('img')
        nvPost_thumbnail = nvPost_thumbnail_tag['src']
        nvPost_title_tag = nvPost.select_one('a.sh_blog_title._sp_each_url._sp_each_title')
        nvPost_title = nvPost_title_tag.text
        nvPost_url = nvPost.select_one('a.sh_blog_title._sp_each_url._sp_each_title')['href']
        nvPost_poster = nvPost.select_one('dd.txt_block>span.inline>a.txt84').text
        nvPost_date = nvPost.select_one(' dl > dd.txt_inline').text
        print(nvPost_thumbnail, nvPost_title, nvPost_url, nvPost_poster, nvPost_date)
        doc = {
            'nvPost_thumbnail': nvPost_thumbnail,
            'nvPost_title': nvPost_title,
            'nvPost_url': nvPost_url,
            'nvPost_date': nvPost_date,
            'nvPost_poster': nvPost_poster

        }
        # db.nvBakingPost.insert_one(doc)

    return jsonify({'result': 'success'})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)
