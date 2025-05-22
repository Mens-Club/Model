import shutil
import boto3
import os
from dotenv import load_dotenv
from storage.connect_storage import get_client
from datasets import load_from_disk
import zipfile
import logging

load_dotenv()

def zip_dataset_dir(dir_path: str) -> str:
    """
    디렉토리를 zip 파일로 압축
    """
    zip_path = shutil.make_archive(dir_path, 'zip', dir_path)
    logging.info(f"압축 완료: {zip_path}")
    return zip_path

def upload_zip_to_s3(zip_path: str, bucket: str, s3_key: str):
    """
    zip 파일을 S3에 업로드
    """
    s3 = get_client()
    with open(zip_path, "rb") as f:
        s3.upload_fileobj(f, bucket, s3_key)
    logging.info(f"S3 업로드 완료: s3://{bucket}/{s3_key}")

def compress_and_upload_fashion_dataset():
    folder_path = "fashion_instruction_dataset"
    zip_path = zip_dataset_dir(folder_path)

    bucket = os.getenv("PREPROCESSING_BUCKET")        
    s3_key = os.getenv("HF_DATASET_ZIP_KEY")             
    
    if not bucket or not s3_key:
        raise ValueError("S3 버킷명 또는 경로가 설정되지 않았습니다.")

    upload_zip_to_s3(zip_path, bucket, s3_key)
    

def download_zip_from_s3(bucket: str, s3_key: str, local_path: str):
    s3 = get_client()
    with open(local_path, "wb") as f:
        s3.download_fileobj(bucket, s3_key, f)
    logging.info(f"S3 다운로드 완료: {local_path}")

def unzip_dataset(zip_path: str, extract_dir: str):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    logging.info(f"압축 해제 완료: {extract_dir}")

def load_hf_dataset(dataset_dir: str):
    dataset = load_from_disk(dataset_dir)
    logging.info(f"로딩된 샘플 수: {len(dataset)}")
    return dataset

def main():
    bucket = "model-training-data"
    s3_key = "train_arrow/fashion_instruction_dataset.zip"
    zip_path = "tmp/fashion_instruction_dataset.zip"
    extract_dir = "."

    # Step 1. S3에서 zip 다운로드
    download_zip_from_s3(bucket, s3_key, zip_path)

    # Step 2. 압축 해제
    unzip_dataset(zip_path, extract_dir)

    # Step 3. 데이터셋 로드
    dataset = load_hf_dataset("fashion_instruction_dataset")

    # 샘플 확인
    logging.info("첫 샘플:")
    logging.info(len(dataset))

if __name__ == "__main__":
    main()