from fastapi import FastAPI
from pydantic import BaseModel
import json
import random
from src.answer import split_answer_recommend
from src.filter import filter_items, generate_outfit_combinations

app = FastAPI()

class OutfitRequest(BaseModel):
    image_id: str

@app.post("/generate-outfit")
def generate_outfit(request: OutfitRequest):
    # 하드코딩된 테스트 텍스트
    test_text = '{"answer": "이 상품은 데님 팬츠로 보이며 해당 상품은 겨울에 맞는 상품입니다. 그에 맞는 상품들을 추천드릴게요.", "recommend": {"상의": ["긴소매 티셔츠", "셔츠&블라우스 - 긴소매", "긴소매 티셔츠"], "아우터": ["롱패딩&헤비 아우터", "겨울 싱글 코트", "무스탕&퍼"], "하의": [], "신발": ["모카신", "패션스니커즈화", "캔버스/단화"]}}'
    # answer.py로 텍스트 파싱
    result = split_answer_recommend(test_text)
    answer = result.get("answer", "")
    season = result.get("season", "")
    recommend = result.get("recommend", "{}")

    # Debug: Print values before filtering
    print(f"Main - Answer: {answer}")
    print(f"Main - Season: {season}")
    print(f"Main - Recommend: {recommend}")

    # style 랜덤 선택
    style = random.choice(["캐주얼", "미니멀"])

    # filter.py로 조합 생성
    filtered = filter_items(recommend, style, season)
    combos = generate_outfit_combinations(recommend, filtered)

    return {"answer": answer, "combinations": combos}

@app.get("/health")
def health_check():
    return {"status": "ok"}