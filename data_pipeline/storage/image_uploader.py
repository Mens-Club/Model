from PIL import Image
from io import BytesIO
import requests

from .connect_storage import upload_to_s3
from typing import List
import pandas as pd


# 추후 리팩토링 예정
def upload_to_image(data: pd.DataFrame, bucket_name: str, folder: str) -> List[str]:
    """
    DataFrame의 thumbnail_url을 기반으로 이미지를 S3에 업로드
    
    Args:
        data (pd.DataFrame): 'thumbnail_url' 열이 포함된 데이터프레임
        bucket_name (str): 업로드할 S3 버킷 이름
        folder (str): S3 내부 경로(prefix)

    Returns:
        List[str]: 업로드된 이미지의 S3 키 목록
    """
    uploaded_keys = []

    for idx, row in data.iterrows():
        try:
            image_url = row["thumbnail_url"]
            response = requests.get(image_url, timeout=10)
            image = Image.open(BytesIO(response.content)).convert("RGB")

            # 고유 키 생성
            image_id = image_url.split("/")[6]
            s3_key = f"{folder.rstrip('/')}/{image_id}.jpg"
            
            buffer = BytesIO()
            image.save(buffer, format="JPEG")
            buffer.seek(0)

            upload_to_s3(
                data=buffer,
                bucket_name=bucket_name,
                s3_key=s3_key,
                content_type="image/jpeg"
            )

            print(f"✅ [{idx}] 업로드 성공: s3://{bucket_name}/{s3_key}")
            uploaded_keys.append(s3_key)

        except Exception as e:
            print(f"❌ [{idx}] 업로드 실패: {e}")

    return uploaded_keys
