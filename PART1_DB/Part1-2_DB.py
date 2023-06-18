
# data를 정제해서 넣는 과정(15분 소요)

import json
import requests
import pymongo
from pymongo import MongoClient

# PyMongo
HOST = 'learn.v7lcdhw.mongodb.net'
USER = 'YerinRyu'
PASSWORD = 'ESoUNU8DFZFPIiMr'
DATABASE_NAME = 'project'
COLLECTION_NAME = 'weather_query'
    
URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"
client = MongoClient(URI)

db = client.db
db = client[DATABASE_NAME]

collection = db.collection
collection = db['weather']

for doc in collection.find():
    collection_insert = db.collection
    collenction_insert = db[COLLECTION_NAME]
    try:
        collection_insert.insert_many(doc['response']['body']['items']['item'])
        collection = db.collection
        collection = db['weather']
        
    except:
        try:
            if doc['response']['header']['resultCode'] == '03':
                print(doc['response']['header']['resultCode'])
                continue
        except:
            print(doc)
            collection_insert.insert_one(doc)
            collection = db.collection
            collection = db['weather']
            continue