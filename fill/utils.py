import re

def extract_clothing_name(answer: str) -> str:
    match = re.search(r'이 옷은 (.+?)입니다', answer)
    return match.group(1) if match else None