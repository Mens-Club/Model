import base64
import io
import torch
from PIL import Image
import clip
import runpod

# 모델 로딩
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)
model.eval()

def handler(event):
    input_data = event.get("input", {})

    if "image_base64" not in input_data:
        return {"error": "image_base64 필드가 필요합니다."}
    
    try:
        # 이미지 디코딩
        image_bytes = base64.b64decode(input_data["image_base64"])
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # 전처리 및 인코딩
        image_input = preprocess(image).unsqueeze(0).to(device)
        with torch.no_grad():
            features = model.encode_image(image_input)

        # 벡터 반환
        return {
            "embedding": features.cpu().numpy().flatten().tolist()
        }

    except Exception as e:
        return {"error": str(e)}

runpod.serverless.start({"handler": handler})
