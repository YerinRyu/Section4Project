from flask import Blueprint, url_for, render_template
from werkzeug.utils import redirect

bp = Blueprint('clothes', __name__, url_prefix='/')


import requests
import json

API_key = 'a70dc2963798086f5d430b6af4a55004'
city_name = 'Seoul'

URL = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key}&units=metric"

row_data = requests.get(URL)
current_weather = json.loads(row_data.text)


@bp.route('/clothes')
def hello_clothes():
    
    temp = current_weather['main']['temp']
    weather = current_weather['weather'][0]['main']
    
    if temp >= 28:
        answer = "민소매, 반팔, 반바지, 원피스"
    elif temp >= 23:
        answer = "반팔, 얇은 셔츠, 반바지, 면바지"
    elif temp >= 20:
        answer = "얇은 가디건, 반팔, 면바지, 청바지"
    elif temp >= 17:
        answer = "얇은 니트, 맨투맨, 가디건, 청바지"
    elif temp >= 12:
        answer = "자켓, 가디건, 야상, 스타킹, 청바지, 면바지"
    elif temp >= 9:
        answer = "자켓, 트렌치코트, 야상, 니트, 청바지, 스타킹"
    elif temp >= 5:
        answer = "코트, 가죽자켓, 히트텍, 니트, 레깅스"
    else:
        answer = "패딩, 두꺼운 코트, 목도리, 기모제품"
    
    return render_template('clothes.html', temp=temp, weather=weather, answer=answer)

