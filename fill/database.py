import random

SHOES_CATEGORIES = {
    "캔버스/단화",
    "패션스니커즈화",
    "앵클/숏 부츠",
    "미들/하프 부츠",
    "워커",
    "더비 슈즈",
    "스트레이트 팁",
    "로퍼",
    "모카신",
    "쪼리/플립플랍",
    "스포츠/캐주얼 샌들"
}

COLOR_PALETTE_BY_SEASON = {
    "봄": ['오트밀', '아이보리', '화이트', '블랙', '베이지', '네이비', "흑청", "진청", "연청", "중청"],
    "여름": ['스카이블루', '네이비', '화이트', '블랙', "연청", "중청", "흑청"],
    "가을": ['화이트', '블랙', '버건디', '오트밀', '아이보리', '카키', '베이지', '브라운', "흑청", "진청", "중청"],
    "겨울": ['화이트', '그레이', '블랙', '네이비', '카키', "흑청", "진청", "중청"]
}

def get_random_item_id(cursor, category_name):
    # 카테고리가 신발 리스트에 포함돼 있으면 shoes 테이블에서 조회
    table_name = "shoes" if category_name in SHOES_CATEGORIES else "clothes"
    
    query = f"""
        SELECT id FROM {table_name}
        WHERE sub_category = %s
    """
    cursor.execute(query, (category_name,))
    results = cursor.fetchall()
    return random.choice(results)['id'] if results else None

def get_price(cursor, item_id, isShoes):
    if not item_id:
        return 0
    if isShoes:
        cursor.execute("SELECT price FROM shoes WHERE id = %s", (item_id,))
    else:
        cursor.execute("SELECT price FROM clothes WHERE id = %s", (item_id,))
    result = cursor.fetchone()
    return result['price'] if result else 0

def fetch_recommendations_to_process(cursor):
    cursor.execute("""
        SELECT r.id, r.top_id, r.bottom_id, r.outer_id, r.shoes_id, r.style, r.answer, r.reasoning_text, p.id AS picked_id
        FROM recommend_recommendation r
        JOIN recommend_bookmark p ON r.id = p.recommendation_id
        WHERE (r.top_id IS NULL OR r.bottom_id IS NULL OR r.shoes_id IS NULL OR r.outer_id IS NULL)
          AND p.whether_main = 0
    """)
    return cursor.fetchall()

def update_whether_main(cursor, picked_id):
    cursor.execute("""
        UPDATE recommend_bookmark SET whether_main = 1 WHERE id = %s
    """, (picked_id,))