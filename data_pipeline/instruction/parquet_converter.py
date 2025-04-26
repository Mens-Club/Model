import io
from datasets import Dataset

def convert_dataset(data) -> io.BytesIO:
    ds = Dataset.from_list(data)
    
    buffer = io.BytesIO()
    ds.to_parquet(buffer)
    buffer.seek(0)

    print(f"✅ Parquet 변환 완료: 총 {len(ds)}개 샘플")
    
    return buffer