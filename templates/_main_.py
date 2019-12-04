from flask import Flask
from flask import escape
from flask import url_for
from flask import request
from flask import render_template
from flask import abort
from flask import redirect

app = Flask(__name__)

@app.route('/')
def index_page():
    return redirect(url_for('login'))

@app.route('/dashboard')
def hello_world1():
    return 'Hello, World!'

@app.route('/configuration/')
@app.route('/configuration/<name>')
def hello_world2(name=None):
    return render_template('index.html',name=name)

@app.route('/contact_us/<username>')
def hello_world3(username):
    return 'User %s' % escape(username)

@app.route('/check_id/<int:id>')
def id_fnc(id):
    return 'User %s' % escape(id)

@app.route('/projects/')
def projects():
    return 'The project page'




@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)