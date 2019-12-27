#!/usr/bin/python3
from flask import Flask
from flask import escape
from flask import url_for
from flask import request
from flask import render_template
#from flask import abort
from flask import redirect
from flask import session
#from flask import flash
from flask import jsonify
from flask_mqtt import Mqtt
from flask_mysqldb import MySQL
import psutil
import time
#import redis
#from flask_redis import FlaskRedis
import pymongo
from pymongo import MongoClient
from OpenSSL import SSL
import pprint
# self made
from _include.heartbeat import MQTT_ as _mqtt
from _include.heartbeat import HTTP_ as _http
from _include.dbClasses import mysqldb as _mysql
from _include.dbClasses import mongodb as _mongodb
from _include.dbClasses import redisdb as _redis

import json
#import os

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
db    = _mongodb.initMongo_(MongoClient, pymongo)
mysql = _mysql.initMysql_(MySQL, app)
# ===================MQTT FUNCTIONS===========================
_mqtt.connect_(Mqtt, app, _redis)
# ===================OPENSSL FUNCTIONS========================
#context = SSL.Context(SSL.PROTOCOL_TLSv1_2)
#context.use_privatekey_file('server.key')
#context.use_certificate_file('server.crt')

# =================MONGO-DB FUNCTIONS=========================
@app.route('/creat_model')                      # Create Model
def insert_():
	return 'as'

@app.route('/show_dat')                         # Get data query
def show_():
	_mongodb.show_(db)
	return 'as'

@app.route('/del_db/<db_name>')                 # Del DB
def delDB_(db_name):
	_mongodb.delDB_(db_name, MongoClient)
	return 'as'

@app.route('/del_coll/<coll_name>')             # Del Collection
def delColl_(coll_name):
	_mongodb.delColl_(coll_name, db)
	return redirect(url_for('showColl_'))

@app.route('/showColl_/<collname>')                       # Show Collection
@app.route('/showColl_',methods = ['POST', 'GET'])                       # Show Collection
def showColl_(collname=None):
    if request.method == 'POST':
        data = [];
        data.append(request.form['coll_name'])
        data.append(request.form['dev_id'])
        data.append(request.form['dev_ip'])
        data.append(request.form['dev_mac'])
        data.append(request.form['dev_rssi'])
        data.append(request.form['dev_ext'])
        data.append(request.form['dev_b'])
        data.append(request.form['dev_c'])
        print(data[0])
        _mongodb.insert_(MongoClient, pymongo, data)
    collections = _mongodb.showColl_(db)
    print(collections)
    return render_template("mongoColl.html", collections=collections)

@app.route('/del_rec/<_id>/<collname>/')
def delRec_(collname=None, _id=None):
    print(collname)
    print(_id)
    print("------------cursor testing---------------")
    collections = _mongodb.delRec_(collname, db, _id)
    return redirect(url_for('mongoRec',collname=collname ))

@app.route('/mongoRec/<collname>')                       # Show Collection
def mongoRec(collname):
    print(collname)
    rec = _mongodb.showRec_(collname, db)
    print("------------cursor testing---------------")
    return render_template("mongoRec.html", coll=rec, collname=collname)




# ===================HTTPLIB2 FUNCTIONS==========================
@app.route('/http_data/<username>') #, methods=['GET', 'POST'])
def http_data(username):
    if(username):
        http_data =  'User %s' % escape(username)
        print(http_data)
        _http.connect_(http_data, app, _redis)
        return 'success'
    return 'No success'




# ===================MYSQL FUNCTIONS==========================
@app.route('/createModel')
def createModel():
	_mysql.createModel_(MySQL, app)
	return 'success'

@app.route('/delProfile/<ids>')
def delProfile(ids=None):
    _mysql.delProfile_(mysql, ids)
    print("deleted..")
    return redirect(url_for('editProfile'))



# ===================HBEAT FUNCTIONS==========================
@app.route('/beat/')
def beat():
	return render_template("index.html")


#=============================================================
#=====================WEB-PAGE FUNCTIONS======================
#=============================================================

# ============================================================INDEX
@app.route('/')
@app.route('/index/')
@app.route('/index')
def index():
	if 'username' in session:
		print("logedin")
		return redirect(url_for('dashboard'))
	return redirect(url_for('login'))

