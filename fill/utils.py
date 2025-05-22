import re

def extract_clothing_name(answer: str) -> str:
    match = re.search(r'상품은 (.+?)로 보이며', answer)
    return match.group(1) if match else None