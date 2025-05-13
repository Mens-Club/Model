import runpod
import os
import traceback
from dotenv import load_dotenv

load_dotenv()

# RunPod API 키 설정
api_key = os.getenv("RUNPOD_API")

# GPU 및 이미지 설정
gpu_id = "NVIDIA RTX 6000 Ada Generation"  
image_path = os.getenv("GCP_IMAGE_PATH")
template_id = os.getenv("RUNPOD_TEMPLATE_ID")

runpod.api_key = api_key

# 환경 변수 설정
env = {
    "HUGGINGFACE_TOKEN": os.getenv("HUGGINGFACE_TOKEN"),
    "MAIN_MODEL": os.getenv("MAIN_MODEL"),
    "BASE_MODEL": os.getenv("BASE_MODEL"),
    "EXTRACT_PATH": os.getenv("EXTRACT_PATH"),
    "ZIP_PATH": os.getenv("ZIP_PATH"),
    "HF_DATASET_ZIP_KEY": os.getenv("HF_DATASET_ZIP_KEY"),
    "PREPROCESSING_BUCKET": os.getenv("PREPROCESSING_BUCKET"),
    "SERVICE_NAME": os.getenv("SERVICE_NAME"),
    "ENDPOINT_URL": os.getenv("ENDPOINT_URL"),
    "REGION_NAME": os.getenv("REGION_NAME"),
    "ACCESS_KEY": os.getenv("ACCESS_KEY"),
    "SECRET_KEY": os.getenv("SECRET_KEY")
}

# Pod 생성
try:
    deployment = runpod.create_pod(
        name="mensclub-trainer",
        image_name=image_path,
        template_id=template_id, #이미 개발환경에서 세팅 완료된 id 매핑
        gpu_type_id=gpu_id,
        cloud_type="SECURE",
        container_disk_in_gb=100,
        volume_in_gb=100,
        env=env
    )
    print("Pod 생성 완료:", deployment)
except Exception as e:
    print(f"Pod 생성 실패: {e}")
    traceback.print_exc()

