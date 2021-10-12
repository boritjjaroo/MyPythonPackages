import requests
import xml.etree.ElementTree as ET
import gov.data.util as util

# 공공데이터포털(data.go.kr)
# 국토교통부_건축소유자정보 서비스(https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15021136)

class ArchOwn:

    service_url = 'http://apis.data.go.kr/1611000/OwnerInfoService/getArchitecturePossessionInfo'
    params = {
        'serviceKey': util.service_key,
        'numOfRows': '1000',
        'pageNo': '1',
        # 5자리
        'sigungu_cd': '48330',
        'bjdong_cd': '25324',
        # 0:대지 1:산 2:블록
        'plat_gb_cd': '0',
        'bun': '',
        'ji': '',
        'dong_nm': '',
        'ho_nm': '',
    }

    def __init__(self):
        self.owner = ''
        self.change_date = ''
        pass

    def __repr__(self):
        str = f'{self.owner} {self.change_date}'
        return str

    @staticmethod
    def search(lawd_cd, is_san, bonbun, bubun=None, dong=None, ho=None, rows=None, page=None):
        result = []

        url = ArchOwn.service_url
        params = ArchOwn.params
        params['sigungu_cd'] = lawd_cd[0:5]
        params['bjdong_cd'] = lawd_cd[5:10]
        params['plat_gb_cd'] = f'{is_san}'
        if bonbun:
            params['bun'] = f'{bonbun:04}'
        if bubun:
            params['ji'] = f'{bubun:04}'
        if dong:
            params['dong_nm'] = dong
        if ho:
            params['ho_nm'] = ho
        if rows:
            params['numOfRows'] = rows
        if page:
            params['pageNo'] = page


        response = requests.get(url, params=params)
        if response.status_code != 200 :
            print(f'getArchitecturePossessionInfo Http error : {response.status_code}')
            return None

        #response 데이터 확인
        #print(response.content)

        root = ET.fromstring(response.content.decode('utf-8'))
        print(f"getArchitecturePossessionInfo : {root.find('header').findtext('resultMsg')}")

        for item in root.iter('item'):
            arch_own = ArchOwn()
            arch_own.owner = item.findtext('nm')
            arch_own.change_date = item.findtext('chang_caus_day')
            result.append(arch_own)
        
        return result


if __name__ == "__main__":
    print(ArchOwn.search('4833025324', 0, 538))
