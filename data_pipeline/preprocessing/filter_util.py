# Modules 
from database.connect_to_database import fetch_data_as_pandas
from storage.connect_storage import upload_to_s3

from typing import Optional
import random

def recommend_by_filter(season, category, sub_category, filter_json, max_per_category=3):
    result = {}

    for cat in ["하의", "아우터", "상의", "신발"]:
        # 입력 category와 같으면 빈 리스트로 처리
        if cat == category:
            result[cat] = []
            continue

        # 여름에는 아우터 제외 (빈 리스트로)
        if season == "여름" and cat == "아우터":
            result[cat] = []
            continue

        # 후보군 조회
        candidates = filter_json.get(season, {}).get(cat, [])
        if not candidates:
            result[cat] = []
            continue

        # 랜덤 셔플 및 추천 수 제한
        shuffled = candidates[:]
        random.shuffle(shuffled)
        result[cat] = shuffled[:max_per_category]

    return result

def get_season_category_map(
    table_name: str,
    category_column: str = "category",
    fixed_category: Optional[str] = None,
    s3_bucket: Optional[str] = None,
    s3_key: Optional[str] = None
) -> dict:
    # 쿼리 구성
    columns = "season, sub_category"
    if not fixed_category:
        columns = f"season, {category_column}, sub_category"

    query = f"""
    SELECT {columns}
    FROM {table_name}
    WHERE season IS NOT NULL AND sub_category IS NOT NULL
    """
    if not fixed_category:
        query += f" AND {category_column} IS NOT NULL"

    df = fetch_data_as_pandas(query)
    season_category_map = {}

    for _, row in df.iterrows():
        # 복수 계절 처리: "봄, 여름" → ["봄", "여름"]
        seasons = [s.strip() for s in row["season"].split(",")]
        category = fixed_category if fixed_category else row[category_column]
        sub_category = row["sub_category"]

        for season in seasons:
            if season not in season_category_map:
                season_category_map[season] = {}

            if category not in season_category_map[season]:
                season_category_map[season][category] = []

            if sub_category not in season_category_map[season][category]:
                season_category_map[season][category].append(sub_category)

    # S3로 저장
    if s3_bucket and s3_key:
        upload_to_s3(season_category_map, s3_bucket, s3_key)

    return season_category_map