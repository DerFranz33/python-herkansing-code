from flask import Flask, url_for, render_template, session, request, redirect
import re as regex

app = Flask(__name__)

app.secret_key = 'VeryHard@ToGuess666SecretKey#'

@app.route('/', methods=['POST', 'GET'])
def home():
    if(request.method == 'POST'):
        nickname =  request.form['nickname']
        session['nickname'] = nickname
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
            return f'<p>{nickname}</p>'
    else:
        return redirect(url_for('home'))