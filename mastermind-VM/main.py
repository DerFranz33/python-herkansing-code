from flask import Flask, url_for, render_template, session, request, redirect
from flask_sqlalchemy import SQLAlchemy
import re as regex
from datetime import timedelta
from datetime import datetime
from enum import Enum
from random import randrange


# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# make sure session is cleaned very soon (TODO just for testing purposes)
# app.permanent_session_lifetime = timedelta(seconds=20)
# set secret key which is needed for sqlalchemy to operate (TODO make it a difficult key)
app.secret_key = 'ali'

# initialize the app with the extension
db.init_app(app)

feedback_so_far = []



# ---------- CLASSES TODO remove here and put in a file called models.py -----------------------
# TODO check if need nullables TODO rename Players to player

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    score  = db.Column(db.Integer)
    amount_of_colours = db.Column(db.Integer)
    amount_of_positions = db.Column(db.Integer)
    doubles_allowed = db.Column(db.Boolean)
    cheat_modus = db.Column(db.Boolean)
#     # R -> speler
    players_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=True)
#     # A -> status
    is_won = db.Column(db.Boolean, nullable=True)

    def __str__(self):
        return "Game_id: {game_id}, start_time: {start_time}".format(game_id=self.id, start_time=self.start_time)


class Players(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), unique=True)
    Game = db.relationship('Game', backref='players', lazy=True)


class Pin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    players_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=True)
    colour = db.Column(db.String(20)) # TODO als lukt maak enum van
    position = db.Column(db.Integer)

    
class Colour(Enum):
    RED = 1
    BLUE = 2
    GREEN = 3
    YELLOW = 4
    ORANGE = 5
    BROWN = 6
    TURQUOISE = 7
    PURPLE = 8
    PINK = 9
    OLIVE = 10
    BLACK = 11
    WHITE = 12





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
            
            # TODO POST in db nowhere else
            if(request.method == 'POST'):
                _number_of_colours = request.form['number_of_colours']
                _number_of_positions = request.form['number_of_positions']
                _doubles_allowed = request.form['doubles_allowed']
                _cheat_modus = request.form['cheat_modus']

                feedback_so_far = []

                
                


                game_id = __generate_game(positions_length=_number_of_positions,
                                amount_of_colours=_number_of_colours,
                                can_be_double=_doubles_allowed,
                                cheat_modus=_cheat_modus,
                                players_name=session['nickname'])


                
                return redirect(url_for('game_session', game_id=game_id))
            else:
                return render_template('game.html', nickname=nickname)
    else:
        return redirect(url_for('home'))
    








# TODO refactor: only use game_id and get rest of values out of db
@app.route('/game/<game_id>', methods=['POST', 'GET'])
def game_session(game_id):
    

    if __nickname_okay():
        nickname = session['nickname']





    game = db.session.execute(db.select(Game).filter_by(id=game_id)).scalar_one_or_none()






    number_of_colours = game.amount_of_colours
    number_of_positions = game.amount_of_positions
    doubles_allowed = game.doubles_allowed
    cheat_modus = game.cheat_modus
    answer = __get_answer(game_id)
    # al_guesses = __get_player_guesses(game_id, number_of_positions)


    # if(doubles_allowed == 'true' or doubles_allowed == 'True'):
    #     doubles_allowed = True
    # elif(doubles_allowed == 'false' or doubles_allowed == 'False'):
    #     doubles_allowed = False

    # TODO this needs to be in Game route
    # __generate_game(amount_of_colours=number_of_colours, positions_length=number_of_positions, can_be_double=doubles_allowed, cheat_modus=cheat_modus, players_name=session['nickname'])

    if(request.method == 'POST'):
        # al_guesses = []
        guess = []
        counter = 1
        while counter <= number_of_positions:
            guess.append(request.form['guess_position_{}'.format(counter)])
            temp_pin = Pin()
            temp_pin.colour = request.form['guess_position_{}'.format(counter)]
            temp_pin.position = counter
            player_id = db.session.execute(db.select(Players).filter_by(nickname=session['nickname'])).scalar_one().id
            temp_pin.players_id = player_id
            temp_pin.game_id = game_id
            db.session.add(temp_pin)
            db.session.commit()
            counter += 1
        # al_guesses = __get_player_guesses(game_id, number_of_positions)
        all_user_pins = db.session.execute(db.select(Pin).filter_by(game_id=game_id, players_id=player_id)).scalars().all()
        amount_of_guesses = int(len(all_user_pins)/number_of_positions)
        # TODO store in db get current game_id -> game.end_time = current time
        # TODO game.score = game.score +1

        if (__is_game_won(answer, guess)):
                    print('TODO yeah game won!!!!')
        else:
            feedback = __give_feedback(game_id, guess)
            return render_template('game-session.html', nickname=nickname,
                    number_of_colours=number_of_colours,
                    number_of_positions=number_of_positions,
                    doubles_allowed=doubles_allowed,
                    cheat_modus=cheat_modus,
                    answer = answer,
                    amount_of_guesses=amount_of_guesses,
                    all_user_pins=all_user_pins,
                    feedback=feedback
                    )


        return render_template('game-session.html', nickname=nickname,
                        number_of_colours=number_of_colours,
                        number_of_positions=number_of_positions,
                        doubles_allowed=doubles_allowed,
                        cheat_modus=cheat_modus,
                        answer = answer,
                        amount_of_guesses=amount_of_guesses,
                        all_user_pins=all_user_pins
                        )
        

        
    
    return render_template('game-session.html', nickname=nickname,
                            number_of_colours=number_of_colours,
                            number_of_positions=number_of_positions,
                            doubles_allowed=doubles_allowed,
                            cheat_modus=cheat_modus,
                            answer = answer
                            )
    









