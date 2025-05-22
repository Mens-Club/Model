from datasets import load_from_disk
import logging

def load_dataset_from_disk(path):
    logging.info("Dataset 로딩 중...")
    dataset = load_from_disk(path)
    logging.info(f"로딩 완료! 샘플 수: {len(dataset)}")
    return dataset
