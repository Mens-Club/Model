import json

# 1. JSON 파일 불러오기
with open("../data/season_category_filter.json", encoding="utf-8") as f:
    clothes = json.load(f)

with open("../data/season_category_filter_shoes.json", encoding="utf-8") as f:
    shoes = json.load(f)

# 2. 병합
merged = {}

all_seasons = set(clothes.keys()) | set(shoes.keys())

for season in all_seasons:
    merged[season] = {}

    # 의류 카테고리 추가
    if season in clothes:
        for cat, items in clothes[season].items():
            merged[season][cat] = items

    # 신발 카테고리 추가
    if season in shoes:
        merged[season]["신발"] = shoes[season].get("신발", [])

# 3. 저장
with open("../data/season_filter_combined.json", "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)

print("✅ 병합 완료: season_filter_combined.json")
