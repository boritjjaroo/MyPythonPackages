import requests
import xml.etree.ElementTree as ET
import gov.data.util as util

# 공공데이터포털(data.go.kr)
# 국토교통부_공동주택 단지 목록제공 서비스(https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15057332)

class AptList:

    service_url = 'http://apis.data.go.kr/1613000/AptListService1/'
    service_name = 'getLegaldongAptList'
    params = {
        'serviceKey': util.service_key,
        'numOfRows': '1000',
        'pageNo': '1',
    }

    def __init__(self):
        self.code = ''
        self.name = ''

    def __repr__(self):
        str = f'{self.name}'
        return str

    @classmethod
    def search_(cls, params):
        result = []

        url = cls.service_url + cls.service_name

        response = requests.get(url, params=params)
        if response.status_code != 200 :
            print(f'{cls.service_name} Http error : {response.status_code}')
            return result

        #response 데이터 확인
        #print(response.content)

        root = ET.fromstring(response.content.decode('utf-8'))
        print(f"{cls.service_name} : [{root.find('body').findtext('totalCount')}건] {root.find('header').findtext('resultMsg')}")

        for item in root.iter('item'):
            data = cls()
            data.code = item.findtext('kaptCode', '')
            data.name = item.findtext('kaptName', '')
            result.append(data)

        return result


# 국토교통부_시군구 아파트 목록
class AptListSiGunGu(AptList):

    service_name = 'getSigunguAptList'

    def __init__(self):
        super().__init__()

    @classmethod
    def search(cls, lawd_cd):
        params = cls.params
        params['sigunguCode'] = lawd_cd[0:5]

        return cls.search_(params)


# 국토교통부_법정동 아파트 목록
class AptListLawdCD(AptList):

    service_name = 'getLegaldongAptList'

    def __init__(self):
        super().__init__()

    @classmethod
    def search(cls, lawd_cd):
        params = cls.params
        params['bjdCode'] = lawd_cd

        return cls.search_(params)


if __name__ == "__main__":
    print(AptListLawdCD.search('4128112800'))
    print(AptListLawdCD.search('4833025300'))
    print(AptListSiGunGu.search('4833025300'))
