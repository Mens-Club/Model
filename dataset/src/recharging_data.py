import requests
import os
from PIL import Image
from io import BytesIO
import json
from datasets import Dataset
import time 
import random

def recharging_data(instruction_path, parquet_path=None, image_dir="./images"):
    with open(instruction_path, encoding="utf-8") as f:
        data = json.load(f)

    dataset = Dataset.from_list(data)

    os.makedirs(image_dir, exist_ok=True)
    updated_data = []

    for idx, row in enumerate(dataset):
        image_url = row["input"]["image"]
        try:
            response = requests.get(image_url, timeout=10)
            image = Image.open(BytesIO(response.content)).convert("RGB")

            filename = f"{idx:06}.jpg"
            save_path = os.path.join(image_dir, filename)
            image.save(save_path)

            row["input"]["image_path"] = save_path
            updated_data.append(row)

            # ✅ 랜덤 sleep 추가
            sleep_time = random.uniform(1, 4)
            print(f"🕒 Sleep {sleep_time:.2f}초 대기 중...")
            time.sleep(sleep_time)

        except Exception as e:
            print(f"❌ [{idx}] 이미지 다운로드 실패: {image_url} - {e}")

    # optional: parquet로 저장
    if parquet_path:
        final_ds = Dataset.from_list(updated_data)
        final_ds.to_parquet(parquet_path)
        print(f"✅ 저장 완료: {parquet_path}")

    return updated_data
    