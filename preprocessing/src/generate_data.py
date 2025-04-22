import json
from .connect_to_database import fetch_data_as_polars
from .category_generate import recommend_by_filter
import random 



# Llama3.2-vision 학습을 위한 instruction 매핑 

def split_and_filter_seasons(row, filter_json):
    valid_seasons = []
    all_seasons = [s.strip() for s in row["season"].split(",")]

    for season in all_seasons:
        if row["main_category"] not in filter_json.get(season, {}):
            continue    
        if row["sub_category"] in filter_json[season][row["main_category"]]:
            valid_seasons.append(season)

    # ✅ 유효한 계절 중 랜덤 하나만 선택
    return [random.choice(valid_seasons)] if valid_seasons else []

def generate_instruction_sample(season, category, sub_category, color, thumbnail_url, filter_json):
    instruction = "당신은 패션 추천 전문가입니다. 아래 이미지를 보고 판단하여 적절한 코디를 JSON 형식으로 추천해주세요. 결과는 다음 형식이어야 합니다: { \"answer\": ..., \"recommend\": { \"상의\": [...], \"아우터\": [...], \"하의\": [...], \"신발\": [...] } }"
    answer = f"이 상품은 {sub_category} 상품이고 {color} 컬러이며 {season}에 맞는 상품입니다. 그에 맞는 상품들을 추천드릴게요."
    
    recommend = recommend_by_filter(
        season=season,
        category=category,
        sub_category=sub_category,
        filter_json=filter_json,
        max_per_category=3
    )

    return {
        "instruction": instruction,
        "input": {
            "season": season,
            "category": category,
            "sub_category": sub_category,
            "color": color,
            "image": thumbnail_url
        },
        "output": {
            "answer": answer,
            "recommend": recommend
        }
    }



def generate_instruction_dataset_from_maintable(filter_json: dict, clothing_query: str, shoes_query: str) -> list:
    df_clothing = fetch_data_as_polars(clothing_query)
    df_shoes = fetch_data_as_polars(shoes_query)

    all_samples = []

    # ✅ 의류
    for row in df_clothing.iter_rows(named=True):
        try:
            valid_seasons = split_and_filter_seasons(row, filter_json)
            for season in valid_seasons:
                sample = generate_instruction_sample(
                    season=season,
                    category=row["main_category"],
                    sub_category=row["sub_category"],
                    color=row["color"],
                    thumbnail_url=row["thumbnail_url"],
                    filter_json=filter_json
                )
                all_samples.append(sample)
        except Exception as e:
            print(f"[의류 FAIL] {row} - {e}")

    # ✅ 신발 (main_category 없음 → category는 고정)
    for row in df_shoes.iter_rows(named=True):
        try:
            row["main_category"] = "신발"
            valid_seasons = split_and_filter_seasons(row, filter_json)
            for season in valid_seasons:
                sample = generate_instruction_sample(
                    season=season,
                    category="신발",
                    sub_category=row["sub_category"],
                    color=row["color"],
                    thumbnail_url=row["thumbnail_url"],
                    filter_json=filter_json
                )
                all_samples.append(sample)
        except Exception as e:
            print(f"[신발 FAIL] {row} - {e}")

    return all_samples

