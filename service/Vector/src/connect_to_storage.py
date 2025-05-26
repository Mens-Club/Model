import boto3
import os
from dotenv import load_dotenv

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