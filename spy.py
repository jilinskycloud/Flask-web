import redis
import pymongo
from pymongo import MongoClient
from _include.dbClasses import mongodb as _mongodb


r = redis.StrictRedis()
pubsub = r.pubsub()
pubsub.psubscribe("*")
for msg in pubsub.listen():
	s = msg["data"]
	#print(s)
	if(s != 1):
		key_1 = s.decode("utf-8")
		#print(key_1)
		key_ = key_1.replace('s_', '')
		#print(key_)
		print(r.hgetall(key_))
		_mongodb.insertSpy_(MongoClient, pymongo, data=r.hgetall(key_))

		r.delete(key_)
		print(r.hgetall(key_))
		print("deleted----------------------------")
		#print(key_)
