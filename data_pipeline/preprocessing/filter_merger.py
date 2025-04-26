from typing import Dict, List 

def merge_season_filters(
    clothes: Dict[str, Dict[str, List[str]]], # 의류 필터 
    shoes: Dict[str, Dict[str, List[str]]] # 신발 필터
) -> Dict[str, Dict[str, List[str]]]: # Dict 안에 List nested 
    merged = {}
    all_seasons = set(clothes.keys()) | set(shoes.keys())

    for season in all_seasons:
        merged[season] = {}

        # 의류 추가
        if season in clothes:
            for cat, items in clothes[season].items():
                merged[season][cat] = items

        # 신발 추가
        if season in shoes and "신발" in shoes[season]:
            merged[season]["신발"] = shoes[season]["신발"]

    return merged
    