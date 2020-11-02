import os
from pymongo import MongoClient

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DB = MongoClient()['test']
    USER_COLLECTION = DB.user
    PLAYER_COLLECTION = DB.player

