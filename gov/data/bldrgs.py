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
        url = BldRgs.service_url + service_name
        params = BldRgs.params
        params['sigunguCd'] = lawd_cd[0:5]
        params['bjdongCd'] = lawd_cd[5:10]
        params['platGbCd'] = f'{is_san}'
        if bonbun:
            params['bun'] = f'{bonbun:04}'
        if bubun:
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
        pass

    def __repr__(self):
        str = f''
        return str

    @staticmethod
    def search(lawd_cd, is_san, bonbun=None, bubun=None):
        result = []

        root = BldRgs.search(BldRgsTitle.service_name, lawd_cd, is_san, bonbun, bubun)

        for item in root.iter('item'):
            print(item.findtext('platPlc'))
        
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