# ============================================================DASHBOARD
@app.route('/dashboard')
@app.route('/dashboard/')
def dashboard():
    if 'username' in session:
        u_name = escape(session['username'])
        print(session.get('device1'))
        print("----------------------------------------------------------------")
        #while(1):
        cpu = psutil.cpu_percent()
        stats = psutil.cpu_stats()
        cpu_freq = psutil.cpu_freq()
        cpu_load = psutil.getloadavg()
        ttl_memo = psutil.virtual_memory()
        swp_memo = psutil.swap_memory()
        mount = psutil.disk_partitions(all=False)
        disk_io_count = psutil.disk_io_counters(perdisk=False, nowrap=True)
        net_io_count = psutil.net_io_counters(pernic=False, nowrap=True)
        nic_addr = psutil.net_if_addrs()
        tmp = psutil.sensors_temperatures(fahrenheit=False)
        boot_time = psutil.boot_time()
        c_user = psutil.users()
        #return render_template('dashboard.html',cpu=cpu)
        return render_template('dashboard.html', reload = time.time(), cpu = cpu, stats=stats, cpu_freq=cpu_freq, cpu_load=cpu_load, ttl_memo=ttl_memo, swp_memo=swp_memo, nic_addr=nic_addr, boot_time=boot_time, tmp=tmp, c_user=c_user)
        #return 'Logged in as %s' % escape(session['username'])
    else:
        return redirect(url_for('login'))

# ============================================================DEVICES
@app.route('/devices')
@app.route('/devices/')
@app.route('/devices/<device>')
def devices(device=None):
    if 'username' in session:
        return render_template('devices.html',device=device)
    else:
        return redirect(url_for('login'))
    

# ============================================================SETUP
@app.route('/setup',methods = ['POST', 'GET'])
@app.route('/setup/',methods = ['POST', 'GET'])
def setup():
    if 'username' in session:   
        print("this is setup page")
        result = request.form.to_dict()
        print(result)
        with open("./tp.text", "w") as f:
            json.dump(result, f, indent=4)
        return render_template('setup.html')
    else:
        return redirect(url_for('login'))

# ============================================================MQTT-CONSOLE
@app.route('/mqtt-console')
@app.route('/mqtt-console/')
@app.route('/mqtt-console/<params>')
def mqtt_on(params=None):
    if 'username' in session:
        print("1111111111111111111111111111111111111111111111111111111111")
        print(params)
        print("1111111111111111111111111111111111111111111111111111111111")
        return render_template('mqtt-console.html', data=params)
    else:
        return redirect(url_for('login'))

# =============================================================CMD LINE
@app.route('/sendcmd/')
def sendcmd(name=None):
	if 'username' in session:
		return render_template('sendcmd.html')
	else:
		return redirect(url_for('login'))

# ============================================================UPDATE ADMIN DETAILS
@app.route('/editProfile/', methods=['GET', 'POST'])
def editProfile():
    error = None
    data = []
    rec=[]
    if 'username' in session:
        if request.method == 'POST':
            print("Posted********************************************")
            data.append(request.form['name'])
            data.append(request.form['pass'])
            print(data)
            print(_mysql.editProfile_(mysql, data))
            rec = _mysql.show_(mysql)
            print(rec)
        rec = _mysql.show_(mysql)
        print(rec)
        return render_template('editProfile.html', error=error, data=data, rec=rec)
    else:
        return redirect(url_for('login'))



# ============================================================LOGIN PAGE
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    #print(_mysql.initLogin_(mysql))
    if request.method == 'POST':
        u_name = request.form['username']
        u_pass = request.form['password']
        flag = _mysql.verify_(u_name, u_pass, mysql)
        #print(flag)
        #if request.form['username'] != 'admin' or request.form['password'] != 'admin':
        if(flag == -1):
            error = 'Invalid Credentials. Please try again.'
        else:
            session['username'] = request.form['username']
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

# ============================================================LOGOUT PAGE
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


#=============================================================
#=====================SUPPORT FUNCTIONS=======================
#=============================================================

	
    
#=============================================================
#=====================EXTRA FUNCTIONS=======================
#=============================================================
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

#=============================================================
#========================MAIN FUNCTION=======================
#=============================================================


if  __name__  ==  '__main__' : 
    app.run(host = '0.0.0.0',  port = 5000, threaded = True,  debug = True, ssl_context='adhoc') #Ssl_context = Context ,