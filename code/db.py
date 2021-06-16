import sqlite3
from sqlite3 import Error

db = sqlite3.connect('pe.db')
print("db connected")




cursor=db.cursor()
cursor.execute("DROP TABLE IF EXISTS people")
    
sql = "CREATE TABLE people ( id CHAR(30)NOT NULL ,NAME CHAR(20) , TEL CHAR(15), ADDR CHAR(20), DIS CHAR(50) )"
try:
    cursor.execute(sql)
    db.commit()
except:
    db.rollback()
    
 
db.close()

