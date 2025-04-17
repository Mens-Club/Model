import json
from .connect_to_database import fetch_data_as_polars
from .category_generate import recommend_by_filter



# Llama3.2-vision 학습을 위한 instruction 매핑 

def generate_instruction_sample(season, category, sub_category, color, thumbnail_url, filter_json):
    instruction = "당신은 패션추천 전문가입니다. 아래 이미지를 보고 판단하여 적절한 코디를 추천해주세요."
    answer = f"이 상품은 {category} 상품이고 {color}색이고 {season}에 맞는 상품입니다. 그에 맞는 상품들을 추천드릴게요."
    
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
            "image" : thumbnail_url
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

    # 의류
    for row in df_clothing.iter_rows(named=True):
        try:
            sample = generate_instruction_sample(
                season=row["season"],
                category=row["main_category"],
                sub_category=row["sub_category"],
                color=row["color"],
                thumbnail_url=row["thumbnail_url"],
                filter_json=filter_json
            )
            all_samples.append(sample)
        except Exception as e:
            print(f"의류 결합 실패 사유: {row} - {e}")

    # 신발 (category는 고정: "신발") 사유는... main_category는 변칙이 없음
    for row in df_shoes.iter_rows(named=True):
        try:
            sample = generate_instruction_sample(
                season=row["season"],
                category="신발",  # 카테고리는 고정
                sub_category=row["sub_category"],
                color=row["color"],
                thumbnail_url=row["thumbnail_url"],
                filter_json=filter_json
            )
            all_samples.append(sample)
        except Exception as e:
            print(f"신발 결합 실패 사유: {row} - {e}")

    return all_samples
