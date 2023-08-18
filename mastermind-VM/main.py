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



# ---------- CLASSES TODO remove here and put in a file called models.py -----------------------
# TODO check if need nullables TODO rename Players to player
class Players(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), unique=True)

# class Game(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     start_time = db.Column(db.DateTime)
#     end_time = db.Column(db.DateTime)
#     score  = db.Column(db.Integer)
#     # R -> speler
#     # A -> antwoord type=list
#     # R -> gok
#     # A -> status
#     pass

#--------------- ENDCLASSES ----------------------------------------------------------------------

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

        if (db.session.execute(db.select(Players).filter_by(nickname=temp_player.nickname)).scalar_one_or_none() == None):
            db.session.add(temp_player)
            db.session.commit()

        # ------------- TODO just testing purposes --------------
        # _player = db.one_or_404(db.select(Players).filter_by(nickname='Henk'))
        # return render_template('game.html', player=_player.nickname)
        # -------------------------------------------------------

        return redirect(url_for('game'))
    else:
        if('nickname' in session):
            return redirect(url_for('game'))
        else:

            # nicknames = ('test1', 'test2', 'test3')
            _players = db.session.execute(db.select(Players)).scalars().all()
            _nickames = []
            for player in _players:
                _nickames.append(player.nickname)

            return render_template('index.html', nicknames=_nickames)
    
@app.route('/game/', methods=['POST', 'GET'])
def game():
    if('nickname' in session):
        nickname = session['nickname']
        if(regex.search('[a-zA-Z]', nickname) == None):
            return redirect(url_for('home'))
        else:
            
            if(request.method == 'POST'):
            # TODO hardcoded remove later
                _number_of_colours = int(request.form['number_of_colours'])
                _number_of_positions = int(request.form['number_of_positions'])
                _doubles_allowed = request.form['doubles_allowed']
                _cheat_modus = request.form['cheat_modus']
                # _number_of_colours = 8
                # _number_of_positions = 4
                # _doubles_allowed = True
                # _cheat_modus = False
                game_data = {'number_of_colours':_number_of_colours, 'number_of_positions':_number_of_positions, 'doubles_allowed':_doubles_allowed, 'cheat_modus':_cheat_modus}
                return render_template('game-session.html', nickname=nickname, game_data=game_data)
            else:
                return render_template('game.html', nickname=nickname)
    else:
        return redirect(url_for('home'))
    
@app.route('/game/<game_id>', methods=['POST', 'GET'])
def game_session():
    pass
    
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
