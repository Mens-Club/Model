FROM runpod/pytorch:2.2.0-py3.10-cuda12.1.1-devel-ubuntu22.04

# 기본 패키지 설치
RUN apt-get update && apt-get install -y \
    git wget \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app  

# 필요한 패키지 설치
RUN pip install --no-cache-dir \
    transformers \
    accelerate \
    pillow \
    python-multipart \
    requests \
    huggingface-hub \
    runpod

# 서버 코드 복사
COPY ./test.py /app/

# 모델 캐싱을 위한 환경변수 설정
ENV HF_HOME=/app/hf_cache

# 포트 노출
EXPOSE 8000

# 서버 실행
CMD ["python", "test.py"]