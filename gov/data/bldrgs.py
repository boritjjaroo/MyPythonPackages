import requests
import xml.etree.ElementTree as ET
import gov.data.util as util

# 공공데이터포털(data.go.kr)
# 국토교통부_건축물대장정보 서비스(https://www.data.go.kr/data/15044713/openapi.do)

class BldRgs:

    service_url = 'http://apis.data.go.kr/1613000/BldRgstService_v2/'
    params = {
        'serviceKey': util.service_key,
        # 5자리
        'sigunguCd': '48330',
        'bjdongCd': '25324',
        # 0:대지 1:산 2:블록
        'platGbCd': '0',
        'bun': '',
        'ji': '',
        'startDate': '',
        'endDate': '',
        'numOfRows': '1000',
        'pageNo': '1',
    }

    def __init__(self):
        pass

    def __repr__(self):
        str = f''
        return str

    @staticmethod
    def search(service_name, lawd_cd, is_san, bonbun=None, bubun=None, dong=None, ho=None, rows=None, page=None):

        if not lawd_cd or len(lawd_cd) != 10:
            return None

        url = BldRgs.service_url + service_name
        params = BldRgs.params

        params['sigunguCd'] = lawd_cd[0:5]
        params['bjdongCd'] = lawd_cd[5:10]
        params['platGbCd'] = f'{is_san}'
        if bonbun:
            if isinstance(bonbun, str) and bonbun.isdigit():
                params['bun'] = f'{bonbun:0>04}'
            else:
                params['bun'] = f'{bonbun:04}'
        if bubun:
            if isinstance(bubun, str) and bubun.isdigit():
                params['ji'] = f'{bubun:0>04}'
            else:
                params['ji'] = f'{bubun:04}'
        if dong:
            params['dongNm'] = dong
        if ho:
            params['hoNm'] = ho
        if rows:
            params['numOfRows'] = rows
        if page:
            params['pageNo'] = page


        response = requests.get(url, params=params)
        if response.status_code != 200 :
            print(f'{service_name} Http error : {response.status_code}')
            return None

        #response 데이터 확인
        #print(response.content)

        root = ET.fromstring(response.content.decode('utf-8'))
        print(f"{service_name} : {root.find('header').findtext('resultMsg')}")
        return root

# 국토교통부_건축물대장 표제부 조회
class BldRgsTitle(BldRgs):

    service_name = 'getBrTitleInfo'

    def __init__(self):
        self.pnu = ''
        self.lawd_cd = ''
        self.bonbun = 0
        self.bubun = 0
        self.address = ''
        self.plot_area = 0.0
        self.building_total_area = 0.0
        self.building_area = 0.0
        self.use_approve_date = ''
        self.structure = ''
        self.structure_etc = ''
        self.main_purpose = ''
        self.detail_purpose = ''
        self.height = 0.0
        self.ground_floor = 0
        self.under_floor = 0

    def __repr__(self):
        str = f'{self.address}'
        return str

    @staticmethod
    def search(lawd_cd, is_san, bonbun=None, bubun=None):
        result = []

        root = BldRgs.search(BldRgsTitle.service_name, lawd_cd, is_san, bonbun, bubun)

        for item in root.iter('item'):
            building = BldRgsTitle()

            sigungu = item.findtext('sigunguCd', '00000')
            eupmyundong = item.findtext('bjdongCd', '00000')
            san = int(item.findtext('platGbCd', '0'))
            bun = int(item.findtext('bun', '0'))
            ji = int(item.findtext('ji', '0'))
            building.pnu = f'{sigungu}{eupmyundong}{san+1}{bun:04}{ji:04}'
            building.lawd_cd = sigungu + eupmyundong
            building.bonbun = bun
            building.bubun = ji

            building.address = item.findtext('platPlc', '')
            building.plot_area = float(item.findtext('platArea', '0.0'))
            building.building_total_area = float(item.findtext('totArea', '0.0'))
            building.building_area = float(item.findtext('archArea', '0.0'))
            building.use_approve_date = item.findtext('useAprDay', '19000101')
            building.use_approve_date = f'{building.use_approve_date[0:4]}-{building.use_approve_date[4:6]}-{building.use_approve_date[6:8]}'
            building.structure = item.findtext('strctCdNm', '')
            building.structure_etc = item.findtext('etcStrct', '')
            building.main_purpose = item.findtext('mainPurpsCdNm', '')
            building.detail_purpose = item.findtext('etcPurps', '')
            building.height = float(item.findtext('heit', '0.0'))
            building.ground_floor = int(item.findtext('grndFlrCnt', '0'))
            building.under_floor = int(item.findtext('ugrndFlrCnt', '0'))
            result.append(building)
        
        return result

# 국토교통부_건축물대장 주택가격 조회
# 국가공간정보포털(nsdi)에 있는 자료가 검색 안 되는 경우 있음
class BldRgsPrice(BldRgs):

    service_name = 'getBrHsprcInfo'

    def __init__(self):
        pass

    def __repr__(self):
        str = f''
        return str

    @staticmethod
    def search(lawd_cd, is_san, bonbun=None, bubun=None):
        result = []

        root = BldRgs.search(BldRgsPrice.service_name, lawd_cd, is_san, bonbun, bubun)

        for item in root.iter('item'):
            print(item.findtext('hsprc'))

        return result

if __name__ == "__main__":
    #print(BldRgsTitle.search('4833025324', 0, 538, 1))
    print(BldRgsTitle.search('4833025324', 0, 538))
    #print(BldRgsPrice.search('1168010300', 0, 12, 0))
    #print(BldRgsPrice.search('4833025324', 0, 508, 14))
