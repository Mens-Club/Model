import json

def create_llama_vision_example(sample):
    input_info = sample["input"]
    output = sample["output"]
    
    # input_info에서 필요한 변수 추출
    sub_category = input_info.get("sub_category", "")
    season = input_info.get("season", "")
    
    # 1) instruction (text) 에 주의사항을 포함
    instruction = (
        "당신은 패션 추천 전문가입니다. 아래 이미지를 보고 판단하여 적절한 코디를 JSON 형식으로 추천해주세요.\n\n"
        "이미지를 참고하여 다음 형식에 맞춰 출력해주세요:\n"
        '{ "answer": "...", "recommend": { "상의": [...], "아우터": [...], "하의": [...], "신발": [...] } }\n\n'
        "주의사항:\n"
        f"1) \"answer\" 문장에 반드시 '해당 상품은 {sub_category}로 보이며 {season}에 잘 어울리는 스타일입니다'처럼 **계절**과 **아이템 카테고리**를 명시하세요.\n"
        "2) \"recommend\"의 각 카테고리에는 **최소 3개의 아이템**을 제시해야 합니다.\n"
        "3) 이미지에 나타난 **주요 아이템은 해당 카테고리에서 제외**하고, 나머지 카테고리에서는 추천을 제공합니다.\n"
        "4) \"recommend\" 항목에는 **season**, **sub_category**, **main_category** 등의 필드를 추가하지 마세요.\n"
        "5) 참고 가이드라인에서 특정 카테고리가 빈 리스트([])일 경우, **임의로 항목을 추가하지 말고 빈 리스트 그대로 출력**해야 합니다."
    )
    
    # 2) assistant 응답 (JSON 문자열)
    response_json = {
        "answer": output["answer"],
        "recommend": output["recommend"]
    }
    response_str = json.dumps(response_json, ensure_ascii=False)
    
    # 3) messages 리스트에 text+image 묶어서 반환
    return {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": instruction},
                    {"type": "image", "image": input_info["image"]},
                ]
            },
            {
                "role": "assistant",
                "content": [
                    {"type": "text", "text": response_str}
                ]
            }
        ]
    }
    