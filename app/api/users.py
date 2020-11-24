from app.api import bp
from flask import request,render_template,url_for,redirect
from app import create_app
from ..main import main
from ..models import Settings,Player,JSONEncoder
from bson.objectid import ObjectId
import json
import re

app = create_app()

@bp.route('/users/search_player',methods=['GET'])
def search_player():
        info = []
        playerName = request.args.get('playerName')
        list_data = Settings.get_extr_lst_exp(redisclient=app.config['REDIS'], mongodb=app.config['MONGO'], table="player", page=1, size=10, ttl=Settings.DEFAULT_TTL,  player="test1",is_all=False)
        for data in list_data:
            str = data['uid']
            uid = ObjectId(str)
            vote = data['exp']
            piece = app.config['PLAYER_INFO'].find_one({'_id':uid})
            name = piece['name']
            print(type(name))
            match = re.match(playerName,name)
            if match is not None:
                result = match.group()
                if result is not None:
                    obj = {
                        "name":name,
                        "vote":vote,
                        "uid":str
                    }
                    print('yes')
                    info.append(obj)
        dict = {
            "data":info
        }
        return dict


@bp.route('/users/vote',methods=['GET'])
def vote():
    str = request.args.get('uid')
    uid = ObjectId(str)
    # player_id = player['_id']
    # usr_id = json.dumps(player_id,cls=JSONEncoder)
    Settings.add_extr_uid_exp(redisclient=app.config['REDIS'],mongodb=app.config['MONGO'], table="player",key_name="test1",uid=uid,add_exp=1,is_set=False)

    #这里的意思是每次取得原来票数的值再加一，并更新
    # vote = request.args.get('vote')
    # app.config['PLAYER_COLLECTION'].update({"name":name},{"$set":{"vote":vote}})
    return "hello"


@bp.route('/users/player_information',methods=['GET'])
def player_information():
    name = request.args.get('playerName')
    info = app.config['PLAYER_COLLECTION'].find_one({"name":name})
    info['_id']=0
    list_data = list(app.config['PLAYER_COLLECTION'].find({}).sort([('vote', -1)]))
    for x in range(len(list_data)):
        if list_data[x]['name'] == name:
            rank = x+1

    json = {
    "info":info,
    "rank":rank
    }
    return json

@bp.route('/users/load_avatar',methods=['POST'])
def load_avatar():
    img = request.form.get('img')
    phone = request.form.get('phone')
    app.config['IMAGE_COLLECTION'].insert_one({"img": img,"phone":phone})
    return "success"


@bp.route('/users/showInfo')
def show():
    name = request.args.get('name')
    nickname = request.args.get('nickname')
    phone = request.args.get('phone')
    vote = request.args.get('vote')
    rank = request.args.get('rank')
    return render_template('information.html',name=name,nickname=nickname,phone=phone,vote=vote,rank=rank)