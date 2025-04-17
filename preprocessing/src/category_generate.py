from .connect_to_database import fetch_data_as_polars
import json 
from typing import Optional
import random


def recommend_by_filter(season: str, category: str, sub_category: str, filter_json: dict, max_per_category: int = 3) -> dict:
    result = {}

    for cat in ["상의", "하의", "신발"]:
        candidates = filter_json.get(season, {}).get(cat, [])

        # 본인 착용 아이템 제외
        if cat == category:
            filtered = [item for item in candidates if item != sub_category]
        else:
            filtered = candidates

        # 랜덤 셔플 후 상위 N개 추출
        shuffled = filtered[:]
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