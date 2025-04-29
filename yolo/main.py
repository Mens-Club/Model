import os
from src.models import load_yolo_model, download_sam_checkpoint, load_sam_model
from src.processing import process_image
import urllib.request
import pymysql

INPUT_FOLDER = './thumbnail_images'
OUTPUT_FOLDER = './result'

def main():
    model, cloth_cls, shoe_cls = load_yolo_model()
    sam_ckpt_path = download_sam_checkpoint()
    sam, device = load_sam_model(sam_ckpt_path)

    for filename in os.listdir(INPUT_FOLDER):
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff')):
            continue
        image_path = os.path.join(INPUT_FOLDER, filename)
        print(f"처리 중: {filename}")
        process_image(image_path, model, sam, cloth_cls, shoe_cls, OUTPUT_FOLDER, conf=0.1, augment=True)

    print("모든 이미지 처리 완료!")

if __name__ == "__main__":
    # DB 연결 및 데이터 가져오기 (기존 코드 유지)
    db = pymysql.connect(host='172.16.221.208', port=3300, user='HYEONG', passwd='1234', db='mensclub', use_unicode=True)
    cursor = db.cursor()
    query = "SELECT thumbnail_url FROM shoes_test LIMIT 20"
    cursor.execute(query)
    rows = cursor.fetchall()

    input_folder = './thumbnail_images'
    output_folder = './result'

    for idx, row in enumerate(rows):
        thumbnail_url = row[0]
        print(f"→ URL: {thumbnail_url}")
        image_path = os.path.join(input_folder, f'thumbnail_{idx + 1}.jpg')
        urllib.request.urlretrieve(thumbnail_url, image_path)

    cursor.close()
    db.close()

    main()