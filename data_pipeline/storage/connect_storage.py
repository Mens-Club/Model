import boto3
import json
import os
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import logging

load_dotenv()


def get_client():
    
    return boto3.client(
        service_name=os.getenv("SERVICE_NAME"),
        endpoint_url=os.getenv("ENDPOINT_URL"),
        region_name=os.getenv("REGION_NAME"),
        aws_access_key_id=os.getenv("ACCESS_KEY"),
        aws_secret_access_key=os.getenv("SECRET_KEY"),
        config=boto3.session.Config(signature_version="s3v4")
    )

def upload_to_s3(data, bucket_name, s3_key, content_type="application/json"):
    
    if content_type == "application/json" and not isinstance(data, str):
        data = json.dumps(data, ensure_ascii=False, indent=2)

    s3 = get_client()
    
    try:
        s3.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=data,
            ContentType=content_type
        )
        logging.info(f"업로드 완료: s3://{bucket_name}/{s3_key}")
    except ClientError as e:
        logging.info(f"업로드 실패: {e}")

def load_json_from_s3(bucket_name: str, s3_key: str) -> dict:
    
    # S3 클라이언트 생성
    
    s3 = get_client()

    try:
        
        response = s3.get_object(Bucket=bucket_name, Key=s3_key)
        content = response['Body'].read().decode('utf-8')
        data = json.loads(content)
        
        logging.info(f"S3 JSON 로드 완료: s3://{bucket_name}/{s3_key}")
        
        return data
    
    except ClientError as e:
        
        logging.info(f"S3에서 JSON 로드 실패: {e}")
        
        return {}