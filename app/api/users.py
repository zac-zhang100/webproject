from app.api import bp
from flask import request

@bp.route('/users/<int:id>',methods=['GET'])
def get_user(id):
    pass

@bp.route('/users',methods=['GET'])
def get_users():
    pass

@bp.route('/image',methods=['POST'])
def create_user_image():
    return

@bp.route('/image/<int:id>',methods=['PUT'])
def update_user(id):
    pass