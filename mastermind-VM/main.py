from flask import Flask, url_for, render_template, session, request, redirect
from flask_sqlalchemy import SQLAlchemy
import re as regex
from datetime import timedelta


# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# make sure session is cleaned very soon (TODO just for testing purposes)
app.permanent_session_lifetime = timedelta(seconds=20)
# set secret key which is needed for sqlalchemy to operate (TODO make it a difficult key)
app.secret_key = 'ali'

# initialize the app with the extension
db.init_app(app)

class Players(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), unique=True)

with app.app_context():
    db.create_all()



@app.route('/', methods=['POST', 'GET'])
def home():
    if(request.method == 'POST'):
        nickname =  request.form['nickname']
        session['nickname'] = nickname
        # Add player
        temp_player = Players()
        temp_player.nickname = nickname
        db.session.add(temp_player)
        db.session.commit()


        # ------------- TODO just testing purposes --------------
        _player = db.one_or_404(db.select(Players).filter_by(nickname=session['nickname']))
        # -------------------------------------------------------
        return render_template('game.html', player=_player.nickname)

        return redirect(url_for('game'))
    else:
        # if('nickname' in session):
            # return redirect(url_for('game'))
        # else:
            return render_template('index.html')
    
@app.route('/game/')
def game():
    if('nickname' in session):
        nickname = session['nickname']
        if(regex.search('[a-zA-Z]', nickname) == None):
            return redirect(url_for('home'))
        else:
            return render_template('game.html', nickname=nickname)
    else:
        return redirect(url_for('home'))
    
@app.route('/reset_nickname')
def reset_nickname():
    session.pop('nickname', None)
    return redirect(url_for('home'))

@app.route('/statistics')
def statistics():
    if __nickname_okay():
        return render_template('statistics.html', nickname=session['nickname'])
    return redirect(url_for('home'))

def __nickname_okay():
    if 'nickname' in session:
        if regex.search('[a-zA-Z]', session['nickname']) != None:
            return True
    return False
