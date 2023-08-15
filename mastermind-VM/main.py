from flask import Flask, url_for, render_template, session, request, redirect

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
    return f'<p>{nickname}</p>'