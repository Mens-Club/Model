# Model Feature

> AI 기반 패션 추천 모델의 핵심 기능 및 훈련 파이프라인

## Architecture Overview

본 프로젝트는 **CLIP 기반 멀티모달 AI 모델**을 활용한 패션 추천 시스템으로, instruction 데이터 생성부터 모델 훈련까지 `Operation` 리포지토리에서 자동화하기 위한 초석 같은 리포지토리라고 보시면 되겠습니다.

### Key Features

- **CLIP 모델**: 이미지-텍스트 멀티모달 임베딩 생성
- **Instruction 데이터**: 고품질 학습 데이터 자동 생성
- **Docker 기반 훈련**: RunPod를 활용한 클라우드 GPU 훈련
- **Vector Search**: PostgreSQL + pgvector 기반 유사도 검색

## Project Structure

```bash
project_root/
├── crawler/                     # 데이터 수집
│   └── main.py                 # 패션 데이터 크롤링
├── data_pipeline/              # 데이터 처리 파이프라인
│   ├── generate_instruction_image.py    # 이미지 instruction 생성
│   ├── generate_instruction.py          # 텍스트 instruction 생성
│   ├── insert.py                       # 데이터베이스 삽입
│   ├── preprocessing_main.py           # 전처리 메인
│   ├── database/               # 데이터베이스 연결
│   │   ├── connect_to_database.py
│   │   └── __init__.py
│   ├── instruction/            # Instruction 데이터 생성
│   │   ├── instruction_generator.py    # 핵심 instruction 생성기
│   │   ├── parquet_converter.py       # 데이터 포맷 변환
│   │   └── __init__.py
│   ├── preprocessing/          # 데이터 전처리
│   │   ├── filter_merger.py           # 필터 병합
│   │   ├── filter_util.py             # 필터 유틸리티
│   │   └── __init__.py
│   └── storage/               # 클라우드 스토리지
│       ├── connect_storage.py         # 스토리지 연결
│       ├── image_uploader.py          # 이미지 업로드
│       └── __init__.py
├── service/                   # 마이크로서비스
│   ├── CLIP/                 # CLIP 임베딩 서비스
│   │   └── main.py          # CLIP 모델 API
│   ├── Mllamavision/        # 비전 언어 모델
│   │   ├── main.py         # 메인 추론 서비스
│   │   └── RAG_main.py     # RAG 기반 추천
│   └── Vector/             # 벡터 검색 서비스
│       ├── main.py        # 벡터 검색 API
│       └── src/
│           ├── connect_to_storage.py  # 스토리지 연결
│           ├── encoding_elements.py  # 임베딩 인코딩
│           └── PGVec_process.py     # PostgreSQL 벡터 처리
└── train_pipeline/           # 모델 훈련 파이프라인
    ├── main.py              # 훈련 메인 스크립트
    ├── runpod_training.py   # RunPod 클라우드 훈련
    ├── config/              # 훈련 설정
    │   ├── connect_storage.py      # 스토리지 설정
    │   ├── metrics.py             # 평가 메트릭
    │   ├── training_config.py     # 훈련 하이퍼파라미터
    │   └── __init__.py
    ├── data/               # 데이터 로딩
    │   ├── datasets.py            # 데이터셋 클래스
    │   ├── fetch_and_extract.py   # 데이터 다운로드
    │   └── __init__.py
    ├── preprocess/         # 전처리
    │   ├── format_sample.py       # 샘플 포맷팅
    │   ├── postprocess.py         # 후처리
    │   └── __init__.py
    └── train/             # 모델 훈련
        ├── save_and_push.py       # 모델 저장 및 배포
        ├── train_pipeline.py      # 훈련 파이프라인
        └── __init__.py
```

## Core Components

### 1. CLIP 모델 활용

**CLIP(Contrastive Language-Image Pre-training)** 모델을 핵심으로 사용하여 이미지와 텍스트를 동일한 임베딩 공간에 매핑합니다.

**주요 기능:**
- 패션 아이템 이미지 임베딩 생성
- 스타일 설명 텍스트 임베딩 생성  
- 멀티모달 유사도 계산

### 2. Instruction 데이터 생성

