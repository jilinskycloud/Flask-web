from flask import Flask
from flask import escape
from flask import url_for
from flask import request
from flask import render_template
from flask import abort
from flask import redirect
from flask import session

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
@app.route('/index/')
@app.route('/index')
def index():
	if 'username' in session:
		print("logedin")
		return redirect(url_for('dashboard'))
	return redirect(url_for('login'))

@app.route('/dashboard')
@app.route('/dashboard/')
def dashboard():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    else:
        return redirect(url_for('login'))

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

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['username'] = request.form['username']
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))




'''
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
'''