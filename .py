import redis
r = redis.StrictRedis()
pubsub = r.pubsub()
pubsub.psubscribe("*")
for msg in pubsub.listen():
    s = msg["data"]
    #print(s)
    if(s != 1):
    	key_ = s.decode("utf-8")
    	key_ = key_.replace('s_', '')
		#r.delete("dev_id")
		print(key_)
