from src.connect_to_storage import get_client
from src.encoding_elements import Encoding 
from src.PGVec_process import PGVecProcess
import json 
from botocore.exceptions import ClientError
import os 
from tqdm import tqdm

def get_instruction_data(bucket_name, key):
    """S3에서 instruction 데이터를 가져옴"""
    
    try:
    
        s3_client = get_client()
        response = s3_client.get_object(Bucket=bucket_name, Key=key)
        instruction_data = json.loads(response['Body'].read().decode('utf-8'))
    
        return instruction_data
    
    except ClientError as e:
    
        print(f"S3에서 데이터를 가져오는 중 오류 발생: {e}")
        
        return None

def process_instruction_data(instruction_data, encoder):
    """Instruction 데이터를 처리하고 임베딩을 생성"""
    processed_data = []
    
    print(f"총 {len(instruction_data)}개 항목 처리 시작...")
    
    # tqdm을 사용하여 진행 상황 표시
    for i, item in enumerate(tqdm(instruction_data)):
        try:
            # 주기적으로 진행 상황 출력 (예: 100개마다)
            if i > 0 and i % 100 == 0:
                print(f"{i}/{len(instruction_data)} 항목 처리 완료")
                
            # 이미지 URL 가져오기
            image_url = item['input'].get('image', '')
            if not image_url:
                print("이미지 URL이 없습니다. 건너뜁니다.")
                continue
            
            # 이미지 인코딩
            embedding = encoder.encode_image(image_url)
            if embedding is None:
                print(f"이미지 인코딩 실패: {image_url}")
                continue
            
            # 처리된 데이터에 임베딩 추가
            item['embedding'] = embedding
            processed_data.append(item)
            
        except Exception as e:
            print(f"데이터 처리 중 오류 발생: {e}")
            continue
    
    return processed_data

def main():
    
    try:
        
        bucket = os.getenv("PREPROCESSING_BUCKET")
        instruction_key = os.getenv("TRAIN_JSON")
        
        print("버킷에서 데이터 수신중..")
        
        instruction_data = get_instruction_data(bucket_name=bucket, key=instruction_key)
        if not instruction_data:
            print("Instruction 데이터가 없습니다.")
            return 
        
        
        print(f"총 {len(instruction_data)}개의 데이터 수신 완료")
        
        # CLIP 인코더 
        
        print("CLIP 모델 초기화 중")
        
        encoder = Encoding()
        print("CLIP 초기화 완")
        
        print("데이터 처리 및 임베딩 생성 중...")
        processed_data = process_instruction_data(instruction_data=instruction_data, encoder=encoder)

        print("데이터베이스 연결중...")
        db_processor = PGVecProcess()
        cursor = db_processor.connect()
        if cursor is None:
            print("데이터베이스 연결에 실패했습니다.")
            return
        
        success_count = 0
        print("데이터베이스 저장중...")
        for item in tqdm(processed_data):
            if db_processor.injection(item, cursor):
                success_count += 1
        
        print(f"총 {len(processed_data)}개 중 {success_count}개 데이터가 성공적으로 저장되었습니다.")
        
        # 데이터베이스 연결 종료
        db_processor.close()
        print("처리가 완료되었습니다.")
        
    except Exception as e:
        print(f"실행 중 오류 발생: {e}")

if __name__ == "__main__":
    main()