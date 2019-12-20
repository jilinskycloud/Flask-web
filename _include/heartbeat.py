import redis
from flask import session

class heartbeat:
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
			#render_template('/mqtt-console/topic')
			print("Ble Data Message")
			print(data['payload'])
			_redis.create_(data['payload'])

			print("Working!!!!!!!! ")
