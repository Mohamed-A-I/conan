import sqlite3
from sqlite3 import Error

db = sqlite3.connect('pe.db')
print("db connected")





id="helary"

cursor=db.cursor()

sql="SELECT * FROM `people` WHERE name ='%s' " %(id)

try:
    cursor.execute(sql)
    result=cursor.fetchall()
    for row in result:
        print(row)
except:
    print("unable to fetch data")
    
db.close()

