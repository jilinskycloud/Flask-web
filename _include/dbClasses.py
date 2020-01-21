import pprint
import redis
import time
from bson.objectid import ObjectId



#------------------------------------------MONGODB CLASS
class mongodb:
	def insertSpy_(MongoClient, pymongo,data):
		client = MongoClient("mongodb://localhost:27017/")
		db = client["ble_data"] 
		dbs = client.list_database_names()
		data_ = {}
		#convert binary dictionary
		for key, value in data.items(): 
			data_[key.decode("utf-8")] = value.decode("utf-8") 
		#print("here im in mongo db hehehehehehe")
		print(data_)
		r_dat = { '_Did' :data_['_uuid'], '_mac' : data_['_mac'], '_rssi':data_['_rssi'], '_adv':data_['_adv'], '_maj':data_['_maj'], '_min':data_['_min'], '_tx':data_['_tx'] }
		print(r_dat)
		#r_dat = { '_Did' :data_['_id'], '_ip' :data_['_ip'], '_mac' : data_['_mac'], '_rssi':data_['_rssi'], '_ext':data_['_ext'], '_b' : 0, '_c' : 0 }    
		result=db.ble.insert_one(r_dat).inserted_id
		print("---------------BLE Data Inserted -MongoDb---------------")
		print(result)
		

	def initMongo_(MongoClient, pymongo):
		client = MongoClient("mongodb://localhost:27017/")
		db = client.ble_data 
		print(pymongo.version)
		dbs = client.database_names()		#List DBS
		print("---------------Init -MongoDb---------------")
		return db

	def insert_(MongoClient, pymongo, data):
		client = MongoClient("mongodb://localhost:27017/")
		db = client.ble_data 
		#dbs = client.database_names()		#List DBS
		#print(dbs).decode("utf-8")
		print(data)
		r_dat = { '_Did' :data[1], '_mac' :data[2], '_rssi' : data[3], '_adv':data[4], '_maj':data[5], '_min' :data[6], '_tx' :data[7] } 
		result=db[data[0]].insert_one(r_dat).inserted_id
		print("---------------Insert into -MongoDb---------------")
		return 'ok'

	def show_(db):
		dat = db.ble.find()
		for dat1 in dat:
			print('{0}'.format(dat1['_b']))
		pprint.pprint(db.ble.find_one())
		pprint.pprint(db.ble.find_one({"_time": '01fgh'}))
		print("---------------Show Query -MongoDb---------------")
		return 'success'

	def delDB_(db_name, MongoClient):
		client = MongoClient("mongodb://localhost:27017/")
		client.drop_database('ble_data')
		print("---------------Delete DataBase -MongoDb---------------")
		return 'success deleted'

	def delColl_(coll_name, db):
		mycol = db[coll_name]
		mycol.drop()
		print("---------------Delete Collection -MongoDb---------------")
		return 'success!'

	def delRec_(coll_name, db, _id):
		print(coll_name)
		db.ble.remove( {"_id": ObjectId(_id)});
		print("---------------Delete Record -MongoDb---------------")
		return 'success!'
		
	def showColl_(db):
		#cl = db.list_collection_names()           
		#print(cl)
		#print('All available Collections:')
		coll = db.list_collection_names(include_system_collections=False)
		#pprint.pprint(db.ble.find_one())
		#for collect in coll:
		#	print(collect)
		print("---------------Show Collections -MongoDb---------------")
		return coll

	def showRec_(collname, db):
		pprint.pprint(db.collname.find_one())
		print(collname)
		rec_ = db[collname].find()
		print("---------------Show Records -MongoDb---------------")
		return rec_


