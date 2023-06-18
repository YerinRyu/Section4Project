from flask import Blueprint, url_for, render_template, request
from werkzeug.utils import redirect
import pickle
import pandas as pd
import traceback
import time

# 기온 예측
with open('/Users/yerin/AIB/section4/project/PART2_Modeling/model_ta.pkl','rb') as pickle_file:
    model_ta = pickle.load(pickle_file)
    
# 강수 예측
# 0 = 많은 비, 1 = 비 안옴, 2 = 비
with open('/Users/yerin/AIB/section4/project/PART2_Modeling/model_rn.pkl','rb') as pickle_file:
    model_rn = pickle.load(pickle_file)

# 눈 예측
# 0 = 눈, 1 = 눈 없음
with open('/Users/yerin/AIB/section4/project/PART2_Modeling/model_sn.pkl','rb') as pickle_file:
    model_sn = pickle.load(pickle_file)
    
bp = Blueprint('weather', __name__, url_prefix='/')

@bp.route('/weather')
def hello_weather():
    return render_template('weather.html')

@bp.route('/weather/result', methods=['POST'])
def result():
    
    month = None
    day = None
    
    data = pd.DataFrame({'month':[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
        'day':[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
        'time':[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]})
    
    month = int(request.form.get("month"))
    day = int(request.form.get("day"))
    
    # 모델 예측을 위한 dataframe
    data['month'] = month
    data['day'] = day

    # 기온 예측
    pred_ta = model_ta.predict(data)
    
    # 기온 profiling
    morning = round( (sum(pred_ta[6:11]) / len(pred_ta[6:11])), 2)
    afternoon = round( (sum(pred_ta[11:17]) / len(pred_ta[11:17])), 2)
    evening = round( (sum(pred_ta[17:]) / len(pred_ta[17:])), 2)
    dawn = round( (sum(pred_ta[:5]) / len(pred_ta[:5])), 2)
    
    # 강수, 적설 예측을 위한 dataframe
    data['ta'] = pred_ta
    
    pred_rn = []
    pred_sn = []
    
    # 겨울이 아닐 경우 강수 예측, 겨울일 경우 적설 예측
    if (12 > month > 2):
        
        pred_rn = list(model_rn.predict(data))
        rn_mor = pred_rn[6:11]
        rn_aft = pred_rn[11:17]
        rn_eve = pred_rn[17:]
        rn_dawn = pred_rn[:5]
        
        if 0 in rn_mor:
            rn_mor = "오전에는 많은 비가 올 것으로 예상됩니다."
        elif 2 in rn_mor:
            rn_mor = "오전에는 비가 올 것으로 예상됩니다."
        else:
            rn_mor = "오전에는 비가 오지 않을 것으로 예상됩니다."
        
        if 0 in rn_aft:
            rn_aft = "오후에는 많은 비가 올 것으로 예상됩니다."
        elif 2 in rn_aft:
            rn_aft = "오후에는 비가 올 것으로 예상됩니다."
        else:
            rn_aft = "오후에는 비가 오지 않을 것으로 예상됩니다."
            
        if 0 in rn_eve:
            rn_eve = "저녁에는 많은 비가 올 것으로 예상됩니다."
        elif 2 in rn_eve:
            rn_eve = "저녁에는 비가 올 것으로 예상됩니다."
        else:
            rn_eve = "저녁에는 비가 오지 않을 것으로 예상됩니다."

        if 0 in rn_dawn:
            rn_dawn = "새벽에는 많은 비가 올 것으로 예상됩니다."
        elif 2 in rn_dawn:
            rn_dawn = "새벽에는 비가 올 것으로 예상됩니다."
        else:
            rn_dawn = "새벽에는 비가 오지 않을 것으로 예상됩니다."
        
        sn_mor = []
        sn_aft = []
        sn_eve = []
        sn_dawn = []
        pred_sn = []

    elif (month < 3) or (month > 11):
        
        pred_sn = model_sn.predict(data)
        sn_mor = pred_sn[6:11]
        sn_aft = pred_sn[11:17]
        sn_eve = pred_sn[17:]
        sn_dawn = pred_sn[:5]
        
        if 1 in sn_mor:
            sn_mor = "오전에는 눈이 올 것으로 예상됩니다."
        else:
            sn_mor = "오전에는 눈이 오지 않을 것으로 예상됩니다."
        
        if 1 in sn_aft:
            sn_aft = "오후에는 눈이 올 것으로 예상됩니다."
        else:
            sn_aft = "오후에는 눈이 오지 않을 것으로 예상됩니다."
            
        if 1 in sn_eve:
            sn_eve = "저녁에는 눈이 올 것으로 예상됩니다."
        else:
            sn_eve = "저녁에는 눈이 오지 않을 것으로 예상됩니다."

        if 1 in sn_dawn:
            sn_dawn = "새벽에는 눈이 올 것으로 예상됩니다."
        else:
            sn_dawn = "새벽에는 눈이 오지 않을 것으로 예상됩니다."
        
        rn_mor = []
        rn_aft = []
        rn_eve = []
        rn_dawn = []
        pred_rn = []
        
    else:
        return "error"

    return render_template('weather_result.html', month=month, day=day, 
                           morning=morning, afternoon=afternoon, evening=evening, dawn=dawn,
                           rn_mor=rn_mor, rn_aft=rn_aft, rn_eve=rn_eve, rn_dawn=rn_dawn,
                           sn_mor=sn_mor, sn_aft=sn_aft, sn_eve=sn_eve, sn_dawn=sn_dawn,
                           pred_rn=pred_rn, pred_sn=pred_sn)
    
