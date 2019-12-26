import redis
import requests

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


