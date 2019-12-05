from flask import Flask
from flask import escape
from flask import url_for
from flask import request
from flask import render_template
from flask import abort
from flask import redirect
from flask import session
from flask import flash
#import paho.mqtt.client as Mqtt
from flask_mqtt import Mqtt
from flask_mysqldb import MySQL

app = Flask(__name__)


app.config['MQTT_BROKER_URL'] = 'localhost'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds
mqtt = Mqtt(app)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('t1')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode(),
    )
    print(data)


# MYSQL CONNECTION
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'FlaskDb'

mysql = MySQL(app)
# Create the DataBase
@app.route('/DB')
def DB():
    u_name = 'admin'
    u_password = 'pass'
    cur = mysql.connection.cursor()
    #cur.execute("CREATE DATABASE FlaskDb")
    #cur.execute("CREATE TABLE MyUsers(firstName VARCHAR(30), lastName VARCHAR(30))")      
    cur.execute("INSERT INTO MyUsers(firstName, lastName) VALUES (%s, %s)", (u_name, u_password))
    mysql.connection.commit()
    cur.close()
    return 'success'



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
        u_name = escape(session['username'])
        return render_template('dashboard.html', name = u_name)
        #return 'Logged in as %s' % escape(session['username'])
    else:
        return redirect(url_for('login'))


@app.route('/devices')
def devices():
    return render_template('devices.html')


@app.route('/mqtt-console')
def mqtt_on():
    return render_template('mqtt-console.html')

@app.route('/http-console')
def http_con():
    return render_template('http-console.html') 






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

# HTTPLIB2 Message 
@app.route('/http_data', methods=['GET', 'POST'])
def http_data():
    if request.method == 'POST':
        u_msg = request.form['username']
    else:
        print("HTTP Msg Not Received..!")




# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        u_name = request.form['username']
        u_pass = request.form['password']
        flag =  verify(u_name, u_pass)
        #print(flag)
        #if request.form['username'] != 'admin' or request.form['password'] != 'admin':
        if(flag == -1):
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


def verify(u_name, u_pass):
    cur = mysql.connection.cursor()
    print(u_name)
    print(u_pass)
    #cur.execute("SELECT firstName, lastName FROM MyUsers")
    #myresult = cur.fetchall()
    #print("-----------------------------")
    #for x in myresult:
    #    print(x)

    #print("-----------------------------")
    #print(cur.execute("SELECT * FROM MyUsers WHERE firstName='admin' and lastName='pass'"))
    if(cur.execute("SELECT * FROM MyUsers WHERE firstName=%s and lastName=%s", (u_name, u_pass)) < 1):
        cur.close()
        return -1
    else:
        myresult = cur.fetchone()
        print(myresult)
        cur.close()
        return 0

