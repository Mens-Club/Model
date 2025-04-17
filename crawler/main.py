import json
import time 
import pandas as pd
from dotenv import load_dotenv
import os 
import random
import requests
import argparse

from src.combination import generate_combine
from src.generate_url import generate_url



load_dotenv()

# 각 요소들 파싱하기 

with (open("config/param_map.json", encoding="utf-8") as f): param_map = json.load(f)
with (open("config/filter.json", encoding="utf-8") as f):  filters = json.load(f)
with (open("config/categories.json", encoding="utf-8") as f): categories = json.load(f)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json, text/plain, */*",
    "Referer": os.getenv("Referer"),
    "Origin": os.getenv("Origin")
}

def main(output_path):

    results = []

    for category in categories:  # ✅ 복수 카테고리 지원
        category_id = category["id"]
        category_name = category["name"]
        
        for combo in generate_combine(filters):
            url = generate_url(combo, filters, param_map, category_id)

            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                products = response.json().get("data", {}).get("list", [])

                for item in products:
                    enriched = {**item, **combo, "category": category_id, "category_name" : category_name}
                    results.append(enriched)

                print(f"✅ {combo} / {category} → {len(products)}건 수집")

            except Exception as e:
                print(f"❌ 실패: {combo} / {category} → {e}")

            time.sleep(random.uniform(1.0, 3.0))

    # 저장
    df = pd.DataFrame(results)
    df.to_csv(output_path, index=False, encoding="utf-8-sig") # 데님팬츠 부터

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output_path",
        type=str,
        default="../output/slacks_pants_data.csv",
        help="저장할 CSV 파일 경로를 입력하세요 (예: ../output/denim_pants_data.csv)"
    )
    args = parser.parse_args()
    main(args.output_path)