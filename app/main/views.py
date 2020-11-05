from flask import render_template,flash,redirect,url_for,request
from app import create_app
from . import main
from flask_login import current_user,login_user,login_required
from ..models import User

app = create_app()

@main.route('/')
def index():
    name = 'Zac Zhang'
    movies = [
        {'title': 'My Neighbor Toronto', 'year': '1998'},
        {'title': 'Dead	Poets	Society', 'year': '1989'},
        {'title': 'A	Perfect	World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail	Butterfly', 'year': '1996'},
        {'title': 'King	of	Comedy', 'year': '1999'},
        {'title': 'Devils	on	the	Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The	Pork	of	Music', 'year': '2012'},
    ]
    return render_template('base.html')

@main.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        name = request.form['name']

        if name:
            data = app.config['USER_COLLECTION'].find_one({'name':name})
            if data:
                user = User(id=data.get('_id'), username=data.get('name'), password=data.get('password'))
                hash = user.set_password(user.password)
                password = request.form['password']
                if user.validate_password(hash,password):
                    login_user(user)
                    return redirect(url_for('main.index'))
            else:
                return "Invalid password"
            flash("Cannot find username, please register.")
        flash("Empty Input.")
    return render_template('login.html')

@main.route('/enroll',methods=['GET','POST'])
def enroll():
    if request.method == 'POST':
        nickname = request.form.get('nickname')
        name = request.form.get('name')
        phone = request.form.get('phone')
        password = request.form.get('password')
        app.config['PLAYER_COLLECTION'].insert_one({"name":name,"nickname":nickname,"phone":phone,"password":password})
        image = request.form.get('img')
        app.config['IMAGE_COLLECTION'].insert_one(
            {"avatar": image})
        return redirect(url_for('main.index'))

    return render_template('enroll.html')

@main.route('/register',methods=['GET','POST'])
def register():
    return render_template('register.html')

@main.route('/rank',methods=['GET','POST'])
def rank():
    return render_template('rank.html')
