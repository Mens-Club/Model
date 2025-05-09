import pymysql
import os
import re
import random
from dotenv import load_dotenv

load_dotenv()

connection = pymysql.connect(
    host=os.environ['MYSQL_HOST'],
    user=os.environ['MYSQL_USER'],
    password=os.environ['MYSQL_PASSWD'],
    db=os.environ['MYSQL_DB'],
    port=int(os.environ['MYSQL_PORT']),
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

def extract_clothing_name(answer: str) -> str:
    match = re.search(r'이 옷은 (.+?)입니다', answer)
    return match.group(1) if match else None

def get_random_item_id(cursor, category_name):
    cursor.execute("""
        SELECT idx FROM mens_table_refine
        WHERE sub_category = %s
    """, (category_name,))
    results = cursor.fetchall()
    return random.choice(results)['idx'] if results else None

def get_price(cursor, item_id):
    if not item_id:
        return 0
    cursor.execute("SELECT price FROM mens_table_refine WHERE idx = %s", (item_id,))
    result = cursor.fetchone()
    return result['price'] if result else 0

try:
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT r.id, r.top_id, r.bottom_id, r.outer_id, r.shoes_id, r.style, r.answer, r.detail, p.id AS picked_id
            FROM recommend r
            JOIN picked p ON r.id = p.recommend_id
            WHERE (r.top_id IS NULL OR r.bottom_id IS NULL OR r.shoes_id IS NULL OR r.outer_id IS NULL)
              AND p.whether_main = 0
        """)
        rows = cursor.fetchall()

        for row in rows:
            top_id = row['top_id']
            bottom_id = row['bottom_id']
            outer_id = row['outer_id']
            shoes_id = row['shoes_id']
            style = row['style']
            detail = row['detail']
            answer = row['answer']
            picked_id = row['picked_id']

            clothing_name = extract_clothing_name(answer)
            if not clothing_name:
                continue

            filled_id = get_random_item_id(cursor, clothing_name)
            if not filled_id:
                continue

            if not top_id:
                top_id = filled_id
            elif not bottom_id:
                bottom_id = filled_id
            elif not shoes_id:
                shoes_id = filled_id
            elif not outer_id and '여름' not in answer:
                outer_id = filled_id

            total_price = (
                get_price(cursor, top_id) +
                get_price(cursor, bottom_id) +
                get_price(cursor, outer_id) +
                get_price(cursor, shoes_id)
            )

            cursor.execute("""
                INSERT INTO main_recommend (top_id, bottom_id, outer_id, shoes_id, style, total_price, detail)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                top_id, bottom_id, outer_id, shoes_id, style, total_price, detail
            ))

            cursor.execute("""
                UPDATE picked SET whether_main = 1 WHERE id = %s
            """, (picked_id,))

            print(f"Inserted main_recommend from recommend.id={row['id']} (picked.id={picked_id})")

    connection.commit()
finally:
    connection.close()
