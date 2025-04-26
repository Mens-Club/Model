# Modules 
from storage.connect_storage import upload_to_s3
from preprocessing.filter_merger import merge_season_filters
from preprocessing.filter_util import get_season_category_map

import os 
from dotenv import load_dotenv 

load_dotenv()

def main():

    clothes = get_season_category_map(
        table_name="mens_table_refine",
        category_column="main_category",
        s3_bucket=os.getenv("PREPROCESSING_BUCKET"),
        s3_key=os.getenv("CLOTHES_KEY")
    )
    
    shoes = get_season_category_map(
        table_name="shoes_refine",
        fixed_category="신발",
        s3_bucket=os.getenv("PREPROCESSING_BUCKET"),
        s3_key=os.getenv("SHOES_KEY")
    )
    
    merged = merge_season_filters(clothes, shoes) # 병합 
    
    # 병합 된 내용도 버킷에 저장
    upload_to_s3(
        data=merged,
        bucket_name=os.getenv("PREPROCESSING_BUCKET"),
        s3_key=os.getenv("COMBINED")
    )
    
    print("전처리 업로드 완료")

if __name__ == "__main__":
    main()