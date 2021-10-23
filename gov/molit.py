import json
import requests

# 국토교통부 실거래 검색 API

class RealPrice:

    # Request Header
    headers = {
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

    search_category = {
        '아파트': 'A',
        '연립/다세대': 'B',
        '단독/다가구': 'C',
        '오피스텔': 'E',
        '분양/입주권': 'F',
        '상업/업무용': 'H',
        '토지': 'G',
    }

    deal_type = {
        '매매': 1,
        '전/월세': 2,
    }

    jimok_code = {
        '01': '전',
        '02': '답',
        '03': '과수원',
        '05': '임야',
        '08': '대',
        '14': '도로',
    }

    def __init__(self):
        pass

    def parseFromJson(self, json_obj):
        pass

    @classmethod
    def create(cls):
        return cls()

    @classmethod
    def search_(cls, url, params, list_key='result'):
        result = []

        response = requests.get(url, headers=cls.headers, params=params)

        if response.status_code != 200 :
            print(f'Http error : {response.status_code}')
            return result

        #response 데이터 확인
        #print(response.content)

        json_data = json.loads(response.content)
        #print(json_data)

        json_results = json_data.get(list_key, None)
        if json_results is None:
            return result

        for json_result in json_results:
            info = cls.create()
            info.parseFromJson(json_result)
            result.append(info)

        return result


    @classmethod
    def get_year_info_(cls, url, params):
        result = []

        response = requests.get(url, headers=cls.headers, params=params)

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

        for item in json_results:
            area = item.get('ACC_YEAR')
            if area:
                result.append(area)

        return result

    @staticmethod
    def json_get(json_object, key, default):
        val = json_object.get(key)
        if not val:
            val = default
        return val


class RealPriceDandok(RealPrice):

    def __init__(self):
        super().__init__()

        # 계약월 "DEAL_MM": "09",
        self.deal_month = 1
        # 계약일 "DEAL_DD": 1,
        self.deal_day = 1
        # 명칭? "UMD_NM": "문성리"
        # "DNAME": "고아읍",
        # 법정동 코드 "LAWD_CD": "4719025332",
        self.lawd_cd = ''
        # 법정동 "NAME": "문성리",
        self.location = ''
        # 지번 "BUNJI": "7**",
        self.address = ''
        # 도로명 "ROAD_NAME": "외예2길",
        self.road_name = ''
        # 거래금액(만원) "SUM_AMT": "10,800",
        self.price = 0
        # 주택유형 "BLDG_MUSE_NM": "단독",
        self.building_type = ''
        # 건축연도 "BUILD_YEAR": 2015,
        self.build_year = 0
        # 대지면적 "TOT_AREA": 265,
        self.area = 0
        # 연면적 단독/다가구 "BLDG_AREA": 71.5,
        self.total_building_area = 0
        # 지상층수 "GRND_FLR_CNT": null,
        self.floor_count = 0
        # 도로조건 "ROAD_LEN": "-",
        self.road_length = ''
        # 주구조 "ETC_STRCT": null,
        self.structure = ''
        # 건폐율 "VL_RAT": null,
        # 용적률 "BC_RAT": null,
        # 해제사유 발생일 "CNTL_YMD": null,
        self.cancel_ymd = ''
        # 지역지구 "LAND_USE_NM": "[포함]자연녹지지역",  없으면 null
        # 지역지구 "LAND_USE_LAW": "[포함]가축사육제한구역[가축분뇨의관리및이용에관한법률](절대제한구역(전 축종 제한)),[접합]하천구역[하천법]",  없으면 null
        # "DPOS_GBN": "2",
        # "APTFNO": null,
        # "APT_CODE": null,

        self.price_per_area = 0.0

    def __repr__(self):
        str = f'{self.location} {self.address} {self.jimok} {self.deal_month}-{self.deal_day} {self.price}만원'
        return str

    def parseFromJson(self, json_obj):
        self.month = int(self.json_get(json_obj, 'DEAL_MM', '0'))
        self.day = self.json_get(json_obj, 'DEAL_DD', 0)
        self.lawd_cd = self.json_get(json_obj, 'LAWD_CD', '')
        self.location = self.json_get(json_obj, 'NAME', '')
        self.road_name = self.json_get(json_obj, 'ROAD_NAME', '')
        self.address = self.json_get(json_obj, 'BUNJI', '')
        self.price = int(self.json_get(json_obj, 'SUM_AMT', '0').replace(',','')) * 10000
        self.area = float(self.json_get(json_obj, 'TOT_AREA', '0.0'))
        self.total_building_area = float(self.json_get(json_obj, 'BLDG_AREA', '0.0'))
        self.build_year = self.json_get(json_obj, 'BUILD_YEAR', 0)
        self.building_type = self.json_get(json_obj, 'BLDG_MUSE_NM', '')
        self.road_length = self.json_get(json_obj, 'ROAD_LEN', '')
        floor_count = json_obj.get('GRND_FLR_CNT', 0)
        if str.isdigit(floor_count):
            self.floor_count = int(floor_count)
        self.structure = self.json_get(json_obj, 'ETC_STRCT', '')
        self.cancel_ymd = json_obj.get('CNTL_YMD', None)

        self.price_per_area = round(self.price / self.area * 3.3)

    @classmethod
    def search(cls, deal_type, location_code, year):
        url = f'https://rt.molit.go.kr/new/gis/getDanjiInfoDetail.do'
        params = {
            'menuGubun': 'C',
            'p_lawd_cd': '20177829',
            'p_house_cd': '1',
            'p_acc_year': '2021',
            'areaCode': '',
            'areaType': '',
            'jimokCd': '',
            'useCode': '',
            'useSubCode': '',
            'priceCode': '',
            'p_li_type': '',
        }
        params['p_house_cd'] = f'{deal_type}'
        params['p_lawd_cd'] = f'{location_code}'
        params['p_acc_year'] = f'{year}'

        return cls.search_(url, params)


class RealPriceLand(RealPrice):

    def __init__(self):
        super().__init__()

        # 계약월 "DEAL_MM": "09",
        self.month = 1
        # 계약일 "DEAL_DD": 1,
        self.day = 1
        # "DNAME": "고아읍",
        # 명칭? "UMD_NM": "문성리"
        # 법정동 코드 "LAWD_CD": "4719025332",
        self.lawd_cd = ''
        # 법정동 "NAME": "문성리",
        self.location = ''
        # "JIBUN_GBN": "0",
        self.is_san = 0
        # 지번 "BUNJI": "7**",
        self.address = ''
        # 거래면적 토지 "PRIV_AREA": "650",
        self.area = 0
        # 거래금액(만원) 토지 "OBJ_AMT": "50,000",
        self.price = 0
        # 도로조건 "ROAD_LEN": "-",
        self.road_length = ''
        # 지목코드 "JIMOK_CD": "05",
        # 지목 "JIMOK_NM": "임야",
        self.jimok = ''
        # 용도지역 "USE_REGN_NM": "자연녹지",
        self.region_usage = ''
        # 해제사유 발생일 "CNTL_YMD": null,
        self.cancel_ymd = ''
        # 지역지구 "LAND_USE_NM": "[포함]자연녹지지역",  없으면 null
        # 지역지구 "LAND_USE_LAW": "[포함]가축사육제한구역[가축분뇨의관리및이용에관한법률](절대제한구역(전 축종 제한)),[접합]하천구역[하천법]",  없으면 null
        # 용도지역 코드 "USE_REGN": "UQA430",
        # 지상층수 "GRND_FLR_CNT": null,
        # 건폐율 "VL_RAT": null,
        # 용적률 "BC_RAT": null,
        # "DPOS_GBN": "2",
        # 주구조 "ETC_STRCT": null,
        self.price_per_area = 0.0

    def __repr__(self):
        str = f'{self.location} {self.address} {self.jimok} {self.month}-{self.day} {self.price}'
        return str

    def parseFromJson(self, json_obj):
        self.month = int(self.json_get(json_obj, 'DEAL_MM', '0'))
        self.day = self.json_get(json_obj, 'DEAL_DD', 0)
        self.lawd_cd = self.json_get(json_obj, 'LAWD_CD', '')
        self.location = self.json_get(json_obj, 'NAME', '')
        self.is_san = self.json_get(json_obj, 'JIBUN_GBN', '0')
        self.address = self.json_get(json_obj, 'BUNJI', '')
        self.area = int(self.json_get(json_obj, 'PRIV_AREA', '0').replace(',', ''))
        self.price = int(self.json_get(json_obj, 'OBJ_AMT', '0').replace(',', '')) * 10000
        self.road_length = self.json_get(json_obj, 'ROAD_LEN', '')
        self.jimok = self.json_get(json_obj, 'JIMOK_NM', '')
        self.region_usage = self.json_get(json_obj, 'USE_REGN_NM', '')
        self.cancel_ymd = json_obj.get('CNTL_YMD', None)
        self.price_per_area = round(self.price / self.area * 3.3)

    @classmethod
    def search(cls, location_code, year):
        url = f'https://rt.molit.go.kr/new/gis/getDanjiInfoDetail.do'
        params = {
            'menuGubun': 'G',
            'p_lawd_cd': '20177829',
            'p_house_cd': '1',
            'p_acc_year': '2021',
            'areaCode': '',
            'areaType': '',
            'jimokCd': '',
            'useCode': '',
            'useSubCode': '',
            'priceCode': '',
            'p_li_type': '',
        }
        params['p_lawd_cd'] = f'{location_code}'
        params['p_acc_year'] = f'{year}'

        return cls.search_(url, params)

    @classmethod
    def get_year_info(cls, lawd_cd):
        url = f'https://rt.molit.go.kr/new/gis/getDanjiInfoYearList.do'
        params = {
            'menuGubun': 'G',
            'p_lawd_cd': '4719025334',
            'p_house_cd': '1',
            # 호출 시 1씩 증가함
            #'_': '1634279982277',
        }
        params['p_lawd_cd'] = f'{lawd_cd}'

        return cls.get_year_info_(url, params)



class RealPriceAptInfo(RealPrice):
    def __init__(self):
        super().__init__()
        self.aptcd = ''
        self.name = ''

    def __repr__(self):
        str = f'{self.aptcd} {self.name}'
        return str

    def parseFromJson(self, json_obj):
        self.aptcd = self.json_get(json_obj, 'APT_CODE', '')
        self.name = self.json_get(json_obj, 'APT_NAME', '')

    @classmethod
    def search(cls, lawd_cd):
        url = f'https://rt.molit.go.kr/new/gis/getDanjiComboAjax.do'
        params = {
            'menuGubun': 'A',
            'srhType': '',
            'srhYear': '2021',
            'srhLastYear': '',
            'gubunCode': 'LAND', # LAND, ROAD
            'sidoCode': '',
            'gugunCode': '',
            'danjiName': '',
            'roadCode': '483304814913',
            'roadBun1': '65',
            'roadBun2': '',
            'dongCode': '',
            'rentAmtType': '3',
        }
        params['sidoCode'] =  lawd_cd[0:2]
        params['gugunCode'] = lawd_cd[0:5]
        params['dongCode'] =  lawd_cd

        return cls.search_(url, params, 'jsonList')


class RealPriceApt(RealPrice):
    def __init__(self):
        super().__init__()
        self.name = ''
        self.aptcd = ''
        self.build_year = 0
        self.address = ''
        self.dong = 0
        self.floor = 0
        self.ho = 0
        self.area = 0.0
        self.month = 0
        self.day = 0
        # 전/월세 일 경우 전세금
        self.price = 0
        # 전/월세 일 경우 월세금
        self.rent_amount = 0
        self.cancel_ymd = ''

    def __repr__(self):
        str = f'{self.month:02d}-{self.day:02} {self.name} {self.dong}-{self.floor}{self.ho:02} {self.price}'
        return str

    def parseFromJson(self, json_obj):
        self.name = self.json_get(json_obj, 'BLDG_NM', '')
        self.aptcd = str(self.json_get(json_obj, 'BLDG_CD', ''))
        self.build_year = self.json_get(json_obj, 'BUILD_YEAR', 0)
        address = self.json_get(json_obj, 'JIBUN_NAME', '')
        address += ' '
        address += self.json_get(json_obj, 'BOBN', '')
        self.dong = self.json_get(json_obj, 'DONG_CODE', 0)
        self.ho = self.json_get(json_obj, 'HO_CODE', 0)
        self.floor = self.json_get(json_obj, 'APTFNO', 0)
        self.area = self.json_get(json_obj, 'BLDG_AREA', 0.0)
        self.month = int(self.json_get(json_obj, 'DEAL_MM', '0'))
        self.day = self.json_get(json_obj, 'DEAL_DD', 0)
        self.price = int(self.json_get(json_obj, 'SUM_AMT', '0').replace(',', '')) * 10000
        self.rent_amount = int(self.json_get(json_obj, 'RENT_AMT', '0').replace(',', '')) * 10000
        self.cancel_ymd = json_obj.get('CNTL_YMD', None)

    @classmethod
    def search(cls, deal_type, apt_cd, year):
        url = f'https://rt.molit.go.kr/new/gis/getDanjiInfoDetail.do'
        params = {
            'menuGubun': 'A',
            'p_apt_code': '20177829',
            'p_house_cd': '1',
            'p_acc_year': '2021',
            'areaCode': '',
            'priceCode': '',
        }
        params['p_house_cd'] = f'{deal_type}'
        params['p_apt_code'] = f'{apt_cd}'
        params['p_acc_year'] = f'{year}'

        return cls.search_(url, params)


    @classmethod
    def get_apt_list(cls, lawd_cd):
        result = []
        url = f'https://rt.molit.go.kr/new/gis/getDanjiComboAjax.do'
        params = {
            'menuGubun': 'A',
            'srhType': '',
            'srhYear': '2021',
            'srhLastYear': '',
            'gubunCode': 'LAND', # LAND, ROAD
            'sidoCode': '',
            'gugunCode': '',
            'danjiName': '',
            'roadCode': '483304814913',
            'roadBun1': '65',
            'roadBun2': '',
            'dongCode': '',
            'rentAmtType': '3',
        }
        params['sidoCode'] =  lawd_cd[0:2]
        params['gugunCode'] = lawd_cd[0:5]
        params['dongCode'] =  lawd_cd

        response = requests.post(url, headers=cls.headers, params=params)

        if response.status_code != 200 :
            print(f'Http error : {response.status_code}')
            return result

        #response 데이터 확인
        #print(response.content)

        json_data = json.loads(response.content)
        #print(json_data)

        json_results = json_data.get('jsonList', None)
        if json_results is None:
            return result

        for item in json_results:
            print(f"{item.get('APT_CODE')} {item.get('APT_NAME')}")
        print(len(result))
        return result

    @classmethod
    def get_area_info(cls, deal_type, apt_cd, year):
        result = []
        url = f'https://rt.molit.go.kr/new/gis/getDanjiInfoBldgList.do'
        params = {
            'menuGubun': 'A',
            'p_apt_code': '20177829',
            'p_year': '2021',
            'p_house_cd': '1',
            #'_': '1634279982277',
        }
        params['p_house_cd'] = f'{deal_type}'
        params['p_apt_code'] = f'{apt_cd}'
        params['p_year'] = f'{year}'

        response = requests.get(url, headers=cls.headers, params=params)

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

        for item in json_results:
            area = item.get('BLDG_AREA')
            if area:
                result.append(area)

        return result

    @classmethod
    def get_year_info(cls, deal_type, apt_cd):
        url = f'https://rt.molit.go.kr/new/gis/getDanjiInfoYearList.do'
        params = {
            'menuGubun': 'A',
            'p_apt_code': '20177829',
            'p_house_cd': '2',
            # 호출 시 1씩 증가함
            #'_': '1634279982277',
        }
        params['p_house_cd'] = f'{deal_type}'
        params['p_apt_code'] = f'{apt_cd}'

        return cls.get_year_info_(url, params)


if __name__ == "__main__":
    #print(RealPriceDandok.search(1, '4719025334', 2021))
    #print(RealPriceLand.search('4719025334', 2021))
    #print(RealPriceApt.search(1, '20177829', 2021))
    #print(RealPriceApt.get_area_info(1, '20177829', 2021))
    #print(RealPriceApt.get_year_info(1, '20177829'))
    print(len(RealPriceAptInfo.search('4833031026')))
