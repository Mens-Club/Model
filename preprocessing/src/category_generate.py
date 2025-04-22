from .connect_to_database import fetch_data_as_polars
import json 
from typing import Optional
import random


def recommend_by_filter(season, category, sub_category, filter_json, max_per_category=3):
    result = {}

    for cat in ["상의", "아우터", "하의", "신발"]:
        # 입력 category와 같으면 skip (본인 제외 목적)
        if cat == category:
            continue
        if season == "여름" and cat == "아우터":
            continue

        candidates = filter_json.get(season, {}).get(cat, [])

        # 추천 후보군 셔플 및 추출
        shuffled = candidates[:]
        random.shuffle(shuffled)
        result[cat] = shuffled[:max_per_category]

    return result

def get_season_category_map(
    table_name: str,
    category_column: str = "category",
    fixed_category: Optional[str] = None,
    save_path: Optional[str] = None
) -> dict:
    # 쿼리 동적 구성
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

    df = fetch_data_as_polars(query)
    season_category_map = {}

    for row in df.iter_rows(named=True):
        season = row["season"]
        category = fixed_category if fixed_category else row[category_column]
        sub_category = row["sub_category"]

        if season not in season_category_map:
            season_category_map[season] = {}

        if category not in season_category_map[season]:
            season_category_map[season][category] = []

        if sub_category not in season_category_map[season][category]:
            season_category_map[season][category].append(sub_category)

    # 저장 옵션 처리
    if save_path:
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(season_category_map, f, ensure_ascii=False, indent=2)

    return season_category_map