from flask import render_template,flash,redirect,url_for

from . import main
from app.forms import LoginForm,set_password,check_password
from flask_login import current_user,login_user
from app import collection

@main.route('/')
@main.route('/base')
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
    return render_template('index.html', name=name, movies=movies)

@main.route('/login',methods=['GET','POST'])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user =  collection.find({},{"user":1,"password":0})
        if user is None :
                # or not check_password(form.password.data)
            flash("Invalid username or password")
            return redirect(url_for('login'))
            login_user(user,remember=form.remember_me.data)
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data,form.remember_me.data))
        # return redirect(url_for('index'))
    return render_template('login.html',title='Sign In',form=form)
