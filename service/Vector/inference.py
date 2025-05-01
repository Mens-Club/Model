from src.PGVec_process import PGVecProcess
from src.encoding_elements import Encoding
import requests
import base64
import time
from dotenv import load_dotenv
import os 

load_dotenv()

def similar_distance(image_url, top_k=5):
    
    try:
        encoder = Encoding() 
        
        print(f"이미지 인코딩 중: {image_url}")
        
        embedding = encoder.encode_image(image_url=image_url)
        if embedding is None:
            print("이미지 인코딩 실패")
            return []
        
        db_processor = PGVecProcess()
        cursor = db_processor.connect()
        if cursor is None:
            print("데이터베이스 연결에 실패했습니다.")
            return []
        
        print("유사도 검색 중...")
        results = db_processor.similarity_search(embedding, cursor, top_k)
        
                # 데이터베이스 연결 종료
        db_processor.close()
        
        print(f"{len(results)}개의 유사한 아이템을 찾았습니다.")
        return results
        
    except Exception as e:
        
        print(f"유사 이미지 검색 중 오류 발생: {e}")

        return []

def image_to_base64(image_path):
    if image_path.startswith('http'):
        
        response = requests.get(image_path)
        response.raise_for_status()
        img_data = response.content
        
        
    else:
        # 로컬 파일 경로인 경우
        with open(image_path, "rb") as image_file:
            img_data = image_file.read()

    return base64.b64encode(img_data).decode('utf-8')    


def main(image_path, api_id, api_key, rag_context):
    base64_image = image_to_base64(image_path)
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    prompt = f"""
    당신은 패션 추천 전문가입니다. 아래 이미지를 보고 판단하여 적절한 코디를 JSON 형식으로 추천해주세요.

    다음 참고 가이드라인을 고려하여 코디를 제안해주세요:
    {rag_context}

    이미지를 참고하여 다음 형식에 맞게 추천해주세요:
    {{ "answer": ..., "recommend": {{ "상의": [...], "아우터": [...], "하의": [...], "신발": [...] }} }}

    *주의*:
    1) `answer` 문장에 반드시 '봄에 잘 어울리는 스타일입니다'처럼 계절을 언급할 것.
    2) `recommend` 내 각 카테고리별로 최소 3개의 아이템을 제시할 것.
    3) 이미지에 등장하는 주요 아이템은 해당 카테고리에서 제외하고, 나머지 카테고리는 모두 추천할 것.
    """
    payload = {
        'input': {
            "image_base64": base64_image,
            "rag_context": rag_context,
            "prompt": prompt,
            "temperature": 0.7,
            "max_tokens": 512
        }
    }
    
    url = f"https://api.runpod.ai/v2/{api_id}/run"
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()

        # 동기 요청의 경우 바로 결과가 반환됨
        if "output" in result:
            return result

        # 비동기 요청의 경우 작업 ID가 반환되고 결과를 폴링해야 함
        elif "id" in result:
            task_id = result["id"]
            status_url = f"https://api.runpod.ai/v2/{api_id}/status/{task_id}"

            while True:
                status_response = requests.get(status_url, headers=headers)
                status_data = status_response.json()

                if status_data["status"] == "COMPLETED":
                    return status_data
                elif status_data["status"] in ["FAILED", "CANCELLED"]:
                    return {"error": f"Task {status_data['status']}", "details": status_data}

                time.sleep(2)  # 폴링 간격
    else:
        return {"error": f"API 요청 실패: {response.status_code}", "details": response.text}
    
if __name__ == "__main__":
    api_key = os.getenv("RUNPOD_API")
    api_id = os.getenv("RUNPOD_ID")
    
    image_url = "https://kr.object.iwinv.kr/web-assets-prod/clothes/3689714.jpg"
    context = similar_distance(image_url=image_url)

    # 두 번째 결과의 필요한 필드만 추출
    filtered_result = {k: context[1][k] for k in ['season', 'sub_category', 'answer']} if len(context) > 1 else {}
    print(filtered_result)
    
    result = main(image_path=image_url,
         api_id=api_id,
         api_key=api_key,
         rag_context=filtered_result
         )["output"]["generated_text"]
    
    print(result)
    
    
    