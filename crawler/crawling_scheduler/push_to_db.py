import pandas as pd
from tqdm import tqdm

def push_to_db(db, shoes_results, other_results):
    shoes_df = pd.DataFrame(shoes_results)
    other_df = pd.DataFrame(other_results)

    cursor = db.cursor()

    # 데이터 삽입 쿼리 준비
    insert_query = """
    INSERT INTO menstable_test2 (
        style, season, fit, color, goods_name, thumbnail_url,
        is_soldout, goods_url, brand, normal_price, price,
        main_category, sub_category
    ) VALUES (
        %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s
    )
    """

    # tqdm을 DataFrame에 적용
    for _, row in tqdm(other_df.iterrows(), total=len(other_df)):
        values = (
            row['스타일'],           # style
            row['계절'],            # season
            row['핏'],              # fit
            row['컬러'],            # color
            row['제품명'],          # goods_name
            row['썸네일링크'],      # thumbnail_url
            row['판매여부'],        # is_soldout
            row['제품링크'],        # goods_url
            row['브랜드'],          # brand
            row['원가'],            # normal_price
            row['가격'],            # price
            row['대분류'],
            row['소분류']           # category_name (← 소분류만 들어감)
        )
        cursor.execute(insert_query, values)

    db.commit()

    insert_query = """
    INSERT INTO shoes_test2 (
        color, sub_category, season, goods_name, thumbnail_url, is_soldout, goods_url, brand, normal_price, price
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
    """

    # tqdm을 DataFrame에 적용
    for _, row in tqdm(shoes_df.iterrows(), total=len(shoes_df)):
        values = (
            row['컬러'],           # style
            row['소분류'],            # season
            row['계절'],              # fit
            row['제품명'],            # color
            row['썸네일링크'],          # goods_name
            row['판매여부'],        # is_soldout
            row['제품링크'],        # goods_url
            row['브랜드'],          # brand
            row['원가'],            # normal_price
            row['가격'],            # price
        )
        cursor.execute(insert_query, values)

    # 커밋 & 연결 종료
    db.commit()
    cursor.close()
    db.close()
