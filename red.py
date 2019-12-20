import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)
print("Redis DataBase")
print(r)

key_n = "dev_id"
r.hmset(key_n, {'a':'1', 'b':'2', 'c':'3'})
print(r.hgetall(key_n))


r.hset('s_key_n', 1,'val')
r.expire('s_key_n', 5)
print(r.hgetall(key_n))
