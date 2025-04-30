# handler.py
import base64
import io
import torch
from PIL import Image
from transformers import MllamaForConditionalGeneration, MllamaProcessor
import runpod

processor = MllamaProcessor.from_pretrained('UICHEOL-HWANG/MensCLUB-Fashion-Llama3.2-vision-5B')
model = MllamaForConditionalGeneration.from_pretrained(
    'UICHEOL-HWANG/MensCLUB-Fashion-Llama3.2-vision-5B',
    torch_dtype=torch.bfloat16,
    device_map='auto',
    use_safetensors=True
)

def handler(event):
    """RunPod Serverless 핸들러 함수"""
    input_data = event.get("input", {})
    
    # 이미지 처리
    if "image_base64" in input_data:
        image_data = base64.b64decode(input_data["image_base64"])
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
    elif "image_url" in input_data:
        # URL에서 이미지 다운로드 로직 필요
        return {"error": "image_url 지원 준비 중"}
    else:
        return {"error": "이미지가 제공되지 않았습니다"}
    
    # RAG 컨텍스트 추출 (외부에서 이미 유사도 계산 후 전달)
    rag_context = input_data.get("rag_context", "")
    
    # 모델 파라미터
    prompt = input_data.get("prompt", "이 패션 이미지에 대해 설명해주세요.")
    temperature = input_data.get("temperature", 0.7)
    max_tokens = input_data.get("max_tokens", 512)
    
    # RAG 컨텍스트를 프롬프트에 통합
    full_prompt = f"""
    다음 참고 가이드라인을 고려하여 이미지를 분석하고 스타일링 조언을 제공해주세요:

    {rag_context}

    원본 프롬프트: {prompt}
    """
    
    # 메시지 구성
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": full_prompt},
                {"type": "image", "image": image},
            ],
        }
    ]
    
    # 입력 텍스트 생성
    input_text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    
    # 입력 처리
    inputs = processor(
        text=input_text,
        images=image,
        add_special_tokens=False,
        return_tensors="pt",
    ).to(model.device)
    
    # 모델 추론
    output = model.generate(
        **inputs,
        max_new_tokens=max_tokens,
        temperature=temperature,
        eos_token_id=processor.tokenizer.eos_token_id,
        use_cache=True
    )
    
    # 결과 디코딩
    decoded = processor.tokenizer.decode(output[0], skip_special_tokens=True)
    
    return {"generated_text": decoded}

runpod.serverless.start({"handler": handler})