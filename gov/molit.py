# 국토교통부 실거래 검색 API
import json
import requests


# 네이버맵에서 좌표로 주소 구하는 URL
# 원본
# Request URL: https://rt.molit.go.kr/new/gis/getDanjiInfoDetail.do?menuGubun=G&p_lawd_cd=4719025300&p_house_cd=1&p_acc_year=2021&areaCode=&areaType=&jimokCd=&useCode=&useSubCode=&priceCode=&p_li_type=&_=1631083374124
# Request Method: GET

# Response Header
# Access-Control-Allow-Headers: x-requested-with
# Access-Control-Allow-Methods: POST, GET
# Access-Control-Allow-Origin: *
# Access-Control-Max-Age: 3600
# Connection: Keep-Alive
# Content-Language: ko-KR
# Content-Type: application/json;charset=utf-8
# Date: Wed, 08 Sep 2021 09:38:38 GMT
# Keep-Alive: timeout=10, max=98
# Server
# Set-Cookie: JSESSIONID=82530DCE69F56A3B5949355610622A43.rtmolit; # Path=/; Secure; HttpOnly
# Transfer-Encoding: chunked

api_url_real_sale_price = 'https://rt.molit.go.kr/new/gis/getDanjiInfoDetail.do?menuGubun=G&p_lawd_cd=4719025300&p_house_cd=1&p_acc_year=2021&areaCode=&areaType=&jimokCd=&useCode=&useSubCode=&priceCode=&p_li_type=&_=1631083374124'

# Request Header

header = {
    #Accept: application/json, text/javascript, */*; q=0.01
    #Accept-Encoding: gzip, deflate, br
    #Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7
    #Connection: keep-alive
    #Cookie: ROUTEID=.HTTP1; OPEN_POP0201=Y; JSESSIONID=6F09D2AB9A9E55FA33120E0E2C4862FF.rtmolit
    #Host: rt.molit.go.kr
    'Referer': 'https://rt.molit.go.kr/new/gis/srh.do?menuGubun=C&gubunCode=LAND',
    #sec-ch-ua: "Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"
    #sec-ch-ua-mobile: ?0
    #Sec-Fetch-Dest: empty
    #Sec-Fetch-Mode: cors
    #Sec-Fetch-Site: same-origin
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    #X-Requested-With: XMLHttpRequest
}

jimok_code = {
    '01': '전',
    '02': '답',
    '03': '과수원',
    '05': '임야',
    '08': '대',
    '14': '도로',
}