#------------------------------------------MYSQL CLASS
class mysqldb:
	def initMysql_(MySQL, app):
		app.config['MYSQL_HOST'] = 'localhost'
		app.config['MYSQL_USER'] = 'root'
		app.config['MYSQL_PASSWORD'] = 'root'
		app.config['MYSQL_DB'] = 'FlaskDb'
		mysql = MySQL(app)
		print(mysql)
		print("---------------Init -MYSQLDB---------------")
		return mysql
	# Create the DataBase-----------------------------------------------------------------------------------This One have to edit 
	def createModel_(MySQL, app):
		app.config['MYSQL_HOST'] = 'localhost'
		app.config['MYSQL_USER'] = 'root'
		app.config['MYSQL_PASSWORD'] = 'root'
		mysql = MySQL(app)
		print(mysql)
		cur = mysql.connection.cursor()
		dbs_ = cur.execute("SHOW DATABASES")
		ax = cur.fetchall()
		print(ax)
		for a in ax:
			if('FlaskDb' in a[0]):
				print(a)
				print("it exist")
				cur.close()
				mysql=0
				return 'OK'
			else:
				#query = "DROP DATABASE FlaskDb"
				#cur.execute(query)
				cur = mysql.connection.cursor()
				cur.execute("CREATE DATABASE FlaskDb")
				cur.execute("USE FlaskDb")
				cur.execute("CREATE TABLE login_(id int(11) PRIMARY KEY AUTO_INCREMENT, firstName VARCHAR(30), lastName VARCHAR(30))")      
				cur.execute("INSERT INTO login_(firstName, lastName) VALUES (%s, %s)", ("admin", "pass"))
				print("inserted....")
				mysql.connection.commit()
				cur.close()
				return "OK"
		print("---------------Create Model -MYSQLDB---------------")
		return "OK"
	# Login Verify
	def verify_(u_name, u_pass, mysql):
		cur = mysql.connection.cursor()
		print(u_name)
		print(u_pass)
		print("---------------Verify Login -MYSQLDB---------------")
		flag1 = cur.execute("SELECT * FROM login_ WHERE firstName=%s and lastName=%s", (u_name, u_pass))
		print(flag1)
		if(flag1 < 1):
			cur.close()
			return -1
		else:
			myresult = cur.fetchone()
			print(myresult)
			cur.close()
			return 0

	def show_(mysql):
		cur = mysql.connection.cursor()
		#print(cur.execute("SELECT version()"))
		#print(cur.fetchall())
		#print(cur)
		if(cur.execute("SELECT * FROM login_") == 0):
			print("There is no record!")
		rec = cur.fetchall()
		print("---------------Show Table -MYSQLDB---------------")
		return rec

	def editProfile_(mysql, data):
		cur = mysql.connection.cursor()    
		cur.execute("INSERT INTO login_(firstName, lastName) VALUES (%s, %s)", (data[0], data[1]))
		mysql.connection.commit()
		cur.close()
		print("---------------Update Profile -MYSQLDB---------------")
		return 'OK'

	def delProfile_(mysql, ids):
		cur = mysql.connection.cursor()    
		cur.execute("DELETE FROM login_ where id= %s", (ids))
		mysql.connection.commit()
		cur.close()
		print("---------------Delete Profile -MYSQLDB---------------")
		return 'OK'
		


#------------------------------------------MYSQL CLASS

r = redis.StrictRedis(host='localhost', port=6379, db=0)
class redisdb:
	def set_spy():
		r = redis.StrictRedis()
		pubsub = r.pubsub()
		pubsub.psubscribe("*")
		for msg in pubsub.listen():
			s = msg["data"]
    		#print(s)
			if(s != 1):
				print(s.decode("utf-8")) 

	def create_(data):
		print("-----------------------------------------------ssssssssssssssss\n")
		#print(data)
		'''
		da = data.split('|')
		print(da)
		print(da[0])
		_id  = da[0]
		_mac = da[1]
		_rssi= da[2]
		_ext = da[3]
		_ip  = da[4]
		print("-----------------------------------------------ssssssssssssssss\n")
		print(_id)
		print(_mac)
		'''
		tm_k = time.time()
		s_key_n = 's_'+str(tm_k)
		#print(tm_k)
		#print(s_key_n)
		r.hmset(tm_k, {'_uuid':data['uuid'], '_mac':data['mac'], '_rssi':data['rssi'], '_adv':data['adv'], '_tx':data['tx'], '_maj':data['maj'], '_min':data['min']})
		#print(r.hgetall(tm_k))
		r.hset(s_key_n, 1,'val')
		r.expire(s_key_n, 10)
		#print(r.hgetall(key_n))
		
	'''
	def createHB_(data):
		print("-----------------------------------------------in ccreateHB-REDIS\n")
		tm_k = time.time()
		r.hmset(data[0], {'_tm':tm_k, '_ext':data[2]})
		r.expire(data[0], 10)
		print(r.hgetall(tm_k))
	'''	

	def print_():
		print("huuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu----------haaaaaaaaaaaa\n")
