**고품질 학습 데이터**를 자동으로 생성하는 파이프라인을 구축했습니다.

**특징:**
- 계절별, 카테고리별 맞춤 instruction
- 이미지-텍스트 쌍 데이터 자동 생성
- 다양한 스타일링 시나리오 커버

### 3. Docker 기반 RunPod 훈련

**Docker 이미지로 패키징**하여 RunPod 클라우드 GPU에서 모델을 훈련합니다.

**RunPod 훈련 프로세스:**
1. 데이터 다운로드 및 전처리
2. 모델 초기화 및 설정
3. 분산 훈련 실행
4. 모델 저장 및 클라우드 업로드

### 4. Vector Search with PostgreSQL

**pgvector** 확장을 사용한 고성능 벡터 검색을 구현했습니다.

**주요 기능:**
- 임베딩 벡터 저장 및 인덱싱
- 코사인 유사도 기반 아이템 검색
- 실시간 추천 결과 반환

## Training Pipeline

### 1. 데이터 준비

크롤링된 패션 데이터를 전처리하고 데이터베이스에 저장합니다.

### 2. Instruction 데이터 생성

패션 아이템과 스타일링 규칙을 기반으로 instruction 데이터를 자동 생성합니다.

### 3. Docker 이미지 빌드 및 RunPod 배포

훈련 환경을 Docker로 패키징하고 RunPod 클라우드에서 GPU 훈련을 실행합니다.

### 4. 모델 서빙

훈련된 모델을 마이크로서비스 형태로 배포하여 실시간 추천 서비스를 제공합니다.

## Model Performance

### Training Metrics

- **Dataset Size**: 30,000+ 패션 아이템
- **Instruction Data**: 42,000+ instruction 쌍
- **Training Time**: RunPod A100에서 약 30분(`Unsloth`로 훈련하여 훈련시간 절약)
- **Model Size**: 5B 파라미터 (LLaMA 기반)

## Key Highlights

### CLIP 활용의 핵심 가치

1. **멀티모달 이해**: 이미지와 텍스트를 동일한 임베딩 공간에서 처리
2. **Zero-shot 추론**: 새로운 패션 카테고리도 추가 훈련 없이 처리 가능
3. **의미적 유사도**: 시각적 유사성과 의미적 유사성을 동시에 고려

### Instruction 데이터의 중요성

1. **도메인 특화**: 패션 전문 용어와 스타일링 규칙 학습
2. **자동 생성**: 수작업 없이 대규모 고품질 데이터 확보
3. **다양성 확보**: 다양한 시나리오와 스타일 조합 커버

### RunPod 클라우드 훈련의 장점

1. **비용 효율성**: 필요할 때만 GPU 사용, 유연한 스케일링
2. **Docker 표준화**: 환경 일관성 보장, 재현 가능한 훈련
3. **자동화**: 완전히 자동화된 훈련 파이프라인
4. **고성능**: A100 GPU를 활용한 빠른 훈련 속도

## Technical Architecture

### Data Flow

1. **크롤링**: 패션 아이템 데이터 수집
2. **전처리**: 데이터 정제 및 필터링
3. **Instruction 생성**: 학습용 instruction 데이터 자동 생성
4. **임베딩**: CLIP을 통한 멀티모달 임베딩 생성
5. **벡터 저장**: PostgreSQL pgvector에 임베딩 저장
6. **모델 훈련**: RunPod에서 Docker 기반 훈련
7. **서빙**: 마이크로서비스 형태로 모델 배포

### Service Architecture

- **CLIP Service**: 이미지/텍스트 임베딩 생성
- **Vector Service**: 유사도 검색 및 추천
- **Mllamavision Service**: 비전-언어 모델 추론
- **RAG Service**: 검색 증강 생성 기반 추천

## Deployment

### Local Development

모든 서비스는 Docker Compose로 로컬에서 실행 가능합니다.

### Production Deployment

- **Training**: RunPod 클라우드 GPU
- **Storage**: Custom S3(iwinv)
- **Database**: PGVector

## Contributing

모델 개선이나 새로운 기능 추가에 관심이 있으시면 언제든 기여해주세요.