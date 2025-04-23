import os
from src.models import load_yolo_model, download_sam_checkpoint, load_sam_model
from src.processing import process_image

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
    main()