class RealSalePriceInfo:

    def __init__(self):

        # 계약월 "DEAL_MM": "09",
        self.deal_month = 1
        # 계약일 "DEAL_DD": 1,
        self.deal_day = 1
        # "DPOS_GBN": "2",
        # "DNAME": "고아읍",
        # 법정동 코드 "LAWD_CD": "4719025332",
        # 법정동 "NAME": "문성리",
        self.location = ''
        # 명칭? "UMD_NM": "문성리"
        # 도로명 "ROAD_NAME": "외예2길",
        self.road_name = ''
        # "JIBUN_GBN": "0",
        # 지번 "BUNJI": "7**",
        self.address = ''
        # 거래금액(만원) 토지 "OBJ_AMT": "50,000",
        # 거래금액(만원) 단독/다가구 "SUM_AMT": "10,800",
        self.amount = 0
        # 거래면적 토지 "PRIV_AREA": "650",
        # 대지면적 단독/다가구 "TOT_AREA": 265,
        self.area = 0
        # 연면적 단독/다가구 "BLDG_AREA": 71.5,
        self.total_building_area = 0
        # 건축연도 "BUILD_YEAR": 2015,
        self.build_year = 0
        # 주택유형 "BLDG_MUSE_NM": "단독",
        self.building_type = ''
        # 용도지역 코드 "USE_REGN": "UQA430",
        # 용도지역 "USE_REGN_NM": "자연녹지",
        self.region_usage = ''
        # 지목코드 "JIMOK_CD": "05",
        # 지목 "JIMOK_NM": "임야",
        self.jimok = ''
        # 지역지구 "LAND_USE_NM": "[포함]자연녹지지역",  없으면 null
        # 지역지구 "LAND_USE_LAW": "[포함]가축사육제한구역[가축분뇨의관리및이용에관한법률](절대제한구역(전 축종 제한)),[접합]하천구역[하천법]",  없으면 null
        # 도로조건 "ROAD_LEN": "-",
        self.road_length = ''
        # 토지대장
        # 토지이동일 "LAND_MOVE1": "202*",
        # 토지이동사유 "LAND_MOVE2": "산 번에서 등록전환",
        # 건축물대장
        # 지상층수 "GRND_FLR_CNT": null,
        self.floor_count = 0
        # 건폐율 "VL_RAT": null,
        # 용적률 "BC_RAT": null,
        # 주구조 "ETC_STRCT": null,
        self.structure = ''
        # 해제사유 발생일 "CNTL_YMD": null,
        self.cancel_ymd = ''

        self.amount_per_area = 0

    def __repr__(self):
        str = f'{self.location} {self.address} {self.jimok} {self.deal_month}-{self.deal_day} {self.amount}만원'
        return str

    def __str__(self):
        str = f'{self.location} {self.address} {self.jimok} {self.deal_month}-{self.deal_day} {self.amount}만원'
        return str

    def parseFromJson(self, jsonObject):
        self.deal_month = int(jsonObject.get('DEAL_MM', 0))
        self.deal_day = jsonObject.get('DEAL_DD', 0)
        self.location = jsonObject.get('NAME', '')
        self.road_name = jsonObject.get('ROAD_NAME', '')
        self.address = jsonObject.get('BUNJI', '')
        if jsonObject.get('SUM_AMT') is not None:
            self.amount = int(jsonObject['SUM_AMT'].replace(',',''))
        elif jsonObject.get('OBJ_AMT') is not None:
            self.amount = int(jsonObject['OBJ_AMT'].replace(',',''))
        else:
            self.amount = 0
        if jsonObject.get('TOT_AREA') is not None:
            self.area = jsonObject['TOT_AREA']
        elif jsonObject.get('PRIV_AREA') is not None:
            self.area = int(jsonObject['PRIV_AREA'].replace(',',''))
        else:
            self.area = 0
        self.total_building_area = jsonObject.get('BLDG_AREA', 0)
        self.build_year = jsonObject.get('BUILD_YEAR', 0)
        self.building_type = jsonObject.get('BLDG_MUSE_NM', '')
        self.region_usage = jsonObject.get('USE_REGN_NM', '')
        self.jimok = jsonObject.get('JIMOK_NM', '')
        self.road_length = jsonObject.get('ROAD_LEN', '')
        self.floor_count = jsonObject.get('GRND_FLR_CNT', 0)
        self.structure = jsonObject.get('ETC_STRCT', '')
        self.cancel_ymd = jsonObject.get('CNTL_YMD', None)

        self.amount_per_area = round(self.amount / self.area * 3.3)

search_category = {
    '아파트': 'A',
    '연립/다세대': 'B',
    '단독/다가구': 'C',
    '오피스텔': 'E',
    '분양/입주권': 'F',
    '상업/업무용': 'H',
    '토지': 'G',
}

def get_real_sale_price(category, location_code, year):
    result = []

    #url = f'https://rt.molit.go.kr/new/gis/getDanjiInfoDetail.do?menuGubun={category}&p_lawd_cd={location_code}&p_house_cd=1&p_acc_year={year}&areaCode=&areaType=&jimokCd=&useCode=&useSubCode=&priceCode=&p_li_type=&_=1631083374124'
    url = f'https://rt.molit.go.kr/new/gis/getDanjiInfoDetail.do?menuGubun={category}&p_lawd_cd={location_code}&p_house_cd=1&p_acc_year={year}&areaCode=&areaType=&jimokCd=&useCode=&useSubCode=&priceCode=&p_li_type='

    response = requests.get(url, headers=header)

    if response.status_code != 200 :
        print(f'Http error : {response.status_code}')
        return result

    #response 데이터 확인
    #print(response.content)

    json_data = json.loads(response.content)
    #print(json_data)

    json_results = json_data.get('result', None)
    if json_results is None:
        return result

    for json_result in json_results:
        info = RealSalePriceInfo()
        info.parseFromJson(json_result)
        result.append(info)

    return result


if __name__ == "__main__":
    print(get_real_sale_price('C', '4719025334', 2021))
