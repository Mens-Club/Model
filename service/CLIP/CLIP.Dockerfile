FROM runpod/pytorch:2.2.0-py3.10-cuda12.1.1-devel-ubuntu22.04

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    git wget \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정 
WORKDIR /app

# 필요한 Python 패키지 설치
RUN pip install --no-cache-dir \
    openai-clip \
    torch \
    torchvision \ 
    numpy \
    Pillow \
    requests \
    runpod

# 코드 복사
COPY ./main.py /app/

EXPOSE 8000

# 실행
CMD ["python", "main.py"]
