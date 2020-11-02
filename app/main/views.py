from flask import render_template,flash,redirect,url_for,request
from app import create_app
from . import main
from app.forms import LoginForm,set_password,check_password
from flask_login import current_user,login_user
from flask_pymongo import PyMongo

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
    return render_template('base.html', name=name, movies=movies)

@main.route('/login',methods=['GET','POST'])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))

    # app.config["MONGO_URI"] = "mongodb://localhost:27017/test"
    # mongo = PyMongo(app)
    form = LoginForm()
    if form.validate_on_submit():
        user = app.config['USER_COLLECTION'].find_one({"name":form.username.data})
        if user:
            check = app.config['USER_COLLECTION'].find_one({"name": form.username.data, "password": form.password.data})
            if check:
                flash('Login requested for user {}, remember_me={}'.format(
                    form.username.data, form.remember_me.data))
                return redirect(url_for('main.base'))
            else:
                flash('Invalid password')
                return "Invalid password"

        flash("Cannot find username, please register.")

    return render_template('login.html', title='Sign In', form=form)

@main.route('/enroll',methods=['GET','POST'])
def enroll():
    if request.method == 'POST':
        nickname = request.form.get('nickname')
        name = request.form.get('name')
        phone = request.form.get('phone')
        password = request.form.get('password')
        app.config['PLAYER_COLLECTION'].insert_one({"name":name,"nickname":nickname,"phone":phone,"password":password})
        return redirect(url_for('main.base'))

    return render_template('enroll.html')
