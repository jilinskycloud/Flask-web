import redis
import requests
import time

class MQTT_:
	def connect_(Mqtt, app, _redis):
		app.config['MQTT_BROKER_URL'] = 'localhost'
		app.config['MQTT_BROKER_PORT'] = 1883
		app.config['MQTT_USERNAME'] = ''
		app.config['MQTT_PASSWORD'] = ''
		app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds
		mqtt = Mqtt(app)
		@mqtt.on_connect()
		def handle_connect(client, userdata, flags, rc):
			mqtt.subscribe('exp')
			mqtt.subscribe('ble')

		@mqtt.on_message()
		def handle_mqtt_message(client, userdata, message):
			data = dict(
        		topic=message.topic,
        		payload=message.payload.decode(),
        	)
			print("Ble Data Message")
			print(data['payload'])
			_redis.create_(data['payload'])

			#r = requests.get('http://192.168.1.74:5000/mqtt-console/', params='abc')
			#print(r.text)
			#print(r.url)

			print("Working!!!!!!!! ")

class HTTP_:
	def connect_(http_data, app, _redis):
		print("This Message is from HTTP Heartbeat file ......")
		print(http_data)
		_redis.create_(http_data)


class heartBeat_:
	def hd_insert(MongoClient, pymongo, hbD, _redis):
		
		client = MongoClient("mongodb://localhost:27017/")
		db = client["ble_data"] 
		data = hbD.split('|')
		_sr  = data[0]
		_ip  = data[1]
		_ext = data[2]
		#dbs = client.list_database_names()
		#data_ = {}
		#convert binary dictionary
		#for key, value in data.items(): 
		#	data_[key.decode("utf-8")] = value.decode("utf-8") 
		#print(_redis.createHB_(data))
		tm_k = time.time()
		#tm_k1 = tm_k+5
		#tm_k2 = tm_k+10
		#tm_k3 = tm_k-25
		if( db.reg_devices.find_one({"_id": _sr}) == None):
			r_dat = { '_id' :_sr, 'time' :tm_k, 'extra' : _ip}    
			result=db.reg_devices.insert_one(r_dat)
			print("New Device inserted")
		else:
			print("Already Exist")
			db.reg_devices.update_one({'_id': _sr},{'$set': {'time': tm_k, 'extra': _ip}}, upsert=False)
			#db.reg_devices.update_one({'_id': "000000002"},{'$set': {'time': tm_k1}}, upsert=False)
			#db.reg_devices.update_one({'_id': "000000003"},{'$set': {'time': tm_k2}}, upsert=False)
			#db.reg_devices.update_one({'_id': "000000004"},{'$set': {'time': tm_k3}}, upsert=False)  
		print("---------------HB Data Inserted -MongoDb---------------")
		return "OK"

	def status_(MongoClient, pymongo):
		client = MongoClient("mongodb://localhost:27017/")
		db = client["ble_data"] 
		tm_k = time.time()
		print(tm_k)
		tm_k = tm_k-10
		axv = db.reg_devices.find( { "time": { "$gt": tm_k } } )
		return axv

	def delDevice(MongoClient, pymongo, sid):
		client = MongoClient("mongodb://localhost:27017/")
		db = client["ble_data"]
		print(sid)
		db.reg_devices.remove({"_id" : sid})
		print("---------------HB Data Deleted -MongoDb---------------")
		return "OK"


