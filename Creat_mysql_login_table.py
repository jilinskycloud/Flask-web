import mysql.connector as mysql
import hashlib

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "root"
)
cur = db.cursor()
dbs_ = cur.execute("SHOW DATABASES")
ax = cur.fetchall()
uname = "admin"
passw = "pass".encode('utf-8')
salt = "skycloud".encode('utf-8')
h = hashlib.new('sha256')
h.update(salt)
h.update(passw)
passw = h.hexdigest()
v = []

for a in ax:
	v.append(a[0])

if 'FlaskDb' in v:
	print(ax)
	print("DATABASE Already Exist Going to rewrite it...")
	cur.execute("DROP DATABASE FlaskDb")
	cur.execute("CREATE DATABASE FlaskDb")
	cur.execute("USE FlaskDb")
	cur.execute("CREATE TABLE login_(id int(11) PRIMARY KEY AUTO_INCREMENT, u_username VARCHAR(30), u_password Text(4294967295))")      
	cur.execute("INSERT INTO login_(u_username, u_password) VALUES (%s, %s)", (uname, passw))
	db.commit()
	#print("inserted....", a)	
cur.close()
print("---------------Create Model -MYSQLDB---------------")



