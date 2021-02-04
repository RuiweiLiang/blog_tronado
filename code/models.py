import pymysql, pymongo
from settings import settings

# db = pymysql.connect(host=settings['host'], user=settings['db_user'], password=settings['db_user_pwd'], database=settings['db_name'])
# cursor = db.cursor()
# cursor.execute("SELECT * from user")
# data = cursor.fetchone()
client = pymongo.MongoClient(host="139.9.222.155", port=27017)
db = client.trnodao
db.authenticate("pig", "123456", mechanism='SCRAM-SHA-1')



