from app.api import bp
from flask import request,render_template
from app import create_app


app = create_app()

@bp.route('/users/search_player',methods=['GET'])
def search_player():
        playerName = request.args.get('playerName')
        list_data = list(app.config['PLAYER_COLLECTION'].find({'name': {"$regex":playerName}}).sort([('vote',-1)]))
        for x in range(len(list_data)):
            list_data[x]['_id']=0
        dict = {
            "data":list_data
        }
        return dict


@bp.route('/users/player_information',methods=['GET'])
def player_information():
    Name = request.args.get('playerName')
    vote = request.args.get('vote')
    app.config['PLAYER_COLLECTION'].update({"name":Name},{"$set":{"vote":vote}})
    return "hello"


@bp.route('/image',methods=['POST'])
def create_user_image():
    return

@bp.route('/image/<int:id>',methods=['PUT'])
def update_user(id):
    pass