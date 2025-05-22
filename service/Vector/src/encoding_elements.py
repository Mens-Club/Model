import clip 
from PIL import Image
import requests
import io 
import torch 
import logging 


class Encoding:
    
    def __init__(self, model="ViT-B/32", device=None):
        
        # GPU Device 장착 
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
        
        try:
            self.model, self.preprocess = clip.load(model, device=self.device)
            self.model.eval()  # 평가 모드로 설정
        except Exception as e:
            raise RuntimeError(f"CLIP 모델 로딩 중 오류 발생: {e}")
     
    def encode_image(self, image_url):
        
        try:
            headers = {
                "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
            }
            response = requests.get(image_url, headers=headers)
            response.raise_for_status() # 상태 보고 
            
            image = Image.open(io.BytesIO(response.content))
            
            image_input = self.preprocess(image).unsqueeze(0).to(self.device)
            
            with torch.no_grad():
                image_features = self.model.encode_image(image_input)

            return image_features.cpu().numpy().flatten()
        except Exception as e:
            logging.info(f"이미지 처리 중 오류 발생 - {image_url}: {e}")
            return None

    def encode_text(self, text):
        try:
            text_input = clip.tokenize([text]).to(self.device)
                    # 텍스트 인코딩 (그래디언트 계산 비활성화)
            with torch.no_grad():
                text_features = self.model.encode_text(text_input)
            
            # numpy 배열로 변환 및 반환
            return text_features.cpu().numpy().flatten()
        
        except Exception as e:
            logging.info(f"텍스트 처리 중 오류 발생: {e}")
            return None