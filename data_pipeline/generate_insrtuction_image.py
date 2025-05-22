import os
import json
import shutil
import requests
from PIL import Image as PILImage
from io import BytesIO
from tqdm import tqdm
from dotenv import load_dotenv
from datasets import Dataset, Image, load_from_disk, concatenate_datasets
from storage.connect_storage import get_client

import logging

load_dotenv()

s3_client = get_client()
bucket = os.getenv("PREPROCESSING_BUCKET")          
s3_key = os.getenv("HF_DATASET_ZIP_KEY")             


def download_instruction_json(bucket: str, s3_key: str, local_path: str):
    s3_client.download_file(bucket, s3_key, local_path)
    with open(local_path, "r", encoding="utf-8") as f:
        return json.load(f)

def fetch_image(url: str) -> PILImage.Image:
    response = requests.get(url, timeout=5)
    return PILImage.open(BytesIO(response.content)).convert("RGB")

def save_dataset_chunk(samples: list, start_idx: int, chunk_size: int):
    images, instructions, seasons, categories, sub_categories, colors, answers, recommends = [], [], [], [], [], [], [], []

    for sample in tqdm(samples, desc=f"이미지 로딩 {start_idx}~{start_idx + len(samples)}"):
        try:
            image = fetch_image(sample["input"]["image"])
            images.append(image)
            instructions.append(sample["instruction"])
            seasons.append(sample["input"]["season"])
            categories.append(sample["input"]["category"])
            sub_categories.append(sample["input"]["sub_category"])
            colors.append(sample["input"]["color"])
            answers.append(sample["output"]["answer"])
            recommends.append(sample["output"]["recommend"])
        except Exception as e:
            logging.info(f"실패: {sample['input']['image']} - {e}")

    if len(images) == 0:
        logging.info(f" 이미지 없음: {start_idx}")
        return

    dataset = Dataset.from_dict({
        "image": images,
        "instruction": instructions,
        "season": seasons,
        "category": categories,
        "sub_category": sub_categories,
        "color": colors,
        "answer": answers,
        "recommend": recommends,
    }).cast_column("image", Image())

    save_path = f"fashion_dataset_part_{start_idx}"
    dataset.save_to_disk(save_path)
    logging.info(f"저장 완료: {save_path}")


def chunked(data, size):
    for i in range(0, len(data), size):
        yield data[i:i + size], i


def save_all_chunks(samples: list, chunk_size=1000):
    for chunk, idx in chunked(samples, chunk_size):
        save_dataset_chunk(chunk, idx, chunk_size)

def merge_all_chunks(output_path: str, total: int, chunk_size: int):
    paths = [f"fashion_dataset_part_{i}" for i in range(0, total, chunk_size) if os.path.exists(f"fashion_dataset_part_{i}")]
    datasets = [load_from_disk(path) for path in paths]

    merged = concatenate_datasets(datasets)
    merged.save_to_disk(output_path)
    logging.info(f"전체 데이터셋 저장 완료: {output_path}")

def normalize_recommend_field(r):
    def safe(v):
        return v if v and isinstance(v, list) else [""]
    return {
        "상의": safe(r.get("상의")),
        "아우터": safe(r.get("아우터")),
        "하의": safe(r.get("하의")),
        "신발": safe(r.get("신발")),
    }
    
def fix_recommend_and_save(part_path):
    ds = load_from_disk(part_path)

    # normalize recommend field
    def fix(example):
        example["recommend"] = normalize_recommend_field(example["recommend"])
        return example

    ds_fixed = ds.map(fix)
    ds_fixed.save_to_disk(part_path)
    logging.info(f"✅ recommend 필드 수정 완료: {part_path}")


def normalize_recommend_field(r):
    def safe(v):
        return v if v and isinstance(v, list) else [""]
    return {
        "상의": safe(r.get("상의")),
        "아우터": safe(r.get("아우터")),
        "하의": safe(r.get("하의")),
        "신발": safe(r.get("신발")),
    }

def fix_recommend_and_save(part_path):
    ds = load_from_disk(part_path)

    def fix(example):
        example["recommend"] = normalize_recommend_field(example["recommend"])
        return example

    # 1. 임시 디렉토리에 저장
    tmp_path = part_path + "_tmp"
    ds_fixed = ds.map(fix)
    ds_fixed.save_to_disk(tmp_path)

    # 2. 기존 디렉토리 삭제 후 덮어쓰기
    shutil.rmtree(part_path)
    shutil.move(tmp_path, part_path)

    logging.info(f"recommend 정제 완료: {part_path}")


def merge_all_parts(output_path: str, total: int, chunk_size: int):
    paths = [
        f"fashion_dataset_part_{i}" 
        for i in range(0, total, chunk_size) 
        if os.path.exists(f"fashion_dataset_part_{i}")
    ]
    datasets = [load_from_disk(path) for path in paths]

    full_dataset = concatenate_datasets(datasets)
    full_dataset.save_to_disk(output_path)
    logging.info(f"🎉 전체 데이터셋 병합 완료: {output_path}")

def main():
    # 환경변수에서 읽기
    bucket = os.getenv("PREPROCESSING_BUCKET")  
    s3_key = os.getenv("TRAIN_JSON")           
    json_local = "instruction_dataset.json"

    # 1. JSON 다운로드
    logging.info(" instruction JSON 다운로드 중...")
    samples = download_instruction_json(bucket, s3_key, json_local)
    logging.info(f"총 샘플 수: {len(samples)}")

    # 2. 분할 저장
    save_all_chunks(samples, chunk_size=1000)

    # 3. 전체 병합
    merge_all_chunks("fashion_dataset_full", total=len(samples), chunk_size=1000)

def zip_and_upload(local_dir: str, zip_path: str, bucket: str, s3_key: str):
    shutil.make_archive(zip_path, 'zip', local_dir)
    logging.info(f"압축 완료: {zip_path}.zip")

    with open(f"{zip_path}.zip", "rb") as f:
        s3_client.upload_fileobj(f, bucket, s3_key)
    logging.info(f"S3 업로드 완료: s3://{bucket}/{s3_key}")


if __name__ == "__main__":
    full_path = "fashion_dataset_full"
    zip_base = "fashion_dataset_full"  
    zip_and_upload(full_path, zip_base, bucket, s3_key)