from get_category import connect_to_db, get_categories

total_style_dict = {'캐주얼': '1', '미니멀': '11'}
top_fit_dict = {'슬림': '2%5E87', '레귤러': '2%5E88', '오버사이즈': '2%5E90'}
bottom_fit_dict = {'와이드': '14%5E238', '스트레이트': '14%5E239', '테이퍼드': '14%5E242'}
season_dict = {'봄': '31%5E361', '여름': '31%5E362', '가을': '31%5E363', '겨울': '31%5E364'}
sleeve_dict = {'반소매': '11%5E225', '긴소매': '11%5E228'}
sleeves = ['피케&카라 티셔츠', '니트&스웨터','셔츠&블라우스']

total_color_dict = {
    '화이트': 'WHITE', 
    '그레이': 'GRAY', 
    '블랙': 'BLACK', 
    '버건디': 'BURGUNDY', 
    '오트밀': 'OATMEAL', 
    '아이보리': 'IVORY', 
    '카키': 'KHAKI', 
    '스카이블루': 'SKYBLUE', 
    '네이비': 'NAVY', 
    '베이지': 'BEIGE', 
    '브라운': 'BROWN',
    '데님': 'DENIM',
    '연청': 'LIGHTBLUEDENIM',
    '중청': 'MEDIUMBLUEDENIM',
    '진청': 'DARKBLUEDENIM',
    '흑청': 'BLACKDENIM'
}

shoes_color_dict = {
    '화이트': 'WHITE',
    '그레이': 'GRAY',
    '블랙': 'BLACK',
    '버건디': 'BURGUNDY',
    '오트밀': 'OATMEAL',
    '아이보리': 'IVORY',
    '카키': 'KHAKI',
    '스카이블루': 'SKYBLUE',
    '네이비': 'NAVY',
    '베이지': 'BEIGE',
    '브라운': 'BROWN'
}

shoes_urls = []
bottom_urls = []
outwear_urls = []
top_urls = []

def generate_url(categories):
    for category in categories['신발']:
        for color in shoes_color_dict.keys():
            url = f'https://api.musinsa.com/api2/dp/v1/plp/goods?gf=M&color={shoes_color_dict[color]}&category={category[1]}&size=60&caller=CATEGORY&page=1'
            # print(url)
            shoes_urls.append([url, color, '신발', category[0]])

    for category in categories['하의']:
        for style in total_style_dict.keys():
            for color in total_color_dict.keys():
                for fit in bottom_fit_dict.keys():
                    url = f'https://api.musinsa.com/api2/dp/v1/plp/goods?gf=M&color={total_color_dict[color]}&attribute={bottom_fit_dict[fit]}&style={total_style_dict[style]}&category={category[1]}&size=60&caller=CATEGORY&page=1'
                    # print(url)
                    bottom_urls.append([url, style, fit, color, '후처리', '하의', category[0]])

    for category in categories['아우터']:
        for style in total_style_dict.keys():
            for color in total_color_dict.keys():
                for fit in top_fit_dict.keys():
                    url = f'https://api.musinsa.com/api2/dp/v1/plp/goods?gf=M&color={total_color_dict[color]}&attribute={top_fit_dict[fit]}&style={total_style_dict[style]}&category={category[1]}&size=60&caller=CATEGORY&page=1'
                    # print(url)
                    outwear_urls.append([url, style, fit, color, '후처리', '아우터', category[0]])

    for category in categories['상의']:
        if category[0] in sleeves:
            for style in total_style_dict.keys():
                for color in total_color_dict.keys():
                    for fit in top_fit_dict.keys(): 
                        for sleeve in sleeve_dict.keys():
                            url = f'https://api.musinsa.com/api2/dp/v1/plp/goods?gf=M&color={total_color_dict[color]}&attribute={top_fit_dict[fit]},{sleeve_dict[sleeve]}&style={total_style_dict[style]}&category={category[1]}&size=60&caller=CATEGORY&page=1'
                            # print(url)
                            top_urls.append([url, style, fit, color, '후처리', '상의', str(category[0]) + ' - ' + sleeve])
        else:
            for style in total_style_dict.keys():
                for color in total_color_dict.keys():
                    for fit in top_fit_dict.keys(): 
                        url = f'https://api.musinsa.com/api2/dp/v1/plp/goods?gf=M&color={total_color_dict[color]}&attribute={top_fit_dict[fit]}&style={total_style_dict[style]}&category={category[1]}&size=60&caller=CATEGORY&page=1'
                        # print(url)
                        top_urls.append([url, style, fit, color, '후처리', '상의', category[0]])

    return shoes_urls, bottom_urls, outwear_urls, top_urls