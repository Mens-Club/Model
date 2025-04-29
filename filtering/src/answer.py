import json

def split_answer_recommend(text: str):
    cleaned_text = text.strip().replace('\r\n', '\n').replace('\r', '\n')
    print(f"Cleaned input text: {cleaned_text!r}")
    #텍스트를 JSON으로 파싱
    try:
        data = json.loads(cleaned_text)
        answer = data.get("answer", "")
        recommend = data.get("recommend", {})
        print(f"Parsed answer: {answer}")  # Debug: Print parsed answer
        print(f"Parsed recommend: {recommend}")  # Debug: Print parsed recommend
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")  # Debug: Print JSON error
        print(f"Error context: {cleaned_text[:50]!r}...")  # Debug: Show start of problematic text
        answer = ""
        recommend = {}

    # answer에서 계절 추출
    seasons = ["봄", "여름", "가을", "겨울"]
    season = ""
    for s in seasons:
        if s in answer:
            season = s
            break
    print(f"Extracted season: {season}")  # Debug: Print extracted season

    return {"answer": answer, "season": season, "recommend": recommend}