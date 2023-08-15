from flask import Flask, url_for, render_template, session, request

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
    # nickname = request.form['nickname_form']
    # session['nickname'] = nickname
    return render_template('index.html')