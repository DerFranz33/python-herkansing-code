from flask import Flask, url_for, render_template, session, request, redirect

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
    # nickname = request.form['nickname_form']
    # session['nickname'] = nickname
    if(request.method == 'POST'):
        nickname =  request.form['nickname']
        return redirect(url_for('game', nick_name=nickname))
    else:
        return render_template('index.html')
    
@app.route('/game/<nick_name>')
def game(nick_name):
    return f'<p>{nick_name}</p>'