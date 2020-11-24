import os
from pymongo import MongoClient
from redis import StrictRedis

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DB = MongoClient()['test']
    REDIS = StrictRedis(host="localhost",port=6379,db=0,decode_responses=True,charset='UTF-8',encoding='UTF-8')
    USER_COLLECTION = DB.user
    PLAYER_COLLECTION = DB.player
    PLAYER_INFO = DB.player_info
    IMAGE_COLLECTION = DB.image
    MONGO = {
        "player":DB.player
    }

