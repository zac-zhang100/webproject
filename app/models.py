from flask_login import UserMixin
from . import login_manager,create_app
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime,timedelta
import json
from bson import json_util,ObjectId


app = create_app()

class User(UserMixin):
    is_active = True
    is_anonymous = False
    is_authenticated = True

    def __init__(self,id,username,password):
        self.id = str(id)
        self.name = username
        self.password = password

    def set_password(self, password):
        return generate_password_hash(password)

    def validate_password(self, password_hash,password):
        return check_password_hash(password_hash, password)

# 回调函数必须注册，用于验证id是否为该用户，帮助login_manager验证用户状态
# 这个函数装饰器不是类成员，但是只有在main.views中import User才不会报错：Exception: Missing user_loader or request_loader.
@login_manager.user_loader
def load_user(user_id):
    user = app.config['USER_COLLECTION'].find_one({'_id':ObjectId(user_id)})
    return User(id=user.get('_id'),username=user.get('name'),password=user.get('password'))

class Player:
    def __init__(self,name,nickname,id,phone,vote,rank,image):
        self.name = name
        self.nickname = nickname
        self.id = id
        self.phone = phone
        self.vote = vote
        self.rank = rank
        self.image = image

    def parse_json(data):
        return json.loads(json_util.dumps(data))

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o,ObjectId):
            return str(o)
        return json.JSONEncoder.default(self,o)

class Settings:

    DEFAULT_TTL = 60 * 60 * 24 * 40
    DAY_TTL = 60 * 60 * 24 * 1
    TWO_DAY_TTL = 60 * 60 * 24 * 2
    HOUR_TTL = 60 * 60 * 1
    TWO_HOUR_TTL = 60 * 60 * 2

    # 选手的总积分
    extr_all_exp = "all_exp"
    """ uid:uid,exp:积分 """

    # 选手每天的积分
    extr_day_exp = "day_exp"
    """ uid:uid,day:日期,exp:积分 """

    # 选手每月的积分
    extr_month_exp = "month_exp"
    """ uid:uid,month:月,exp:积分 """

    # 选手每小时的积分
    extr_hour_exp = "hour_exp"
    """ uid:uid,hour:日期,exp:积分 """

    # 选手总积分排名zset序：<key uid,score 积分榜>
    @classmethod
    def get_extr_all_exp_key(cls,name):
        return "%s_%s_zset" % (name,Settings.extr_all_exp)

    # 清空选手总积分排名
    @classmethod
    def get_extr_all_exp_key_empty(cls,name):
        return "%s_%s_empty" % (name, Settings.extr_all_exp)

    # 选手每日积分排名zset序：<key uid,score 积分榜>
    @classmethod
    def get_extr_day_exp_key(cls,name,day):
        return "%s_%s_zset_%s" % (name, Settings.extr_day_exp,day)

    # 清空选手每日积分排名
    @classmethod
    def get_extr_day_exp_key_empty(cls,name,day):
        return "%s_%s_empty_%s" % (name, Settings.extr_day_exp,day)

    # 选手每月积分排名zset序：<key uid,score 积分榜>
    @classmethod
    def get_extr_month_exp_key(cls,name,month):
        return "%s_%s_zset_$s" % (name,Settings.extr_month_exp,month)

    # 清空选手每月积分排名
    @classmethod
    def get_extr_month_exp_key_empty(cls,name,month):
        return "%s_%s_zset_%s" % (name,Settings.extr_month_exp,month)

    # 选手每时积分排名zset序：<key uid,score 积分榜>
    @classmethod
    def get_extr_hour_exp_key(cls,name,hour):
        return "%s_%s_zset_%s" % (name,Settings.extr_hour_exp,hour)

    # 清空选手每时积分排名
    @classmethod
    def get_extr_hour_exp_key_empty(cls,name,hour):
        return "%s_%s_zset_%s" % (name, Settings.extr_hour_exp,hour)

    @classmethod
    def getDay(cls,days=0,f="%Y-%m-%d",currTime=None):
        if currTime is None:
            currTime = datetime.now()
        day = currTime + timedelta(days)
        return day.strftime(f)

    @classmethod
    def getMonth(cls,days=0):
        currTime = datetime.now()
        day = currTime + timedelta(days)
        return day.strftime("%Y-%m")

    @classmethod
    def getHour(cls,days=0):
        currTime = datetime.now()
        day = currTime + timedelta(days)
        return day.strftime("%Y-%m-%d %H")

    @classmethod
    def get_extr_exp(cls,mongodb,table):
        retData = []
        if mongodb is None:
            return retData
        res = mongodb[table].find()
        for eachRes in res:
            uid = eachRes.get("_id",0)
            vote = eachRes.get("vote",0)
            retData.append({"uid":uid,"vote":vote})
        return retData

    @classmethod
    def load_extr_exp(cls,redisclient,mongodb,table,key,keyepy,ttl):
        if redisclient.exists(key) or redisclient.exists(keyepy):
            return
        dbData = Settings.get_extr_exp(mongodb,table)
        if len(dbData) > 0:
            for eachData in dbData:
                usruid = eachData.get("uid",0)
                vote = eachData.get("vote",0)
                redisclient.zadd(key,vote,usruid)
            redisclient.expire(key,ttl)
        else:
            redisclient.setex(keyepy,ttl,"")

    @classmethod
    def add_extr_exp(cls,mongodb,table,uid,add_exp,is_set):
        if mongodb is None:
            return None
        query = {}
        query["_id"] = uid
        u_data = {}
        u_data["vote"] = add_exp
        if not is_set:
            res = mongodb[table].find_and_modify(query,{"$inc":u_data},upsert=True,new=True)
        else:
            res = mongodb[table].find_and_modify(query,{"$set":u_data},upsert=True,new=True)

        if res:
            return res.get("exp",None)
        else:
            return res

    @classmethod
    def get_extr_lst_exp(cls,redisclient,mongodb,table,page=1,size=10,ttl=DEFAULT_TTL,player=None,is_all=False):
        retData = []
        if None in (redisclient,mongodb):
            return retData
        key = "%s_%s" % (player,"zset")
        keyepy = "redis_empty_%s" % (player)

        Settings.load_extr_exp(redisclient,mongodb,table,key,keyepy,ttl)

        if redisclient.exists(key):
            if is_all:
                tops = redisclient.zrevrange(key, 0, -1, withscores=True)
            else:
                start = (page - 1) * size
                tops = redisclient.zrevrange(key, start, start + size - 1, withscores=True)
            for usr in tops:
                usr_uid = usr[0]
                exp = usr[1]
                retData.append({'exp': int(exp),'uid':usr_uid})


        return retData

    @classmethod
    def add_extr_uid_exp(cls,redisclient,mongodb,table,key_name,uid,add_exp,is_set=False):
        retData = 0

        if None in (redisclient,mongodb):
            return retData

        key = "%s_%s" % (key_name, "zset")
        keyepy = "redis_empty_%s" % (key_name)

        res = Settings.add_extr_exp(mongodb,table,uid,add_exp,is_set)
        if res is not None:
            uid = str(uid)
            if redisclient.exists(key):
                redisclient.zadd(key,res,uid)
            elif redisclient.exists(keyepy):
                redisclient.delete(keyepy)
        return res









