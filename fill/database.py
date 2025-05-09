import random

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

def fetch_recommendations_to_process(cursor):
    cursor.execute("""
        SELECT r.id, r.top_id, r.bottom_id, r.outer_id, r.shoes_id, r.style, r.answer, r.detail, p.id AS picked_id
        FROM recommend r
        JOIN picked p ON r.id = p.recommend_id
        WHERE (r.top_id IS NULL OR r.bottom_id IS NULL OR r.shoes_id IS NULL OR r.outer_id IS NULL)
          AND p.whether_main = 0
    """)
    return cursor.fetchall()

def update_whether_main(cursor, picked_id):
    cursor.execute("""
        UPDATE picked SET whether_main = 1 WHERE id = %s
    """, (picked_id,))