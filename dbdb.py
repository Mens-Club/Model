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

try:
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, top_id, bottom_id, outer_id, shoes_id, style, answer, detail
            FROM recommend
            WHERE top_id IS NULL
            OR bottom_id IS NULL
            OR shoes_id IS NULL
            OR (outer_id IS NULL AND answer NOT LIKE '%여름%')
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

            if not top_id or not bottom_id or not shoes_id or (not outer_id and '여름' not in answer):
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

            def get_price(table, item_id):
                if not item_id:
                    return 0
                cursor.execute(f"SELECT price FROM {table} WHERE idx = %s", (item_id,))
                result = cursor.fetchone()
                return result['price'] if result else 0

            total_price = (
                get_price('mens_table_refine', top_id) +
                get_price('mens_table_refine', bottom_id) +
                get_price('mens_table_refine', outer_id) +
                get_price('mens_table_refine', shoes_id)
            )

            cursor.execute("""
                INSERT INTO main_recommend (top_id, bottom_id, outer_id, shoes_id, style, total_price, detail)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                top_id, bottom_id, outer_id, shoes_id, style, total_price, detail
            ))
            print(f"Inserted new main_recommend row from recommend.id={row['id']}")

    connection.commit()
finally:
    connection.close()
