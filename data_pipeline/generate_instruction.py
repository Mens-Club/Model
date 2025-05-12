from storage.connect_storage import (load_json_from_s3,
                                     upload_to_s3)

from instruction.instruction_generator import (
    generate_instruction_dataset_from_maintable)

from instruction.parquet_converter import convert_dataset

import os 
from dotenv import load_dotenv 

load_dotenv()

# Search Query 

# 옷 쿼리
query_clothing = """
SELECT season, main_category, sub_category, color, thumbnail_url, s3_path
FROM mens_table_refine;
"""

# 신발 쿼리
query_shoes = """
SELECT season, sub_category, color, thumbnail_url, s3_path
FROM shoes_refine;
"""
    

def main():
    
    data = load_json_from_s3(bucket_name=os.getenv("PREPROCESSING_BUCKET"), 
                    s3_key=os.getenv("COMBINED"))
    
    all_data = generate_instruction_dataset_from_maintable(
        filter_json=data,
        clothing_query=query_clothing,
        shoes_query=query_shoes
    )
    
    upload_to_s3(
        data=all_data,
        bucket_name=os.getenv("PREPROCESSING_BUCKET"),
        s3_key=os.getenv("TRAIN_JSON")
    )
    
    datasets = convert_dataset(all_data)
    upload_to_s3(
        data=datasets,       
        bucket_name=os.getenv("PREPROCESSING_BUCKET"),
        content_type="application/octet-stream", 
        s3_key=os.getenv("TRAIN_PARQUET")
    )
    
    print(f"총 {len(all_data)}개 데이터 저장 완료")
    
    
if __name__ == "__main__":

    
    main()