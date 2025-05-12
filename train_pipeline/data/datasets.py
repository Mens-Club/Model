from datasets import load_from_disk

def load_dataset_from_disk(path):
    print("📥 Dataset 로딩 중...")
    dataset = load_from_disk(path)
    print(f"✅ 로딩 완료! 샘플 수: {len(dataset)}")
    return dataset
