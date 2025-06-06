import os
import zipfile
from config.connect_storage import get_client
import logging

def download_and_extract(bucket, s3_key, zip_path, extract_path):
    s3 = get_client()

    logging.info("ZIP 다운로드 중...")
    with open(zip_path, "wb") as f:
        s3.download_fileobj(bucket, s3_key, f)
    logging.info("다운로드 완료!")

    logging.info("압축 해제 중...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    logging.info(f"압축 해제 완료 → {extract_path}/")

    os.remove(zip_path)
    logging.info("ZIP 파일 삭제 완료")
    
    return extract_path
