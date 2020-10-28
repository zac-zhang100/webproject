from flask import render_template,flash,redirect,url_for
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/base')
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

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data,form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html',title='Sign In',form=form)