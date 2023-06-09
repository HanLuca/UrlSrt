from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
import requests, json, string, random, os, asyncio
from control import Data

from secret import UPTIME_APIKEY

app = Flask(__name__)

# 짧은 URL 생성 함수
def generate_short_url():
    while True:
        short_url = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        
        if Data.dataCheck(f"URL/{short_url}") == False:
            return short_url

        else:
            continue

# URL 저장 함수
def save_url(original_url, short_url):
    basicPath = f"URL/{short_url}"  
    
    Data.dataUpdate(basicPath, {"Original" : original_url}, {"User" : request.remote_addr})

# URL 조회 함수
def get_url(short_url):
    basicPath = f"URL/{short_url}"
    
    return Data.dataGet(basicPath, "Original")

# 루트 페이지
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['url']
        try:
            response = requests.get(original_url)
        except:
            return render_template('error.html', error='존재하지 않는 URL 입니다.')
        else:
            short_url = generate_short_url()
            save_url(original_url, short_url)

            return render_template('result.html', short_url=short_url)
    else:
        return render_template('index.html')

# 짧은 URL 리다이렉트
@app.route('/<short_url>')
def redirect_to_url(short_url):
    original_url = get_url(short_url)
    if original_url is not None:
        return render_template('notice.html', url=original_url, stas=None)

    else:
        return render_template('notice.html', url=original_url, stas="URL Error")


@app.route('/uptime')
def uptime():
    url = "https://api.uptimerobot.com/v2/getMonitors"
    monitorsList = ["793840902", "794492252"]
    datas = []

    for i in monitorsList:
        payload = {
            "api_key": UPTIME_APIKEY,
            "format": "json",
            "monitors": i
        }
        response = requests.post(url, data=payload)
        datas.append(f"{response.json()['monitors'][0]['friendly_name']} : {response.json()['stat']}")

    return datas

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)