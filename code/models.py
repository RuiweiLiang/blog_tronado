import pymysql
from settings import settings

db = pymysql.connect(host=settings['host'], user=settings['db_user'], password=settings['db_user_pwd'], database=settings['db_name'])

cursor = db.cursor()
cursor.execute("SELECT * from user")
data = cursor.fetchone()
