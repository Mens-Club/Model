import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return pymysql.connect(
        host=os.environ['MYSQL_HOST'],
        user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PASSWD'],
        db=os.environ['MYSQL_DB'],
        port=int(os.environ['MYSQL_PORT']),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )