from flask_login import UserMixin
from . import login_manager,create_app
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash,check_password_hash

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