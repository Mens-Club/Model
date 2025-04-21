import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

categories = {}

def connect_to_db():
    # DB 연결
    db = pymysql.connect(
        host=os.environ['MYSQL_HOST'],
        port=int(os.environ['MYSQL_PORT']),
        user=os.environ['MYSQL_USER'],
        passwd=os.environ['MYSQL_PASSWD'],
        db=os.environ['MYSQL_DB'],
        charset='utf8mb4',
        use_unicode=True
    )

    return db

def get_categories(db):
    cursor = db.cursor()

    # INSERT SQL 문 (자동 생성되는 idx, created_at, updated_at은 제외)
    top_sql = "SELECT Category_Name, Category_Code FROM PRODUCT_CATEGORY WHERE Major_Category = '상의';"
    cursor.execute(top_sql)
    categories['상의'] = cursor.fetchall()

    outwear_sql = "SELECT Category_Name, Category_Code FROM PRODUCT_CATEGORY WHERE Major_Category = '아우터';"
    cursor.execute(outwear_sql)
    categories['아우터'] = cursor.fetchall()

    bottom_sql = "SELECT Category_Name, Category_Code FROM PRODUCT_CATEGORY WHERE Major_Category = '하의';"
    cursor.execute(bottom_sql)
    categories['하의'] = cursor.fetchall()

    shoes_sql = "SELECT Category_Name, Category_Code FROM PRODUCT_CATEGORY WHERE Major_Category = '신발';"
    cursor.execute(shoes_sql)
    categories['신발'] = cursor.fetchall()
    cursor.close()
    db.close()

    return categories