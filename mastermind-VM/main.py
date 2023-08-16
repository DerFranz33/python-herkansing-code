from flask import Flask, url_for, render_template, session, request, redirect
from flask_sqlalchemy import SQLAlchemy
import re as regex


# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

app.secret_key = 'ali'

# initialize the app with the extension
db.init_app(app)

class Players(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), unique=True)

with app.app_context():
    db.create_all()

# from flask import Flask, url_for, render_template, session, request, redirect
# from flask_sqlalchemy import SQLAlchemy
# import re as regex

# db = SQLAlchemy()
# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
# db.init_app(app)

# with app.app_context():
#         db.create_all()



# class Players(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
    # nickname = db.Column(db.String(100), unique=True)






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
        return redirect(url_for('game'))
    else:
        if('nickname' in session):
            return redirect(url_for('game'))
        else:
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
    
# @app.route('/reset_nickname')
# def reset_nickname():
#     session.pop('nickname', None)
#     return redirect(url_for('home'))

# @app.route('/statistics')
# def statistics():
#     if __nickname_okay():
#         return render_template('statistics.html', nickname=session['nickname'], values=players.query.all())
#     return redirect(url_for('home'))

# def __nickname_okay():
#     if 'nickname' in session:
#         if regex.search('[a-zA-Z]', session['nickname']) != None:
#             return True
#     return False


# if __name__ == '__main__':
    
#     app.run()