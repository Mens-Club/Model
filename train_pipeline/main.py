from data.fetch_and_extract import download_and_extract
from data.datasets import load_dataset_from_disk

from preprocess.format_sample import create_llama_vision_example
from preprocess.postprocess import clean_empty_lists

from train.train_pipeline import load_model_and_tokenizer, train_model
from train.save_and_push import save_and_push 

from config.training_config import get_training_config
from config.metrics import push_to_gateway

import os 
import time
import mlflow 

# Bucket 
bucket=os.getenv("PREPROCESSING_BUCKET")
s3_key=os.getenv("HF_DATASET_ZIP_KEY")
zip_path=os.getenv("ZIP_PATH")
extract_path=os.getenv("EXTRACT_PATH")

# Model path
model_path=os.getenv("MAIN_MODEL")
base_model=os.getenv("BASE_MODEL")
base_token=os.getenv("HUGGINGFACE_TOKEN")

def main():
    with mlflow.start_run():
        mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))
        mlflow.set_experiment("model_training")
        
        # 버킷에 있는 데이터 다운로드 
        download_and_extract(bucket=bucket, 
                            s3_key=s3_key, 
                            zip_path=zip_path, 
                            extract_path=extract_path)
        
        # 데이터셋으로 그 path로 load 
        dataset = load_dataset_from_disk(extract_path)

        # Llama3.2-vision Task에 맞게 데이터 변형 
        formatted = [create_llama_vision_example(data) for data in dataset]
        
        # 샘플 데이터 확인 
        processed = clean_empty_lists(formatted)
        print(processed[0])
        model, tokenizer = load_model_and_tokenizer(base_model)
        
        # 훈련 시간 재기
        start = time.time()

        trainer = train_model(model=model, 
                            tokenizer=tokenizer, 
                            dataset=processed,
                            config=get_training_config())
        trainer.train()
        
        end = time.time()
        training_time = end - start
        final_loss = trainer.state.log_history[-1].get("loss", 0.0)
        
        # Processor는 Unsloth 상에서 정의하지 않기 때문에 None으로 넣어놓고 추후에 다시 부르는 로직으로 변환
        save_and_push(
            model=model,
            tokenizer=tokenizer,
            processor=None,  # processor는 Unsloth에서 사용 안 하므로 생략
            base_model=base_model,
            save_method="merged_16bit",
            repo=model_path,
            token=base_token
        )
        components = {
            "model": model,
            "tokenizer": tokenizer,
        }
        
        mlflow.transformers.log_model(
            transformers_model=components,
            artifact_path="outputs",
            registered_model_name="llama3.2-vision-finetuned"
        )
        push_to_gateway(loss_value=final_loss, training_time=training_time)
        
if __name__ == "__main__":
    main()
    

