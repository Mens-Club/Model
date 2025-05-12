import runpod 
import os 

# RunPod API 키
api_key = os.getenv("RUNPOD_API_KEY")

# 생성이미지 
image_path = os.getenv("GCP_IAMGE_PATH")

deployment = runpod.create_pod(
    name="mensclub-trainer",
    image=image_path,
    gpu_type_id="NVIDIA-RTX-6000-ADA",   
    cloud_type="SECURE",                
    container_disk_in_gb=100,
    volume_in_gb=100,
    ports=["8000"],
    env={"HUGGINGFACE_TOKEN": os.getenv("HUGGINGFACE_TOKEN")},
)

print("Pod 생성 완료:", deployment)
