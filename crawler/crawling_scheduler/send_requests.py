import requests
import time
import random
from tqdm import tqdm
from generate_url import generate_url

season_map = {
    '캔버스/단화': '봄, 여름, 가을, 겨울', 
    '패션스니커즈화': '봄, 여름, 가을, 겨울', 
    '기타 스니커즈': '봄, 여름, 가을, 겨울',
    '앵클/숏 부츠': '봄, 가을, 겨울', 
    '미들/하프 부츠': '봄, 가을, 겨울', 
    '워커': '봄, 여름, 가을, 겨울',
    '더비 슈즈': '봄, 여름, 가을, 겨울', 
    '스트레이트 팁': '봄, 여름, 가을, 겨울', 
    '로퍼': '봄, 여름, 가을, 겨울',
    '모카신': '봄, 여름, 가을, 겨울', 
    '쪼리/플립플랍': '여름', 
    '스포츠/캐주얼 샌들': '여름',

    '겨울 싱글 코트': '겨울',
    '롱패딩&헤비 아우터': '겨울',
    '무스탕&퍼': '겨울',
    '겨울 기타 코트': '겨울',
    '숏패딩&헤비 아우터': '겨울',
    '겨울 더블 코트': '겨울',

    '코튼 팬츠': '봄, 가을, 겨울',
    '트레이닝&조거 팬츠': '봄, 가을, 겨울',
    '데님 팬츠': '봄, 가을, 겨울',
    '슈트 팬츠&슬랙스': '봄, 가을, 겨울',
    '긴소매 티셔츠': '봄, 가을, 겨울',
    '맨투맨&스웨트': '봄, 가을, 겨울',
    '후드 티셔츠': '봄, 가을, 겨울',
    '니트&스웨터 - 긴소매': '봄, 가을, 겨울',
    '피케&카라 티셔츠 - 긴소매': '봄, 가을, 겨울',
    '셔츠&블라우스 - 긴소매': '봄, 가을, 겨울',

    '숏팬츠': '여름',
    '반소매 티셔츠': '여름',
    '피케&카라 티셔츠 - 반소매': '여름',
    '니트&스웨터 - 반소매': '여름',
    '셔츠&블라우스 - 반소매': '여름',

    '후드 집업': '봄, 가을',
    '카디건': '봄, 가을',
    '트레이닝 재킷': '봄, 가을',
    '아노락 재킷': '봄, 가을',
    '나일론&코치 재킷': '봄, 가을',
    '플리스&뽀글이': '봄, 가을',
    '사파리&헌팅 재킷': '봄, 가을',
    '블루종&MA-1': '봄, 가을',
    '패딩 베스트': '봄, 가을',
    '트러커 재킷': '봄, 가을',
    '환절기 코트': '봄, 가을',
    '스타디움 재킷': '봄, 가을',
    '슈트&블레이저 재킷': '봄, 가을'
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.musinsa.com/",
    "Origin": "https://www.musinsa.com",
}

def send_requests(shoes_urls, bottom_urls, outwear_urls, top_urls):
    shoes_results = []
    for url in tqdm(shoes_urls, desc="신발 크롤링 진행중"):
        response = requests.get(url[0], headers=headers)
        json_data = response.json()['data']['list']
        for json in json_data:
            data = {
                '컬러': url[1],
                '소분류': url[3],
                '계절': season_map.get(url[3], ''),
                '제품명': json['goodsName'],
                '썸네일링크': json['thumbnail'],
                '판매여부': json['isSoldOut'],
                '제품링크': json['goodsLinkUrl'],
                '브랜드': json['brandName'],
                '원가': json['normalPrice'],
                '가격': json['price'],
            }
            shoes_results.append(data)

        if len(json_data) != 0:
            print(data)
        else:
            print(url[1], url[3], '데이타 없다!')
        time.sleep(random.uniform(1, 2))

    other_results = []
    for url_list in [bottom_urls, outwear_urls, top_urls]:
        for url in tqdm(url_list, desc="그외 크롤링 진행중"):
            response = requests.get(url[0], headers=headers)
            json_data = response.json()['data']['list']
            for json in json_data:
                data = {
                    '스타일': url[1], 
                    '계절': season_map.get(url[6], ''),
                    '핏': url[2], 
                    '컬러': url[3], 
                    '제품명': json['goodsName'],
                    '썸네일링크': json['thumbnail'],
                    '판매여부': json['isSoldOut'],
                    '제품링크': json['goodsLinkUrl'],
                    '브랜드': json['brandName'],
                    '원가': json['normalPrice'],
                    '가격': json['price'],
                    '대분류': url[5],
                    '소분류': url[6]
                }
                other_results.append(data)

            if len(json_data) != 0:
                print(data)
            else:
                print(url[1], url[4], url[2], url[3], url[6], '데이타 없다!')
            time.sleep(random.uniform(1, 2))

    return shoes_results, other_results