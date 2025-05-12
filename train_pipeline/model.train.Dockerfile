FROM runpod/pytorch:2.2.0-py3.10-cuda12.1.1-devel-ubuntu22.04

RUN apt-get update && apt-get install -y \
    git wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /train

RUN pip install --no-cache-dir \
    transformers \
    accelerate \
    pillow \
    python-multipart \
    requests \
    huggingface-hub \
    runpod \
    boto3 \
    datasets \
    trl \
    unsloth 

COPY . /train

CMD ["python", "main.py"]