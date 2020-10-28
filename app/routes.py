from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
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