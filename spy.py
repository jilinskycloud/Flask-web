import redis
import pymongo
from pymongo import MongoClient
from _include.dbClasses import mongodb as _mongodb


r = redis.StrictRedis()
#r = redis.StrictRedis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)
pubsub = r.pubsub()
pubsub.psubscribe("*")
print("sdhfhjsgfjgsjdfgsjgdjf")
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
