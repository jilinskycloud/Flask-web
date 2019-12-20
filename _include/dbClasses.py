import pprint
import redis
import time

class mongodb:
	def insertSpy_(MongoClient, pymongo,data):
		#print("i'm in mongodb")
		client = MongoClient("mongodb://localhost:27017/")
		db = client["ble_data"] 
		dbs = client.list_database_names()
		#print(dbs)
		#print(db)
		r_dat = { '_Did' :data[b'_id'], '_ip' :data[b'_ip'], '_mac' : data[b'_mac'], '_rssi':data[b'_rssi'], '_ext':data[b'_ext'], '_b' : 0, '_c' : 0 }    
		result=db.ble.insert_one(r_dat).inserted_id
		print("MOngo Inserted")
		print(result)

	def insert_(MongoClient, pymongo):
		client = MongoClient("mongodb://localhost:27017/")
		db = client.ble_data 
		print(pymongo.version)
		dbs = client.database_names()		#List DBS
		#print(dbs).decode("utf-8")
		print('testing.......!!!!!!!!')
		#if("ble_data" in dbs):
		print("yes")
		r_dat = { '_time' :11, '_mac' :0, '_rssi':0, '_loc':0, 'a' : 0, 'b' : 0, 'c' : 0 }
		result=db.ble.insert_one(r_dat).inserted_id
		return db

	def show_(db):
		dat = db.ble.find()
		for dat1 in dat:
			print('{0}'.format(dat1['_b']))
		pprint.pprint(db.ble.find_one())
		pprint.pprint(db.ble.find_one({"_time": '01fgh'}))
		return 'success'

	def delDB_(db_name, db):
		db.drop_database(db_name)
		return 'success deleted'

	def delColl_(coll_name, db):
		mycol = db[coll_name]
		mycol.drop()
		return 'success!'
		
	def showColl_(db):
		#cl = db.list_collection_names()           
		#print(cl)
		print('All available Collections:')
		coll = db.list_collection_names(include_system_collections=False)
		#pprint.pprint(db.ble.find_one())
		for collect in coll:
			print(collect)
		return collect


class mysqldb:
	def mysql_(MySQL, app):
		app.config['MYSQL_HOST'] = 'localhost'
		app.config['MYSQL_USER'] = 'root'
		app.config['MYSQL_PASSWORD'] = 'root'
		app.config['MYSQL_DB'] = 'FlaskDb'
		mysql = MySQL(app)
		return mysql
	# Create the DataBase
	def DB_(mysql):
		u_name = 'admin_'
		u_password = 'pass_'
		cur = mysql.connection.cursor()
		#cur.execute("CREATE DATABASE FlaskDb")
		#cur.execute("CREATE TABLE MyUsers(firstName VARCHAR(30), lastName VARCHAR(30))")      
		cur.execute("INSERT INTO MyUsers(firstName, lastName) VALUES (%s, %s)", (u_name, u_password))
		print("inserted....")
		mysql.connection.commit()
		cur.close()
		return 'success'
	def verify_(u_name, u_pass, mysql):
		cur = mysql.connection.cursor()
		print(u_name)
		print(u_pass)
		if(cur.execute("SELECT * FROM MyUsers WHERE firstName=%s and lastName=%s", (u_name, u_pass)) < 1):
			cur.close()
			return -1
		else:
			myresult = cur.fetchone()
			print(myresult)
			cur.close()
			return 0


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
		tm_k = time.time()
		s_key_n = 's_'+str(tm_k)
		print(tm_k)
		print(s_key_n)
		r.hmset(tm_k, {'_id':_id, '_mac':_mac, '_rssi':_rssi, '_ext':_ext, '_ip':_ip})
		print(r.hgetall(tm_k))
		r.hset(s_key_n, 1,'val')
		r.expire(s_key_n, 10)
		#print(r.hgetall(key_n))

	def print_():
		print("huuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu----------haaaaaaaaaaaa\n")