@app.route('/reset_nickname')
def reset_nickname():
    session.pop('nickname', None)
    return redirect(url_for('home'))














@app.route('/statistics/', methods=['POST', 'GET'])
def statistics():
    if __nickname_okay():
        player_id = db.session.execute(db.select(Players).filter_by(nickname=session['nickname'])).scalar_one_or_none().id
        player_games = db.session.execute(db.select(Game).filter_by(players_id=player_id)).scalars().all()

        if(request.method == 'POST'):
            pass






        return render_template('statistics.html', nickname=session['nickname'], player_games=player_games)
    return redirect(url_for('home'))



















# --------------- HELPERS AND LOGIC -----------------------


def __nickname_okay():
    if 'nickname' in session:
        if regex.search('[a-zA-Z]', session['nickname']) != None:
            return True
    return False


def __generate_game(positions_length, amount_of_colours, can_be_double, cheat_modus, players_name):

    positions_length = int(positions_length)
    amount_of_colours = int(amount_of_colours)
    # TODO lelijke code hierbeneden
    if(can_be_double == 'true' or can_be_double == 'True'):
        can_be_double = True
    elif(can_be_double == 'false' or can_be_double == 'False'):
        can_be_double = False
    if(cheat_modus == 'true' or cheat_modus == 'True'):
        cheat_modus = True
    elif(cheat_modus == 'false' or cheat_modus == 'False'):
        cheat_modus = False

    print('') # TODO remove
    
    player = db.session.execute(db.select(Players).filter_by(nickname=players_name)).scalar_one()
    players_id = player.id

    temp_game = Game()
    temp_game.start_time = datetime.now()
    temp_game.score = 0
    temp_game.amount_of_colours = amount_of_colours
    temp_game.amount_of_positions = positions_length
    temp_game.players_id = players_id
    # temp_game.status = 'active' TODO remove
    temp_game.cheat_modus = cheat_modus
    db.session.add(temp_game)
    db.session.commit()

    games = db.session.execute(db.select(Game)).scalars().all() # TODO use __str__ here somewhere or something
    for game in games:
        print('game_id: {}, start_time: {}, score: {}, players_id: {}, colours: {}, positions: {}, cheat_modus: {}, is_won: {}'
              .format(game.id, game.start_time, game.score, game.players_id, game.amount_of_colours,
                       game.amount_of_positions, game.cheat_modus, game.is_won))


    end_range_colours = amount_of_colours + 1
    if(can_be_double):
        counter = 1
        while counter <= positions_length:
            temp_pin = Pin()
            temp_pin.colour = randrange(1,end_range_colours)
            temp_pin.position = counter
            temp_pin.game_id = temp_game.id
            db.session.add(temp_pin)
            db.session.commit()
            counter += 1
    else:
        temp_colours = []
        counter = 1
        while(counter <= positions_length):
            colour = randrange(1,end_range_colours)
            if(colour not in temp_colours):
                temp_colours.append(colour)
                temp_pin = Pin()
                temp_pin.colour = randrange(1,end_range_colours)
                temp_pin.position = counter
                temp_pin.game_id = temp_game.id
                db.session.add(temp_pin)
                db.session.commit()
                counter += 1
     

    pins = db.session.execute(db.select(Pin)).scalars().all()
    for pin in pins:
        print('pin_id: {}, colour: {}, position: {}, game_id: {}'.format(pin.id, pin.colour, pin.position, pin.game_id))

    return temp_game.id


def __get_answer(game_id):

    all_pins = db.session.execute(db.select(Pin).filter_by(game_id=game_id)).scalars().all()
    game = db.session.execute(db.select(Game).filter_by(id=game_id)).scalar_one_or_none()
    amount_of_positions = game.amount_of_positions

    answer_pins = []
    counter = 0
    while counter < amount_of_positions:
        answer_pins.append(all_pins[counter])
        counter += 1
    return answer_pins


def __is_game_won(pin_answer, pin_guess):
        counter = 0
        while counter < len(pin_answer):
           a = pin_answer[counter].colour
           b = pin_guess[counter]
           if (pin_answer[counter].colour != pin_guess[counter]):
               return False
           counter += 1
        return True


feedback_so_far = [] # TODO refactor if you can
def __give_feedback(game_id, guess): # TODO instead of guess use all_user_pins
    feedback = []
    answer = __get_answer(game_id=game_id)

    counter = 0
    while counter < len(guess):
        if(answer[counter].colour == guess[counter]):
            feedback.append(11) # TODO needs to be enum
            counter += 1
        else:
            temp_list = [pin for pin in answer if pin.colour == guess[counter]] # TODO check if this is a good enough comprehension
            if(len(temp_list) > 0):
                feedback.append(12) # TODO needs to be enum
                counter += 1
            else:
                feedback.append('')# TODO ugly?
                counter += 1
            
    feedback_so_far.append(feedback)
    return feedback_so_far # TODO probably not necessary








# def __get_player_guesses(game_id, amount_of_positions):
#     all_pins = db.session.execute(db.select(Pin).filter_by(game_id=game_id)).scalars().all()
    
    

#     all_guesses = []

#     pins_guessed = len(all_pins) - amount_of_positions
    
#     outer_counter = 1

#     while outer_counter < (pins_guessed/amount_of_positions):
#         temp_guess_pins = []
#         inner_counter = 0
#         while inner_counter < amount_of_positions: 
#             temp_guess_pins.append(all_pins[inner_counter + (amount_of_positions*outer_counter)])
#             inner_counter += 1
#         all_guesses.append(temp_guess_pins)
#         outer_counter += 1


#     return all_guesses
# -------------------- ENDHELPERS --------------------------