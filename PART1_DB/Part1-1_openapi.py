import json
import requests
import pymongo
from pymongo import MongoClient
import time
import datetime

print(f"시작 시각: {str(datetime.datetime.now())[11:19]}")

# API
KEY = "spCTlbTG%2BoD%2Fc8uHxMa95wySU%2Fa3B7FectEr9chW5mcAiZPyRJIo08Hz9MHX8kbV5T%2B6DdYZv8CizI8igs60qQ%3D%3D"

# PyMongo
HOST = 'learn.v7lcdhw.mongodb.net'
USER = 'YerinRyu'
PASSWORD = 'ESoUNU8DFZFPIiMr'
DATABASE_NAME = 'project'
COLLECTION_NAME = 'weather'
    
URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"
client = MongoClient(URI)
    
db = client.db
db = client[DATABASE_NAME]
collection = db.collection
collection = db[COLLECTION_NAME]

error_list = []
page_list = range(1, 367, 1)

def API(year, error_list=[], page_list=page_list):
    
    if error_list == []:
        print(f"_____{year} START_____")
    else:
        print(f"_____{year} RESTART_____")
        
    # GET
    for page in page_list:
        # time.sleep(1)
        try:
            page = page
            URL = f"http://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList?serviceKey={KEY}&numOfRows=24&pageNo={page}&dataType=JSON&&dataCd=ASOS&dateCd=HR&stnIds=108&endDt={year}1231&endHh=23&startHh=00&startDt={year}0101"
            
            # 1page부터 366page까지 차례로 데이터를 불러옵니다. page = day
            row_data = requests.get(URL)
            doc = json.loads(row_data.text)
            collection.insert_one(doc)
    
        except:
            # 오류가 날 경우 다운로드를 다시 진행합니다.
            print(f"오류 시각: {str(datetime.datetime.now())[11:19]}")
            print(f"error page:{page}")
            error_list.append(page)
            
            continue

    print(f"{year} END")
    print(f"완료 시각: {str(datetime.datetime.now())[11:19]}")
    print("error page:", error_list)
    
    return error_list


year = 2003

# 함수 실행
error_list = API(year, error_list=[], page_list=[65, 360])

print("=", error_list)

# error 실행
if error_list != None:
   API(year, error_list=error_list, page_list=error_list)