from src.generate_data import generate_instruction_dataset_from_maintable
import json 

def main():
    
    # 옷 쿼리
    query_clothing = """
    SELECT season, main_category, sub_category, color, thumbnail_url
    FROM menstable
    WHERE season IS NOT NULL AND main_category IS NOT NULL AND sub_category IS NOT NULL AND color IS NOT NULL AND thumbnail_url IS NOT NULL
    """

    # 신발 쿼리
    query_shoes = """
    SELECT season, sub_category, color, thumbnail_url
    FROM shoes_test
    """
    
    with open("../data/season_filter_combined.json", encoding="utf-8") as f:
        filter_data = json.load(f)
    
    all_data = generate_instruction_dataset_from_maintable(
        filter_json=filter_data,
        clothing_query=query_clothing,
        shoes_query=query_shoes
    )
    
    with open("../data/instruction_data_menstable.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
        
    print(f"{len(all_data)} 개수")
    # 총 6만개 가량 수집

if __name__ == "__main__":
    main()  
