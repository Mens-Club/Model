import os
import cv2
import numpy as np
from PIL import Image
from segment_anything import SamPredictor

#배경 흐림+명암 평활화로 전처리리
def preprocess(img_np):
    blur = cv2.GaussianBlur(img_np, (5,5), 1.5)
    lab = cv2.cvtColor(blur, cv2.COLOR_RGB2LAB)
    lab[:,:,0] = cv2.equalizeHist(lab[:,:,0])
    return cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)

def process_image(image_path, model, sam, cloth_cls, shoe_cls, output_folder, conf, augment):
    fname = os.path.basename(image_path)
    # 1) load & preprocess
    img_pil = Image.open(image_path).convert("RGB")
    img_np = np.array(img_pil)
    proc = preprocess(img_np)

    # 2) YOLO TTA 예측: shoes → clothing
    target = 'clothing'
    res = model.predict(source=proc, conf=conf, classes=[cloth_cls], augment=augment)
    xyxy = res[0].boxes.xyxy.cpu().numpy()
    if len(xyxy) == 0:
        target = 'shoes'
        res = model.predict(source=proc, conf=conf, classes=[shoe_cls], augment=augment)
        xyxy = res[0].boxes.xyxy.cpu().numpy()

    if len(xyxy) == 0:
        print(f"{fname}: 검출 실패")
        return

    # 3) 가장 넓은 박스
    areas = (xyxy[:,2]-xyxy[:,0])*(xyxy[:,3]-xyxy[:,1])
    box = xyxy[np.argmax(areas)]

    # 4) SAM 분할
    predictor = SamPredictor(sam)
    predictor.set_image(proc)
    masks,_,_ = predictor.predict(box=box[None,:], multimask_output=False)
    mask = masks[0]
    ys, xs = np.where(mask)
    if len(xs) == 0:
        print(f"{fname}: 마스크 영역 없음")
        return

    # RGBA 크롭 및 저장
    crop = img_np[ys.min():ys.max()+1, xs.min():xs.max()+1]
    rgba = np.zeros((crop.shape[0],crop.shape[1],4), dtype=np.uint8)
    rgba[..., :3] = crop
    rgba[..., 3]  = mask[ys.min():ys.max()+1, xs.min():xs.max()+1] * 255

    base, _ = os.path.splitext(fname)
    out_path = os.path.join(output_folder, f"{base}_{target}.png")
    Image.fromarray(rgba).save(out_path)
    print(f"Saved: {out_path}")