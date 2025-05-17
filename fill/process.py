from database import get_random_item_id, get_price, fetch_recommendations_to_process, update_whether_main
from utils import extract_clothing_name

def process_recommendations(cursor):
    rows = fetch_recommendations_to_process(cursor)
    for row in rows:
        top_id = row['top_id']
        bottom_id = row['bottom_id']
        outer_id = row['outer_id']
        shoes_id = row['shoes_id']
        style = row['style']
        reasoning_text = row['reasoning_text']
        answer = row['answer']
        picked_id = row['picked_id']

        clothing_name = extract_clothing_name(answer)
        if not clothing_name:
            print('clothing_name')
            continue

        filled_id = get_random_item_id(cursor, clothing_name)
        if not filled_id:
            print('filled_id')
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
            INSERT INTO recommend_main_recommendation (top_id, bottom_id, outer_id, shoes_id, style, total_price, reasoning_text)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            top_id, bottom_id, outer_id, shoes_id, style, total_price, reasoning_text
        ))

        # 처리 후 picked의 whether_main 값을 1로 업데이트
        update_whether_main(cursor, picked_id)

        print(f"Inserted main_recommend from recommend.id={row['id']} (picked.id={picked_id})")