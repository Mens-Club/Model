import os
import urllib.request
import torch
from ultralyticsplus import YOLO
from segment_anything import sam_model_registry

def load_yolo_model():
    model = YOLO('kesimeg/yolov8n-clothing-detection')
    print('YOLO 모델 클래스:', model.names)

    cls_map = {v.lower(): k for k, v in model.names.items()}
    cloth_cls = cls_map['clothing']
    shoe_cls  = cls_map['shoes']
    return model, cloth_cls, shoe_cls

def download_sam_checkpoint(checkpoint_path="sam_vit_h_4b8939.pth"):
    if not os.path.exists(checkpoint_path):
        url = "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth"
        urllib.request.urlretrieve(url, checkpoint_path)
        print(f"SAM 체크포인트 다운로드 완료: {checkpoint_path}")
    else:
        print("SAM 체크포인트 이미 존재함.")
    return checkpoint_path

def load_sam_model(checkpoint_path):
    model_type = "vit_h"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    sam = sam_model_registry[model_type](checkpoint=checkpoint_path)
    sam.to(device=device)
    print(f"SAM 모델 로드 완료 (device: {device})")
    return sam, device
