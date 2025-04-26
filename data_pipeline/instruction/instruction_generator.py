from database.connect_to_database import fetch_data_as_pandas
from preprocessing.filter_util import recommend_by_filter
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

    # 유효한 계절 중 랜덤 하나만 선택
    return [random.choice(valid_seasons)] if valid_seasons else []

def generate_instruction_sample(season, category, sub_category, color, thumbnail_url, filter_json):
    
    instruction = (
        "당신은 패션 추천 전문가입니다. 아래 이미지를 보고 판단하여 적절한 코디를 JSON 형식으로 추천해주세요.\n\n"
        "이미지를 참고하여 다음 형식에 맞게 추천해주세요:\n"
        '{ "answer": ..., "recommend": { "상의": [...], "아우터": [...], "하의": [...], "신발": [...] } }\n\n'
        "*주의*: \n"
        f"1) `answer` 문장에 반드시 “{season}에 잘 어울리는 스타일입니다”처럼 계절을 언급할 것.\n"
        "2) `recommend` 내 각 카테고리별로 최소 3개의 아이템을 제시할 것.\n"
        "3) 입력된 아이템(예: 화이트 데님 팬츠)은 해당 카테고리에서 제외하고, 나머지 카테고리는 모두 추천할 것.\n"
    )


    answer = f"이 상품은 {sub_category}로 보이며 해당 상품은 {season}에 맞는 상품입니다. 그에 맞는 상품들을 추천드릴게요."
    
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
    df_clothing = fetch_data_as_pandas(clothing_query)
    df_shoes = fetch_data_as_pandas(shoes_query)

    all_samples = []

    # 의류
    for _, row in df_clothing.iterrows():
        try:
            valid_seasons = split_and_filter_seasons(row, filter_json)
            for season in valid_seasons:
                sample = generate_instruction_sample(
                    season=season,
                    category=row["main_category"],
                    sub_category=row["sub_category"],
                    color=row["color"],
                    thumbnail_url=row["s3_path"],
                    filter_json=filter_json
                )
                all_samples.append(sample)
                
        except Exception as e:
            print(f"의류 실패 사유 :  {row} - {e}")

    # 신발 (main_category 없음 → category는 고정)
    for _, row in df_shoes.iterrows():
        try:
            row["main_category"] = "신발"
            valid_seasons = split_and_filter_seasons(row, filter_json)
            for season in valid_seasons:
                sample = generate_instruction_sample(
                    season=season,
                    category="신발",
                    sub_category=row["sub_category"],
                    color=row["color"],
                    thumbnail_url=row["s3_path"], # url 변경
                    filter_json=filter_json
                )
                all_samples.append(sample)
        except Exception as e:
            print(f"신발 실패 사유 : {row} - {e}")

    return all_samples

