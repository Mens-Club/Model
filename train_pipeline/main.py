from data.fetch_and_extract import download_and_extract
from data.datasets import load_dataset_from_disk

from preprocess.format_sample import create_llama_vision_example
from preprocess.postprocess import clean_empty_lists

from train.train_pipeline import load_model_and_tokenizer, train_model
from train.save_and_push import save_and_push 

from config.training_config import get_training_config
from config.metrics import push_to_gateway

from dotenv import load_dotenv

import runpod
import os 
import time
import mlflow 

load_dotenv()

# Bucket 
bucket=os.getenv("PREPROCESSING_BUCKET")
s3_key=os.getenv("HF_DATASET_ZIP_KEY")
zip_path=os.getenv("ZIP_PATH")
extract_path=os.getenv("EXTRACT_PATH")

# Model path
model_path=os.getenv("MAIN_MODEL")
base_model=os.getenv("BASE_MODEL")
base_token=os.getenv("HUGGINGFACE_TOKEN")

def handler(job): 
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))
    mlflow.set_experiment("model_training")

    with mlflow.start_run():
        
        download_and_extract(bucket=bucket, 
                            s3_key=s3_key, 
                            zip_path=zip_path, 
                            extract_path=extract_path)
        
        dataset = load_dataset_from_disk(extract_path)
        formatted = [create_llama_vision_example(data) for data in dataset]
        processed = clean_empty_lists(formatted)
        print(processed[0])

        model, tokenizer = load_model_and_tokenizer(base_model)

        start = time.time()
        trainer = train_model(
            model=model,
            tokenizer=tokenizer,
            dataset=processed,
            config=get_training_config()
        )
        trainer.train()
        end = time.time()

        final_loss = trainer.state.log_history[-1].get("loss", 0.0)
        training_time = end - start

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

        return {
            "status": "success",
            "loss": final_loss,
            "training_time": training_time
        }

runpod.serverless.start({"handler": handler})