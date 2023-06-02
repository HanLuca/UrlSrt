from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
import requests, json, string, random, os, asyncio
from control import Data

app = Flask(__name__)

# 데이터베이스 파일 경로
DATABASE_FILE = 'links.json'

# 데이터베이스 초기화
if not os.path.exists(DATABASE_FILE):
    with open(DATABASE_FILE, 'w') as f:
        json.dump({}, f)

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
    if short_url == "fv":
        return redirect(file_view)
    else:
        original_url = get_url(short_url)
        if original_url is not None:
            return render_template('notice.html', url=original_url, stas=None)

        else:
            return render_template('notice.html', url=original_url, stas="URL Error")

@app.route('/fv')
def file_view():
    with open('links.json') as f:
        data = json.load(f)
    return render_template('fileView.html', data=data)


MONITOR_ID = "793840902"
url = "https://api.uptimerobot.com/v2/getMonitors"

@app.route('/ut')
def uptime():
    url = "https://api.uptimerobot.com/v2/getMonitors"

    payload = {
        "api_key": os.environ['API_KEY'],
        "format": "json",
        "monitors": "793840902"
    }

    response = requests.post(url, data=payload)
    data = response.json()

    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)