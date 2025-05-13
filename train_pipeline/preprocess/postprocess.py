# preprocess/postprocess.py
import json

def clean_empty_lists(formatted_data):
    """
    후처리: 빈 문자열 리스트([""])를 빈 리스트([])로 변환
    
    Args:
        formatted_data: 포맷된 데이터셋 (리스트)
    
    Returns:
        후처리된 데이터셋
    """
    processed_data = []
    
    for sample in formatted_data:
        # 현재 샘플의 복사본 생성
        processed_sample = sample.copy()
        
        # assistant 메시지 찾기
        for message in processed_sample.get("messages", []):
            if message.get("role") == "assistant":
                for content_item in message.get("content", []):
                    if content_item.get("type") == "text":
                        try:
                            # JSON 문자열 파싱
                            response_json = json.loads(content_item["text"])
                            
                            # 빈 문자열 리스트 정리
                            for k, v in response_json.get("recommend", {}).items():
                                if isinstance(v, list) and all(item.strip() == "" for item in v):
                                    response_json["recommend"][k] = []
                            
                            # 다시 문자열로 저장
                            content_item["text"] = json.dumps(response_json, ensure_ascii=False)
                        except Exception as e:
                            print(f"⚠️ JSON 파싱 실패: {e}")
        
        processed_data.append(processed_sample)
    
    return processed_data